"""
validate_project_context.py — Valida el formato de `.d365-project.md` (el contexto estático
y compartido del proyecto: Dataverse, Azure DevOps definitivo, suscripciones de Azure,
publisher prefix). Se corre antes de dar por completo el handoff Fase 1 → Fase 2.

Solo valida FORMATO (URLs bien formadas, campos no vacíos, prefix correcto) — nunca valida
que las URLs/suscripciones existan de verdad o sean accesibles (eso requeriría conectividad
real, fuera del alcance de esta skill). "Formato válido" no es lo mismo que "dato correcto" —
decile esto al usuario si pregunta.

Uso:
    python validate_project_context.py .d365-project.md
"""

from __future__ import annotations

import re
import sys
from pathlib import Path
from urllib.parse import urlparse

REQUIRED_DATAVERSE_ENVS = ["DEV", "TEST", "PROD"]
EXPECTED_PREFIX = "axx"


def is_valid_url(value: str) -> bool:
    if not value or value.strip() in ("", "—", "-"):
        return False
    try:
        parsed = urlparse(value.strip())
        return parsed.scheme in ("http", "https") and bool(parsed.netloc)
    except ValueError:
        return False


def is_nonempty(value: str | None) -> bool:
    return bool(value and value.strip() and value.strip() not in ("—", "-", "TBD", "TODO"))


def parse_project_context(text: str) -> dict:
    """Parser simple orientado al schema definido en axxon-orchestrator/SKILL.md — no es un
    parser de Markdown genérico, asume la estructura de secciones/bullets documentada ahí."""
    data: dict = {"dataverse": {}, "ado": {}, "azure_subscriptions": [], "prefix": None, "adr_wiki": None, "equipo": None}

    dataverse_section = re.search(r"## Dataverse\n(.*?)(?=\n## |\Z)", text, re.DOTALL)
    if dataverse_section:
        for env in REQUIRED_DATAVERSE_ENVS:
            m = re.search(rf"-\s*{env}:\s*(\S+)", dataverse_section.group(1))
            data["dataverse"][env] = m.group(1) if m else None

    ado_section = re.search(r"## Azure DevOps.*?\n(.*?)(?=\n## |\Z)", text, re.DOTALL)
    if ado_section:
        for field, label in [("organizacion", "Organización"), ("project", "Project"), ("repo", "Repo")]:
            m = re.search(rf"-\s*{label}:\s*(.+)", ado_section.group(1))
            data["ado"][field] = m.group(1).strip() if m else None

    azure_section = re.search(r"## Azure — suscripciones\n(.*?)(?=\n## |\Z)", text, re.DOTALL)
    if azure_section:
        data["azure_subscriptions"] = [
            line.strip("- ").strip()
            for line in azure_section.group(1).splitlines()
            if line.strip().startswith("-")
        ]

    prefix_section = re.search(r"## Publisher prefix\n(.*?)(?=\n## |\Z)", text, re.DOTALL)
    if prefix_section:
        m = re.search(r"-\s*(\S+)", prefix_section.group(1))
        data["prefix"] = m.group(1) if m else None

    # Opcional — solo se valida si la sección existe (la usa adr-recorder).
    wiki_section = re.search(r"## Wiki de ADRs\n(.*?)(?=\n## |\Z)", text, re.DOTALL)
    if wiki_section:
        data["adr_wiki"] = {}
        for field, label in [("wiki", "Wiki"), ("ruta", "Ruta raíz")]:
            # [ \t]* (no \s*): un valor vacío no debe capturar la línea siguiente.
            m = re.search(rf"^[ \t]*-[ \t]*{label}:[ \t]*(.*)$", wiki_section.group(1), re.MULTILINE)
            data["adr_wiki"][field] = m.group(1).strip() if m else None

    # Opcional — roles del equipo (flujo entre roles, docs/ado-contract.md).
    team_section = re.search(r"## Equipo\n(.*?)(?=\n## |\Z)", text, re.DOTALL)
    if team_section:
        data["equipo"] = [
            line.strip()[1:].strip()
            for line in team_section.group(1).splitlines()
            if line.strip().startswith("-") and not line.strip()[1:].strip().startswith("(")
        ]

    return data


VALID_ROLES = {"funcional", "customizador", "dev", "tech lead", "pm"}


def check_team(data: dict) -> tuple[list[str], list[str]]:
    """Devuelve (errores, avisos) de la sección opcional `## Equipo`.
    Ausente → aviso. Presente → cada línea `persona: rol[, rol]` con roles válidos."""
    team = data.get("equipo")
    if team is None:
        return [], ["Equipo: sección ausente (opcional) — los agentes van a preguntar el rol una vez por sesión."]
    if not team:
        return ["Equipo: la sección existe pero no lista a nadie."], []

    errors = []
    for i, entry in enumerate(team, 1):
        if ":" not in entry:
            errors.append(f"Equipo #{i}: '{entry}' — formato esperado 'persona: rol'.")
            continue
        persona, roles_raw = entry.rsplit(":", 1)
        if not is_nonempty(persona):
            errors.append(f"Equipo #{i}: falta la persona.")
        roles = [r.strip().lower() for r in roles_raw.split(",") if r.strip()]
        if not roles:
            errors.append(f"Equipo #{i}: falta el rol de '{persona.strip()}'.")
        for r in roles:
            if r not in VALID_ROLES:
                errors.append(
                    f"Equipo #{i}: rol '{r}' no válido para '{persona.strip()}' "
                    f"(válidos: Funcional, Customizador, Dev, Tech lead, PM)."
                )
    return errors, []


def check_adr_wiki(data: dict) -> tuple[list[str], list[str]]:
    """Devuelve (errores, avisos) de la sección opcional `## Wiki de ADRs`.
    Ausente → solo aviso (no bloquea el handoff). Presente pero mal formada → error."""
    wiki = data.get("adr_wiki")
    if wiki is None:
        return [], ["Wiki de ADRs: sección ausente (opcional) — adr-recorder la va a pedir cuando haga falta."]

    errors = []
    if not is_nonempty(wiki.get("wiki")):
        errors.append("Wiki de ADRs — Wiki: falta o está vacío.")
    ruta = wiki.get("ruta")
    if not is_nonempty(ruta):
        errors.append("Wiki de ADRs — Ruta raíz: falta o está vacío.")
    elif not ruta.startswith("/"):
        errors.append(f"Wiki de ADRs — Ruta raíz: '{ruta}' debe empezar con '/' (ej. /Arquitectura/ADRs).")
    return errors, []


def validate(data: dict) -> list[str]:
    """Devuelve la lista de errores — vacía significa que el formato está OK."""
    errors = []

    for env in REQUIRED_DATAVERSE_ENVS:
        value = data["dataverse"].get(env)
        if not is_nonempty(value):
            errors.append(f"Dataverse {env}: falta o está vacío.")
        elif not is_valid_url(value):
            errors.append(f"Dataverse {env}: '{value}' no tiene forma de URL válida (falta https:// o el dominio).")

    for field, label in [("organizacion", "Organización"), ("project", "Project"), ("repo", "Repo")]:
        if not is_nonempty(data["ado"].get(field)):
            errors.append(f"Azure DevOps — {label}: falta o está vacío.")

    if not data["azure_subscriptions"]:
        errors.append("Azure — suscripciones: no hay ninguna listada (se necesita al menos una).")
    else:
        for i, sub in enumerate(data["azure_subscriptions"], 1):
            if not is_nonempty(sub):
                errors.append(f"Azure — suscripción #{i}: entrada vacía.")

    prefix = data.get("prefix")
    if not is_nonempty(prefix):
        errors.append("Publisher prefix: falta o está vacío.")
    elif prefix.rstrip("_") != EXPECTED_PREFIX:
        errors.append(
            f"Publisher prefix: '{prefix}' — se esperaba '{EXPECTED_PREFIX}_' (convención fija "
            f"del proyecto, no una preferencia). Si es intencional, confirmalo explícitamente "
            f"con el usuario antes de seguir, no lo corrijas en silencio."
        )

    return errors


def main() -> int:
    if len(sys.argv) != 2:
        print("Uso: python validate_project_context.py .d365-project.md", file=sys.stderr)
        return 1

    path = Path(sys.argv[1])
    if not path.exists():
        print(f"ERROR: no existe '{path}'. Todavía no se completó el contexto del proyecto.", file=sys.stderr)
        return 1

    text = path.read_text(encoding="utf-8")
    data = parse_project_context(text)
    errors = validate(data)
    wiki_errors, warnings = check_adr_wiki(data)
    errors += wiki_errors
    team_errors, team_warnings = check_team(data)
    errors += team_errors
    warnings += team_warnings

    for w in warnings:
        print(f"⚠️  {w}")

    if errors:
        print(f"❌ '{path}' tiene {len(errors)} problema(s) de formato — NO dar por completo el handoff:\n")
        for e in errors:
            print(f"  - {e}")
        return 1

    print(f"✅ '{path}' pasa la validación de formato.")
    print("   Recordatorio: esto valida FORMATO, no que los datos sean correctos ni que las")
    print("   URLs/suscripciones existan de verdad — confirmar eso sigue siendo responsabilidad")
    print("   de quien completó el archivo.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
