---
name: strategize-analyst
description: >
  BLOQUEADO — pendiente de contenido. Subagente de la Fase 0 · Strategize (Success by Design
  de Microsoft): licenciamiento, respuesta formal a RFP, y estimación de esfuerzo/recursos,
  previo a que el proyecto tenga Sprint 0. No activar todavía — las skills que necesita
  (licensing-analyser, rfp-manager, d365crm-resoruces-estimator) no están empaquetadas como
  plugin. Ver ADR-004 para el estado.
model: sonnet
skills: []
---

# Strategize Analyst — subagente de Axxon Dataverse Agent (BLOQUEADO)

> ⚠️ **Este subagente todavía no tiene contenido.** El campo `skills:` está vacío a propósito
> — las 3 skills que necesita (`licensing-analyser`, `rfp-manager`,
> `d365crm-resoruces-estimator`) existen sueltas en el entorno de quien armó este proyecto,
> pero no están empaquetadas como plugin distribuible (`axxon-strategize-suite`, pendiente).
>
> Cuando ese plugin exista:
> 1. Agregar `skills: [licensing-analyser, rfp-manager, d365crm-resoruces-estimator]` acá.
> 2. Declarar `axxon-strategize-suite` como `dependencies` en `plugin.json` de este plugin.
> 3. Escribir el cuerpo real siguiendo el mismo patrón que `sprint0-analyst.md`
>    (routing interno entre las 3 skills, handoff a Fase 1, restricciones).
>
> Ver `docs/ADR-004-supra-agent-architecture.md`, sección "Pendiente", para el estado exacto.
