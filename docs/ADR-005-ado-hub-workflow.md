# ADR-005 — ADO del proyecto como punto de encuentro entre agentes y roles

**Estado:** Aceptado (decisión 1 — uso del campo `Activity` — abierta)
**Fecha:** 2026-11-04
**Contexto del proyecto:** Axxon Dataverse Agent — Axxon Consulting
**Relacionado:** ADR-004 (supraagente), ADR-005/ADR-006 de `axxon-dataverse-architect` (ADRs del proyecto, pro-code)

> Nota de numeración: este ADR-005 es del repo `axxon-dataverse-agent` y es distinto del
> ADR-005 de `axxon-dataverse-architect`. La colisión de numeración entre repos es un
> pendiente conocido.

---

## Contexto

En un proyecto de implementación, los agentes los usan personas con roles distintos:
consultores funcionales / customizadores (low-code) y devs (pro-code), más tech lead y PM.
Cada uno corre sus agentes en su propia sesión y máquina. Sin un lugar común, el plan
aprobado, el contrato técnico de una pieza pro-code o un handoff quedan en la conversación de
una persona y se pierden.

Premisa del negocio: las User Stories se encaran desde la óptica funcional y pueden contener
tareas de desarrollo; las historias de desarrollo puro son las menos.

## Decisión

1. **El Azure DevOps del proyecto es el pivot.** Los agentes no se comunican entre sí: leen y
   escriben un **contrato estándar** en los work items — `docs/ado-contract.md` (tags,
   comentarios con marcador, Tasks, dependencias, estados).
2. **La US funcional es la unidad de trabajo**; el pro-code son **Tasks hijas** (`[PC]`,
   `build-procode`, sin asignar) que toma un dev. Historias técnicas puras: US con tag
   `us-tecnica`.
3. **Plan aprobado en ADO:** `ado-us-planner` usa `build-approach-advisor` y publica el Plan de
   construcción como comentario `[axx:plan-construccion v1]` + tag `plan-aprobado`. La parte
   pro-code la aprueba el **tech lead** (`[axx:aprobacion-procode v1]`).
4. **Cola del dev:** skill nueva `ado-dev-queue` (delivery-suite) — lista Tasks
   `build-procode` sin asignar, el dev toma una, el agente arma el contexto (US + plan +
   contrato técnico + ADRs) y lo pasa a `dataverse-builder`.
5. **Roles** en `.d365-project.md`, sección opcional `## Equipo`; si falta, el agente pregunta
   el rol una vez por sesión.
6. **Acceso a ADO solo vía el servidor MCP oficial** — `ado-us-planner` deja de usar
   `ado_client.py` y PAT.

### Decisión abierta

- **Campo `Activity`** (disciplina de la Task): depende del process template de cada
  proyecto. Hasta decidirlo, los agentes no lo escriben y las colas/reportes usan tags.

### Alternativas descartadas

- **Comunicación directa entre agentes / sesiones:** no deja registro, no sobrevive a la
  sesión, y no es visible para quien no usa agentes.
- **User Story separada para el pro-code:** duplica criterios de aceptación y rompe la
  trazabilidad funcional; se reserva para `us-tecnica`.
- **Tipo de work item nuevo para historias técnicas:** obliga a modificar el process template
  del cliente.

## Consecuencias

- Cualquier persona del equipo (con o sin agentes) ve el plan, el contrato y el estado en ADO.
- Todas las skills que tocan work items dependen del servidor MCP de Azure DevOps — hereda el
  pendiente de conectividad (config remota OAuth vs. local stdio).
- El contrato es un acoplamiento entre 4 repos: cambiarlo requiere actualizar
  `docs/ado-contract.md` primero y versionar el marcador de comentario (`v1` → `v2`).

## Pendiente

- Decisión 1 (`Activity`).
- Migrar a MCP el resto de las skills que todavía usan `ado_client.py` (`ado-daily-prep` se
  migra en este mismo cambio; quedan las de sprint0-suite).
