# Changelog — Axxon Dataverse Agent

## v0.9.0 (2026-11-04)

Soporte para el registro de ADRs del proyecto (skill `adr-recorder`, Axxon Dataverse
Architect v1.7.0-rc1 — ver ADR-005 de ese repo).

- **`.d365-project.md`**: nueva sección opcional `## Wiki de ADRs` (Wiki, Ruta raíz) en el
  schema de `axxon-orchestrator`.
- **`validate_project_context.py`**: valida la sección solo si está presente (Wiki no vacía,
  Ruta raíz empieza con `/`); si falta, emite un aviso sin bloquear el handoff Fase 1 → Fase 2.
  El parser de esta sección usa `[ \t]*` en vez de `\s*` para que un valor vacío no capture la
  línea siguiente.
- **`dataverse-builder`**: menciona `adr-recorder` y dónde se loguea un ADR registrado
  (`.d365-fases/fase-2-implement.md`).

## v0.8.1 (2026-08-21)

- **Fix crítico de carga**: el plugin no cargaba ("couldn't be loaded") desde v0.1.0. Causa
  raíz: `skills:` en el frontmatter de los 5 subagentes (`agents/*.md`) y `dependencies` en
  `plugin.json` no son campos reales del schema de Claude Code — no existe mecanismo de
  cross-linking de skills entre plugins ni de dependencias declarativas entre plugins.
  Confirmado por comparación contra plugins oficiales (`claude-plugins-official`) y contra
  `axxon-dataverse-architect`, ninguno de los cuales usa esos campos.
- Eliminado `skills:` del frontmatter de `dataverse-builder`, `strategize-analyst`,
  `sprint0-analyst`, `delivery-manager`, y `deploy-manager`. El texto en prosa de cada agente
  ya indicaba qué skill invocar por nombre (p. ej. "Delegás la ejecución técnica a la skill
  `dataverse-architect`") — eso se conserva como instrucción para que el subagente invoque la
  skill vía la tool `Skill` en runtime, en vez de un scoping declarativo inexistente.
- Eliminado `dependencies` de `plugin.json`. Los prerequisitos de instalación (que el usuario
  tenga instalados `axxon-dataverse-architect`, `axxon-strategize-suite`,
  `axxon-sprint0-suite`, `axxon-delivery-suite`) ya estaban documentados en prosa dentro de
  cada `agents/*.md` ("Prerequisito de instalación") y en el README — se mantienen como la
  única fuente de verdad, ahora que no hay campo declarativo que los reemplace.
- **Retroactivo**: todo lo documentado como `skills:`/`dependencies` reales en v0.2.0–v0.8.0
  nunca funcionó como mecanismo de carga — era metadata inerte que además rompía la
  validación del plugin. Este fix no cambia el comportamiento pretendido de ningún subagente,
  solo hace que el plugin cargue.

## v0.1.0 (2026-08-05)

Primera versión. Define la arquitectura del supraagente (ver ADR-004): 3 subagentes por fase
de consultoría (`presales-analyst`, `dataverse-builder`, `delivery-manager`), usando el
mecanismo nativo de Subagents de Claude Code (no Agent Teams — experimental y no aplica al
patrón jerárquico buscado).

### Incluido
- `plugin.json` con dependencia declarada de `axxon-dataverse-architect`.
- 3 definiciones de subagente (`agents/*.md`), cada una con su `skills:` scoping.
- Skill raíz `axxon-orchestrator` con el mapa de fases y las reglas de handoff entre ellas.

### Conocido / no bloqueante
- `presales-analyst` y `delivery-manager` dependen de skills que hoy no están empaquetadas
  como plugins — no son portables al resto del equipo todavía. `dataverse-builder` sí lo es.

### Pendiente
- Empaquetar las skills de presales (`d365-requirements-analyst`, `bpc-analyser`,
  `licensing-analyser`, `rfp-manager`, `d365crm-resoruces-estimator`) como plugin propio.
- Empaquetar las skills de delivery (`ado-daily-prep`, `ado-us-planner`) como plugin propio.
- Resolver `output-formatter` (pendiente de otro proyecto) antes de incorporarlo.

## v0.2.0 (2026-08-05)

- Empaquetados `axxon-sprint0-suite` (d365-requirements-analyst, bpc-analyser) y
  `axxon-delivery-suite` (ado-daily-prep, ado-us-planner) como plugins reales.
- Renombrado `presales-analyst` → `sprint0-analyst`, acotado su `skills:` a las 2 skills
  realmente empaquetadas (licensing-analyser, rfp-manager, d365crm-resoruces-estimator quedan
  fuera por decisión explícita — no son Sprint 0).
- `plugin.json` ahora declara `axxon-dataverse-architect`, `axxon-sprint0-suite`, y
  `axxon-delivery-suite` como `dependencies` reales.
- Los 3 subagentes son portables al equipo — resuelta la limitación documentada en v0.1.0.

## v0.3.0 (2026-08-05)

- Mapeados los 3 subagentes contra Success by Design de Microsoft (Strategize/Plan/Implement/
  Deploy/Operate): sprint0-analyst → Plan, dataverse-builder → Implement, delivery-manager →
  Implement (gobierno de sprint, en paralelo).
- Documentados como gaps explícitos: Strategize y Operate sin subagente; Deploy cubierta solo
  parcialmente por solution-packager.
- Corregidas referencias residuales a "presales-analyst" que habían quedado sin actualizar en
  dataverse-builder.md, delivery-manager.md, y README.md tras el rename de v0.2.0.

## v0.4.0 (2026-08-05)

- Numeración explícita de fases: Fase 0 Strategize, Fase 1 Plan, Fase 2 Implement, Fase 3
  Deploy, Fase 4 Operate (sin agentizar).
- Nuevo subagente `deploy-manager` (Fase 3) — reutiliza `dataverse-architect`, sin contenido
  nuevo, encuadrado para promoción/cutover en vez de construcción.
- Nuevo stub `strategize-analyst` (Fase 0) — bloqueado, `skills: []`, a la espera de empaquetar
  `axxon-strategize-suite` (licensing-analyser, rfp-manager, d365crm-resoruces-estimator).
- Nuevo mecanismo de identificación de fase por chat: cada consultor trabaja un chat por fase
  ("Fase N - Nombre"); `axxon-orchestrator` pregunta la fase si no es evidente.
- Modelo de sesión reemplazado: de un `.d365-session.md` único a `.d365-project.md` (estático,
  compartido) + `.d365-fases/fase-N-nombre.md` (un log de acciones por fase, evita condiciones
  de carrera entre fases trabajadas en paralelo).

## v0.6.0 (2026-08-07)

- sprint0-analyst now loads 7 skills (up from 4): added fdd-builder, backlog-refiner,
  fit-gap-rollup, effort-recalibration. Documented the natural sequence within an Epic and
  explicitly distinguished "estimación comercial" (out of scope, presales) from "recalibración
  de esfuerzo técnica" (in scope, Fase 1 close).
- ADR-004: added Decision 2f (skill fusion + fdd-builder naming/neutralization) and Decision
  2g (effort recalibration cycle design). Updated the Blueprint pending note to reflect that
  its 3 input pieces (fdd-builder, fit-gap-rollup, effort-recalibration) now exist.

## v0.7.0 (2026-08-07)

- sprint0-analyst now loads blueprint-builder (8th skill) - Solution Blueprint per the 10
  official Success by Design areas, closing Fase 1 formally.
- Hardened .d365-project.md into a real gate: added an explicit "Paso 0" block at the top of
  dataverse-builder, deploy-manager, and delivery-manager - runs
  validate_project_context.py before processing any user request, no exceptions, blocking
  language throughout. sprint0-analyst's handoff section treats this as a hard blocker too.
- ADR-004: added Decision 2h (formal .d365-project.md schema + validation) and Decision 2i
  (blueprint-builder design, resolving the Blueprint pending item from 2e/2f/2g).

## v0.8.0 (2026-08-18)

- Nueva doc de prerequisito: `docs/prerequisites-ado-mcp-server.md` — instrucciones
  verificadas contra el repo real (microsoft/azure-devops-mcp) para instalar el servidor MCP
  oficial de Microsoft (opción remota sin instalación, o local vía `claude mcp add`), con
  autenticación PAT recomendada por consistencia con `ADO_PAT` de `axxon-ado-connector`.
- Aclarado explícitamente que este servidor es un complemento, no un reemplazo de las 8
  skills que ya usan `ado_client.py` propio — evita que se asuma una migración implícita.
- Referenciado desde el README raíz, sección nueva "Prerequisito opcional".
- Confirmado (contra `code.claude.com/docs/en/mcp`) el comando exacto de Claude Code para la
  opción remota: `claude mcp add --transport http azure-devops https://mcp.dev.azure.com/{org}`
  — sin Node.js, sin `npx`, solo login OAuth vía `/mcp`. Corregido en el doc, que antes lo
  dejaba como "a verificar".
