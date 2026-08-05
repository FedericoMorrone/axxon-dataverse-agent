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
