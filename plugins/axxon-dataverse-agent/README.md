# Axxon Dataverse Agent

Supraagente orquestador de Axxon Consulting para proyectos Dynamics 365 / Power Platform.
Coordina subagentes especializados por fase de **Success by Design** (Microsoft) a lo largo
del ciclo de vida completo del proyecto — ver `docs/ADR-004-supra-agent-architecture.md` en
la raíz del repo para el razonamiento arquitectónico completo.

**Estado: v0.4.0 — 4 de 5 fases agentizadas. Fase 4 (Operate) no se agentiza por decisión
explícita. Fase 0 (Strategize) tiene subagente definido pero bloqueado hasta empaquetar su
plugin de contenido (ver "Estado de portabilidad").**

---

## Estructura

```
axxon-dataverse-agent/
├── .claude-plugin/
│   └── plugin.json               ← manifiesto, dependencias de los otros plugins Axxon
├── agents/
│   ├── strategize-analyst.md     ← Fase 0 · licensing, RFP, estimación (bloqueado, ver abajo)
│   ├── sprint0-analyst.md        ← Fase 1 · requerimientos, BPC
│   ├── dataverse-builder.md      ← Fase 2 · delega en la skill dataverse-architect
│   ├── delivery-manager.md       ← Fase 2 · daily prep, planificación de tasks
│   └── deploy-manager.md         ← Fase 3 · promoción TEST/PROD, checklist, cutover
└── skills/
    └── axxon-orchestrator/
        └── SKILL.md              ← coordinación, mapa de fases, logs por fase
```

## Los 5 subagentes (por fase Success by Design)

| Fase | Subagente | Skills que carga |
|---|---|---|
| 0 · Strategize | `strategize-analyst` | `licensing-analyser`, `rfp-manager`, `d365crm-resoruces-estimator` — **plugin pendiente** |
| 1 · Plan | `sprint0-analyst` | `d365-requirements-analyst`, `bpc-analyser` |
| 2 · Implement | `dataverse-builder` | `dataverse-architect` (del plugin Axxon Dataverse Architect) |
| 2 · Implement (paralelo) | `delivery-manager` | `ado-daily-prep`, `ado-us-planner` |
| 3 · Deploy | `deploy-manager` | `dataverse-architect` (mismo plugin que `dataverse-builder`, encuadre distinto) |
| 4 · Operate | — | No agentizado — decisión explícita |

## Identificación de fase y logs (nuevo en v0.4.0)

Cada consultor trabaja **un chat de Cowork por fase** ("Fase 1 - Plan", etc.). El contexto se
guarda en dos tipos de archivo dentro del Cowork Project del cliente:

- `.d365-project.md` — contexto estático (environment, solución, publisher, repo ADO),
  compartido por todas las fases.
- `.d365-fases/fase-N-nombre.md` — un log de acciones **por fase**, para que dos fases
  trabajadas en paralelo (en chats distintos) no se pisen entre sí.

Ver el detalle completo en `skills/axxon-orchestrator/SKILL.md`.

## Estado de portabilidad

| Subagente | ¿Portable al equipo hoy? |
|---|---|
| `strategize-analyst` | **No** — su plugin (`axxon-strategize-suite`) todavía no está empaquetado |
| `sprint0-analyst` | Sí — depende de `axxon-sprint0-suite`, plugin real (v0.1.0) |
| `dataverse-builder` | Sí — depende de `axxon-dataverse-architect`, plugin real (RC1) |
| `delivery-manager` | Sí — depende de `axxon-delivery-suite`, plugin real (v0.1.0) — con la salvedad de `ado-connector` pendiente (no bloqueante) |
| `deploy-manager` | Sí — depende de `axxon-dataverse-architect`, ya empaquetado |

## Uso

Los subagentes se invocan automáticamente según relevancia, o explícitamente con @-mención:

```
@axxon-dataverse-agent:sprint0-analyst analizame este RFP
@axxon-dataverse-agent:dataverse-builder creá la tabla de solicitudes de crédito
@axxon-dataverse-agent:delivery-manager preparame la daily de hoy
@axxon-dataverse-agent:deploy-manager preparemos el deployment checklist para TEST
```

O simplemente describí el pedido en lenguaje natural — el subagente correcto se activa solo
por su `description`. Si no es evidente en qué fase estás, `axxon-orchestrator` te lo pregunta
una vez al principio del chat.
