# Axxon Dataverse Agent — Repositorio

Supraagente orquestador de Axxon Consulting para proyectos Dynamics 365 / Power Platform.
Comanda subagentes especializados por fase usando el mecanismo nativo de **Subagents** de
Claude Code/Cowork — no Agent Teams.

Ver `docs/ADR-004-supra-agent-architecture.md` para la decisión arquitectónica completa.

**Estado actual: v0.5.0** — 5 subagentes definidos (Fase 0 a Fase 3), **todos funcionales y
portables**. Fase 4 (Operate) explícitamente sin agentizar.

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
│       │   ├── strategize-analyst.md   ← Fase 0
│       │   ├── sprint0-analyst.md      ← Fase 1
│       │   ├── dataverse-builder.md    ← Fase 2
│       │   ├── delivery-manager.md     ← Fase 2 (paralelo)
│       │   └── deploy-manager.md       ← Fase 3
│       ├── skills/axxon-orchestrator/SKILL.md
│       ├── README.md
│       └── CHANGELOG.md
└── docs/
    └── ADR-004-supra-agent-architecture.md
```

## Relación con los otros repos Axxon

Este repo **depende de** 4 plugins, cada uno en su propio repo:
- `axxon-dataverse-architect` (Fase 2/3 — `dataverse-builder`, `deploy-manager`)
- `axxon-strategize-suite` (Fase 0 — `strategize-analyst`)
- `axxon-sprint0-suite` (Fase 1 — `sprint0-analyst`)
- `axxon-delivery-suite` (Fase 2 — `delivery-manager`)

## Instalación

```
/plugin marketplace add <url-de-este-repo>
/plugin install axxon-dataverse-agent@axxon-dataverse-agent-marketplace
```

Requiere también instalados los 4 plugins de dependencia — declarados en `plugin.json`.

## Prerequisito — servidor MCP de Azure DevOps (dejó de ser opcional, ver ADR-001)

`backlog-seeder` ya requiere este servidor conectado (ya no usa HTTP directo) — el resto de
las skills que tocan Azure DevOps se están migrando progresivamente. Ver
[`docs/prerequisites-ado-mcp-server.md`](docs/prerequisites-ado-mcp-server.md) para las
instrucciones exactas (opción remota sin instalación, o local vía `claude mcp add`).
