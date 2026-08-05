# Axxon Dataverse Agent — Repositorio

Supraagente orquestador de Axxon Consulting para proyectos Dynamics 365 / Power Platform.
Comanda subagentes especializados por fase de **Success by Design** (Microsoft) usando el
mecanismo nativo de **Subagents** de Claude Code/Cowork — no Agent Teams.

Ver `docs/ADR-004-supra-agent-architecture.md` para la decisión arquitectónica completa: por
qué Subagents, cómo se numeran y agrupan las fases (0-4), el mecanismo de logs por fase, y el
estado de portabilidad de cada subagente.

**Estado actual: v0.4.0** — 5 subagentes definidos (Fase 0 a Fase 3, más Fase 4 explícitamente
sin agentizar), 4 de ellos funcionales hoy. `strategize-analyst` (Fase 0) existe como stub
bloqueado hasta empaquetar su plugin de contenido.

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
│       │   ├── strategize-analyst.md   ← Fase 0 · BLOQUEADO, stub sin contenido
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

## Relación con Axxon Dataverse Architect

Este repo **depende de** `axxon-dataverse-architect` (repo separado, ya en RC1) — no lo
contiene ni lo reemplaza. `dataverse-builder` y `deploy-manager` delegan en la skill
`dataverse-architect` de ese plugin, cada uno con un encuadre de fase distinto.

## Instalación

```
/plugin marketplace add <url-de-este-repo>
/plugin install axxon-dataverse-agent@axxon-dataverse-agent-marketplace
```

Requiere tener también instalados `axxon-dataverse-architect`, `axxon-sprint0-suite`, y
`axxon-delivery-suite` — declarados como `dependencies` en `plugin.json`. `strategize-analyst`
queda sin efecto hasta que `axxon-strategize-suite` exista y se agregue como dependencia.
