# Axxon Dataverse Agent

Supraagente orquestador de Axxon Consulting para proyectos Dynamics 365 / Power Platform.
Coordina tres subagentes especializados a lo largo del ciclo de vida completo del proyecto —
ver `docs/ADR-004-supra-agent-architecture.md` en la raíz del repo para el razonamiento
arquitectónico completo.

**Estado: v0.2.0 — los 3 subagentes son portables al equipo (ver "Estado de portabilidad" abajo).**

---

## Estructura

```
axxon-dataverse-agent/
├── .claude-plugin/
│   └── plugin.json              ← manifiesto, declara dependencia de axxon-dataverse-architect
├── agents/
│   ├── sprint0-analyst.md      ← requerimientos, BPC
│   ├── dataverse-builder.md     ← delega en la skill dataverse-architect
│   └── delivery-manager.md      ← daily prep, planificación de tasks
└── skills/
    └── axxon-orchestrator/
        └── SKILL.md              ← coordinación de alto nivel, mapa de fases y handoffs
```

## Los 3 subagentes

| Subagente | Fase | Skills que carga |
|---|---|---|
| `sprint0-analyst` | Sprint 0 | `d365-requirements-analyst`, `bpc-analyser` |
| `dataverse-builder` | Build / Implementación | `dataverse-architect` (del plugin Axxon Dataverse Architect) |
| `delivery-manager` | Delivery / Gobierno ALM | `ado-daily-prep`, `ado-us-planner` |

## Estado de portabilidad

| Subagente | ¿Portable al equipo hoy? |
|---|---|
| `dataverse-builder` | **Sí** — depende de `axxon-dataverse-architect`, plugin real y versionado (RC1) |
| `sprint0-analyst` | **Sí** — depende de `axxon-sprint0-suite`, plugin real (v0.1.0) |
| `delivery-manager` | **Sí** — depende de `axxon-delivery-suite`, plugin real (v0.1.0) — con la salvedad de que ambas skills tienen lógica de conexión a ADO duplicada en vez de compartida (`ado-connector` pendiente, no bloqueante) |

Los 3 subagentes quedaron portables en v0.2.0 — instalar `axxon-dataverse-agent` alcanza,
siempre que Cowork resuelva también sus 3 dependencias declaradas en `plugin.json`.

## Uso

Los subagentes se invocan automáticamente según relevancia, o explícitamente con @-mención:

```
@axxon-dataverse-agent:sprint0-analyst analizame este RFP
@axxon-dataverse-agent:dataverse-builder creá la tabla de solicitudes de crédito
@axxon-dataverse-agent:delivery-manager preparame la daily de hoy
```

O simplemente describí el pedido en lenguaje natural — el subagente correcto se activa solo
por su `description`.
