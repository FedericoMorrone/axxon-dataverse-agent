# Axxon Dataverse Agent

Supraagente orquestador de Axxon Consulting para proyectos Dynamics 365 / Power Platform.
Coordina tres subagentes especializados a lo largo del ciclo de vida completo del proyecto —
ver `docs/ADR-004-supra-agent-architecture.md` en la raíz del repo para el razonamiento
arquitectónico completo.

**Estado: v0.1.0 — funcional en el entorno del arquitecto que lo construyó, portabilidad
parcial para el resto del equipo (ver "Estado de portabilidad" abajo).**

---

## Estructura

```
axxon-dataverse-agent/
├── .claude-plugin/
│   └── plugin.json              ← manifiesto, declara dependencia de axxon-dataverse-architect
├── agents/
│   ├── presales-analyst.md      ← RFP, BPC, licensing, estimación
│   ├── dataverse-builder.md     ← delega en la skill dataverse-architect
│   └── delivery-manager.md      ← daily prep, planificación de tasks
└── skills/
    └── axxon-orchestrator/
        └── SKILL.md              ← coordinación de alto nivel, mapa de fases y handoffs
```

## Los 3 subagentes

| Subagente | Fase | Skills que carga |
|---|---|---|
| `presales-analyst` | Presales / Discovery | `d365-requirements-analyst`, `bpc-analyser`, `licensing-analyser`, `rfp-manager`, `d365crm-resoruces-estimator` |
| `dataverse-builder` | Build / Implementación | `dataverse-architect` (del plugin Axxon Dataverse Architect) |
| `delivery-manager` | Delivery / Gobierno ALM | `ado-daily-prep`, `ado-us-planner` |

## Estado de portabilidad

| Subagente | ¿Portable al equipo hoy? |
|---|---|
| `dataverse-builder` | **Sí** — depende de `axxon-dataverse-architect`, que ya es un plugin real y versionado (RC1) |
| `presales-analyst` | **No** — depende de 5 skills que hoy son sueltas, no empaquetadas |
| `delivery-manager` | **No** — depende de 2 skills sueltas + `ado-connector` como librería interna |

Para que los otros dos subagentes funcionen en la máquina de otro consultor, esas skills
necesitan empaquetarse como plugins propios primero (ver "Pendiente" en el ADR-004). Hasta
entonces, este plugin funciona completo solo en el entorno donde esas skills ya están
instaladas localmente.

## Uso

Los subagentes se invocan automáticamente según relevancia, o explícitamente con @-mención:

```
@axxon-dataverse-agent:presales-analyst analizame este RFP
@axxon-dataverse-agent:dataverse-builder creá la tabla de solicitudes de crédito
@axxon-dataverse-agent:delivery-manager preparame la daily de hoy
```

O simplemente describí el pedido en lenguaje natural — el subagente correcto se activa solo
por su `description`.
