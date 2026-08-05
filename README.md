# Axxon Dataverse Agent — Repositorio

Supraagente orquestador de Axxon Consulting para proyectos Dynamics 365 / Power Platform.
Comanda tres subagentes especializados por fase (presales, build, delivery) usando el
mecanismo nativo de **Subagents** de Claude Code/Cowork.

Ver `docs/ADR-004-supra-agent-architecture.md` para la decisión arquitectónica completa
(por qué Subagents y no Agent Teams, cómo se agruparon las fases, y la limitación real de
ahora los 3 subagentes son portables — ver v0.2.0).

**Estado actual: v0.3.0** (los 3 subagentes son portables y ya están mapeados contra Success
by Design de Microsoft; ver ADR-004 para los gaps de fase pendientes — no bloqueante).

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
│       │   ├── sprint0-analyst.md
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

Requiere tener también instalados `axxon-dataverse-architect`, `axxon-sprint0-suite`, y
`axxon-delivery-suite` — los tres quedan declarados como `dependencies` en `plugin.json`.
