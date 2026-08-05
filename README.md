# Axxon Dataverse Agent — Repositorio

Supraagente orquestador de Axxon Consulting para proyectos Dynamics 365 / Power Platform.
Comanda tres subagentes especializados por fase (presales, build, delivery) usando el
mecanismo nativo de **Subagents** de Claude Code/Cowork.

Ver `docs/ADR-004-supra-agent-architecture.md` para la decisión arquitectónica completa
(por qué Subagents y no Agent Teams, cómo se agruparon las fases, y la limitación real de
portabilidad de dos de los tres subagentes).

**Estado actual: v0.1.0** (no es RC1 — quedan dependencias pendientes de empaquetar, ver ADR-004).

---

## Estructura

```
axxon-dataverse-agent/
├── .claude-plugin/
│   └── marketplace.json
├── plugins/
│   └── axxon-dataverse-agent/
│       ├── .claude-plugin/plugin.json
│       ├── agents/
│       │   ├── presales-analyst.md
│       │   ├── dataverse-builder.md
│       │   └── delivery-manager.md
│       ├── skills/axxon-orchestrator/SKILL.md
│       ├── README.md
│       └── CHANGELOG.md
└── docs/
    └── ADR-004-supra-agent-architecture.md
```

## Relación con Axxon Dataverse Architect

Este repo **depende de** `axxon-dataverse-architect` (repo separado, ya en RC1) — no lo
contiene ni lo reemplaza. `dataverse-builder` simplemente delega en la skill
`dataverse-architect` de ese plugin.

## Instalación

```
/plugin marketplace add <url-de-este-repo>
/plugin install axxon-dataverse-agent@axxon-dataverse-agent-marketplace
```

Requiere tener también instalado `axxon-dataverse-architect` para que `dataverse-builder`
funcione, y las skills de presales/delivery instaladas localmente para esos dos subagentes
(ver limitación de portabilidad en el README del plugin).
