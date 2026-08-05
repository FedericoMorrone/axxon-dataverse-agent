# Changelog — Axxon Dataverse Agent

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
