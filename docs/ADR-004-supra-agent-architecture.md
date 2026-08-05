# ADR-004 — Arquitectura del supraagente Axxon Dataverse Agent

**Estado:** Aceptado
**Fecha:** 2026-08-05
**Contexto del proyecto:** Axxon Dataverse Agent (nuevo repo, separado de Axxon Dataverse Architect)
**Depende de:** ADR-003 (pivot a Claude Cowork) del proyecto Axxon Dataverse Architect

---

## Contexto

Axxon Consulting tiene, además del plugin **Axxon Dataverse Architect** (construcción de
soluciones sobre Dataverse), un conjunto de skills ya construidas para otras fases del ciclo
de vida de un proyecto D365/Power Platform: `d365-requirements-analyst`, `bpc-analyser`,
`licensing-analyser`, `rfp-manager`, `d365crm-resoruces-estimator` (presales/discovery), y
`ado-daily-prep`, `ado-us-planner` (delivery/gobierno ALM diario). Hoy cada una se invoca de
forma independiente, sin una capa que oriente al consultor sobre cuál usar según en qué fase
del proyecto está.

Se necesita un **supraagente orquestador** que "comande" — en palabras del arquitecto — a
todos estos subagentes según la fase del proyecto.

---

## Decisión 1 — Mecanismo: Subagents, no Agent Teams

Claude Code/Cowork ofrece dos mecanismos de multi-agente, y son estructuralmente distintos:

| | Subagents | Agent Teams |
|---|---|---|
| Modelo de coordinación | Jerárquico — un lead delega, el subagente reporta de vuelta | Horizontal — pares que comparten una lista de tareas y se comunican directo entre sí |
| Madurez | GA, estable | Experimental, deshabilitado por default (`CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS`), con limitaciones conocidas de sesión/shutdown |
| Encaja con "comandar subagentes" | Sí — es exactamente este patrón | No — está pensado para trabajo paralelo entre pares, no para jerarquía de mando |

**Se elige Subagents.** Es estable, es el patrón recomendado por Anthropic como punto de
partida, y coincide exactamente con la relación jerárquica que se busca (un supraagente que
comanda, subagentes que ejecutan y reportan).

## Decisión 2 — Agrupamiento por fase de consultoría, no por herramienta

En vez de un subagente por skill (7 subagentes sueltos), se agrupan por fase del ciclo de vida
del proyecto — coincide con la metodología de fases (0-5) que ya usás en proyectos como Neural
Cortex:

| Subagente | Skills que carga (`skills:` en el frontmatter del agent) | Fase |
|---|---|---|
| `sprint0-analyst` | `d365-requirements-analyst`, `bpc-analyser` (plugin `axxon-sprint0-suite`) | Sprint 0 |
| `dataverse-builder` | `dataverse-architect` (plugin `axxon-dataverse-architect`) | Build / Implementación |
| `delivery-manager` | `ado-daily-prep`, `ado-us-planner` (plugin `axxon-delivery-suite`) | Delivery / Gobierno ALM |

> **Actualización (v0.2.0):** el subagente se llamó inicialmente `presales-analyst` con 5
> skills. Al empaquetar el contenido real, el arquitecto decidió explícitamente que
> `licensing-analyser`, `rfp-manager`, y `d365crm-resoruces-estimator` **no** son parte de
> Sprint 0 en la metodología de Axxon — quedan fuera del alcance de este subagente. Se
> renombró a `sprint0-analyst` para reflejar el alcance real, y se acotó su `skills:` a las 2
> que efectivamente están empaquetadas.

Quedan fuera de este agrupamiento:
- **`licensing-analyser`, `rfp-manager`, `d365crm-resoruces-estimator`** — etapa de presales
  anterior al Sprint 0, sin subagente ni plugin propio todavía (decisión explícita del
  arquitecto, no un olvido).
- **`output-formatter`** — dependencia de Copilot Studio (Adaptive Cards), pendiente de rework
  identificado en el proyecto Axxon Dataverse Architect (ADR-003). No se incluye hasta que se
  resuelva esa migración.
- **`ado-connector`** — no es un subagente, es la librería cliente compartida que en teoría
  usan `ado-daily-prep`/`ado-us-planner` — en la práctica, al empaquetar `axxon-delivery-suite`
  no estaba disponible, y ambas skills funcionan con su propia implementación Python inline
  (duplicada). No bloqueante; pendiente como refactor futuro.
- **`skill-creator`** — meta-herramienta transversal (crear/optimizar skills), no pertenece a
  ninguna fase de proyecto. Se deja disponible como skill suelta para el propio supraagente,
  no como subagente de dominio.

## Decisión 3 — Mecanismo técnico: `skills:` en el frontmatter del agent

Un subagente (`agents/*.md`) puede declarar `skills:` con una lista de nombres de skill, y
Claude Code inyecta el contenido completo de cada una en el contexto del subagente al
arrancar. **Este campo no está limitado a skills del mismo plugin** — puede referenciar
cualquier skill disponible en la sesión, venga de otro plugin o esté suelta en
`~/.claude/skills/` o `.claude/skills/`. Esto es lo que permite que `axxon-dataverse-agent`
sea un plugin liviano que no necesita duplicar el contenido de `axxon-dataverse-architect` ni
de las skills de presales/delivery.

## Decisión 4 — Repositorio separado, no dentro de Axxon Dataverse Architect

`axxon-dataverse-agent` vive en su **propio repo**, no dentro del de Axxon Dataverse
Architect. Razón: este supraagente está por encima de todos los plugins de Axxon (Dataverse
Architect es uno de varios subagentes que comanda), meterlo adentro de uno de ellos invertiría
la relación de dependencia. `plugin.json` de `axxon-dataverse-agent` declara
`axxon-dataverse-architect` como dependencia (campo `dependencies`) — cuando alguien instala
el supraagente, Claude Code puede requerir/habilitar automáticamente ese plugin también.

---

## Consecuencias

**Actualización v0.2.0 — resuelto:** los tres subagentes son ahora 100% portables. `axxon-sprint0-suite`
y `axxon-delivery-suite` ya existen como plugins reales (ver sus repos separados), y
`plugin.json` de `axxon-dataverse-agent` los declara como `dependencies` junto a
`axxon-dataverse-architect`. La limitación de portabilidad descripta originalmente en esta
sección ya no aplica.

## Pendiente para las próximas iteraciones

- Empaquetar `licensing-analyser`, `rfp-manager`, `d365crm-resoruces-estimator` como plugin
  propio (etapa de presales anterior a Sprint 0) si en algún momento se retoma esa etapa como
  parte del supraagente — hoy queda deliberadamente fuera.
- Empaquetar `ado-connector` como módulo compartido real entre `ado-daily-prep` y
  `ado-us-planner` (hoy cada una tiene su propia implementación duplicada) — refactor, no
  bloqueante.
- Resolver el rework de `output-formatter` (pendiente de otro proyecto) antes de sumarlo acá.
