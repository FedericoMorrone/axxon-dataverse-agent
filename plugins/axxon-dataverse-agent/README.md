# Axxon Dataverse Agent

Supraagente orquestador de Axxon Consulting para proyectos Dynamics 365 / Power Platform.
Coordina subagentes especializados por fase a lo largo del ciclo de vida completo del
proyecto — ver `docs/ADR-004-supra-agent-architecture.md` en la raíz del repo para el
razonamiento arquitectónico completo.

**Estado: v0.5.0 — 5 subagentes, todos funcionales y portables. Fase 4 (Operate) no se
agentiza por decisión explícita.**

---

## Estructura

```
axxon-dataverse-agent/
├── .claude-plugin/
│   └── plugin.json                ← manifiesto, dependencias de los otros plugins Axxon
├── agents/
│   ├── strategize-analyst.md      ← Fase 0 · Kickoff Brief (handoff Ventas → Operaciones)
│   ├── sprint0-analyst.md         ← Fase 1 · requerimientos, BPC
│   ├── dataverse-builder.md       ← Fase 2 · delega en la skill dataverse-architect
│   ├── delivery-manager.md        ← Fase 2 · daily prep, planificación de tasks
│   └── deploy-manager.md          ← Fase 3 · promoción TEST/PROD, checklist, cutover
└── skills/
    └── axxon-orchestrator/
        └── SKILL.md               ← coordinación, mapa de fases, logs por fase
```

## Los 5 subagentes

| Fase | Subagente | Skills que carga |
|---|---|---|
| 0 | `strategize-analyst` | `kickoff-brief` (Kickoff Brief como .pptx, marca Axxon 2025) |
| 1 | `sprint0-analyst` | `d365-requirements-analyst`, `bpc-analyser` |
| 2 | `dataverse-builder` | `dataverse-architect` |
| 2 (paralelo) | `delivery-manager` | `ado-daily-prep`, `ado-us-planner` |
| 3 | `deploy-manager` | `dataverse-architect` (mismo plugin, encuadre distinto) |
| 4 | — | No agentizado — decisión explícita |

> **Nota sobre Fase 0:** no es "Strategize" en el sentido literal de Microsoft (business case
> pre-contrato) — es la transición Ventas → Operaciones, con la propuesta ya aprobada. RFP,
> licenciamiento, y estimación comercial quedan **fuera del alcance de este supraagente**, no
> reubicados a otra fase (ver ADR-004, Decisión 2d).

## Identificación de fase y logs

Cada consultor trabaja **un chat de Cowork por fase** ("Fase 1 - Plan", etc.). El contexto se
guarda en `.d365-project.md` (estático, compartido) + `.d365-fases/fase-N-nombre.md` (log de
acciones por fase, evita que dos fases en paralelo se pisen). Ver
`skills/axxon-orchestrator/SKILL.md` para el detalle completo.

## Estado de portabilidad

Los 5 subagentes son portables — sus 4 plugins de dependencia (`axxon-dataverse-architect`,
`axxon-strategize-suite`, `axxon-sprint0-suite`, `axxon-delivery-suite`) ya existen y están
declarados en `plugin.json`. Única salvedad no bloqueante: `ado-connector` (cliente compartido
para `ado-daily-prep`/`ado-us-planner`) sigue sin empaquetar — cada skill tiene su propia
implementación duplicada.

## Uso

```
@axxon-dataverse-agent:strategize-analyst armá el kickoff brief de este proyecto
@axxon-dataverse-agent:sprint0-analyst analizame este RFP
@axxon-dataverse-agent:dataverse-builder creá la tabla de solicitudes de crédito
@axxon-dataverse-agent:delivery-manager preparame la daily de hoy
@axxon-dataverse-agent:deploy-manager preparemos el deployment checklist para TEST
```

O simplemente describí el pedido en lenguaje natural — el subagente correcto se activa solo
por su `description`. Si no es evidente en qué fase estás, `axxon-orchestrator` te lo pregunta
una vez al principio del chat.
