# Contrato ADO — coordinación entre agentes y roles

**Versión:** 1.0 · **Fecha:** 2026-11-04 · **Decisión:** ADR-005 (este repo)

Los agentes de Axxon **no se hablan entre sí**: se coordinan a través del Azure DevOps del
proyecto. Este documento es la **única fuente de verdad** de qué escribe y qué lee cada agente
en los work items. Toda skill que lea o escriba work items (delivery-suite, sprint0-suite,
dataverse-architect) tiene que respetarlo — si una skill necesita algo que no está acá, se
agrega acá primero.

---

## 1. Premisas

- **La unidad de trabajo es la User Story funcional.** Su dueño es el consultor funcional /
  customizador. Se encara siempre desde la óptica funcional.
- **El pro-code es una Task hija** de esa User Story, que toma un dev — no una User Story
  aparte.
- **Historia técnica pura** (frameworks compartidos, pipelines, infra, refactor): User Story
  con tag `us-tecnica`, dueño el tech lead. Es la excepción, no la regla.
- Funciona con cualquier process template (Agile, Scrum, Basic, CMMI): **los tags son la
  señal principal**, y el tipo de requerimiento, el campo de esfuerzo y los estados salen del
  mapeo de la §9 según el `Proceso` declarado en `.d365-project.md`. Nunca se asume Agile.
- En este contrato, "User Story" / "US" significa **el requerimiento** del proceso (User
  Story, Product Backlog Item, Issue o Requirement — §9).

## 2. Roles

| Rol | Qué hace | Agentes / skills principales |
|---|---|---|
| **Funcional** | Dueño de la User Story: refinamiento, plan, validación de los AC | `sprint0-analyst`, `delivery-manager` (`ado-us-planner`) |
| **Customizador** | Construye la parte low-code (puede ser la misma persona que el Funcional) | `dataverse-builder` (low-code) |
| **Dev** | Construye la parte pro-code | `delivery-manager` (`ado-dev-queue`) → `dataverse-builder` (pro-code) |
| **Tech lead** | Aprueba la parte pro-code del plan, ADRs, revisa PRs, dueño de las `us-tecnica` | `build-approach-advisor`, `adr-recorder` |
| **PM** | Seguimiento, daily, bloqueos | `delivery-manager` (`ado-daily-prep`) |

**Cómo sabe el agente el rol de quien lo usa:** sección `## Equipo` de `.d365-project.md`
(persona → rol). Si la persona no está, el agente pregunta el rol **una vez por sesión** y no
lo vuelve a preguntar.

## 3. Tags

| Tag | Dónde | Quién lo pone | Significado |
|---|---|---|---|
| `fit-gap-{fully-covered\|partially-covered\|not-covered}` | US | `backlog-refiner` | Clasificación de cobertura (ya existente) |
| `procode-candidato` | US | `backlog-refiner` | **Hipótesis** de Fase 1: probablemente requiere pro-code. No es una decisión |
| `us-tecnica` | US | Tech lead / `backlog-refiner` | Historia técnica pura |
| `plan-aprobado` | US | `ado-us-planner` | El Plan de construcción completo está aprobado (Puerta 1), incluida la aprobación del tech lead si hay pro-code |
| `build-lowcode` | Task | `ado-us-planner` | Construcción low-code (cola del customizador) |
| `build-procode` | Task | `ado-us-planner` | Construcción pro-code (cola del dev) |
| `comp-{componente}` | Task | `ado-us-planner` | Componente: `comp-table`, `comp-form`, `comp-view`, `comp-br`, `comp-flow`, `comp-security`, `comp-plugin`, `comp-customapi`, `comp-function`, `comp-logicapp`, `comp-config` |

Reglas: tags en minúscula, sin `#`. Los agentes **agregan** tags preservando los existentes
(el campo `System.Tags` se reescribe completo: leer → agregar → escribir, separados por `; `).

## 4. Comentarios estructurados

Los handoffs viven en comentarios de work item (formato Markdown). La **primera línea** es un
marcador que los agentes buscan con `wit_work_item` action `list_comments`:

| Marcador | Dónde | Quién lo escribe | Contenido |
|---|---|---|---|
| `[axx:plan-construccion v1]` | US | `ado-us-planner` | Plan de construcción de `build-approach-advisor` (tabla por necesidad, piezas pro-code, supuestos), quién lo aprobó y fecha |
| `[axx:aprobacion-procode v1]` | US | `ado-us-planner`, a pedido del tech lead | "Aprobado por {tech lead} — {fecha}" + observaciones |
| `[axx:contrato-tecnico v1]` | Task pro-code | `ado-us-planner` | Qué construir exactamente: Plugin (mensaje, entidad, etapa, modo, filtering attributes, images), Custom API (nombre, parámetros in/out), Function (trigger, entrada/salida, sistema externo) |
| `[axx:handoff v1]` | Task | Quien termina una Task de la que dependen otras | Qué quedó hecho y qué necesita saber el siguiente (ej. logical names creados) |
| `[axx:resultado v1]` | Task pro-code | `dataverse-builder` | Rama, PR, tests, estado del registro/deploy en DEV |

Si hay más de un comentario con el mismo marcador, **vale el más reciente**. Un comentario
nunca se edita para cambiar una decisión: se agrega uno nuevo.

## 5. Tasks

- **Título:** prefijo `[LC]` (low-code) o `[PC]` (pro-code) + acción. Ej. `[PC] Plugin
  ConsultarBureau (Update axx_creditsolicitud, async)`.
- **Asignación:** las `build-lowcode` se asignan al customizador al crearlas. Las
  `build-procode` se crean **sin asignar**: el dev las toma desde `ado-dev-queue`.
- **Estimación:** `Microsoft.VSTS.Scheduling.RemainingWork` (horas) siempre; además
  `OriginalEstimate` solo en Agile y CMMI (en Scrum y Basic la Task no lo tiene — §9).
- **Dependencias:** link `predecessor`/`successor` entre Tasks (ej. `[LC] Crear tabla` →
  predecesora de `[PC] Plugin sobre la tabla`). Antes de empezar una Task, el agente verifica
  que sus predecesoras estén cerradas; si no, avisa y no arranca sin confirmación.
- **Campo `Activity`:** ⏸️ **decisión abierta**. Existe en Agile y Scrum; CMMI usa
  `Discipline`; Basic no tiene ninguno (§9). Hasta resolverla, los agentes **no** lo
  escriben; las colas y reportes usan tags.

## 6. Código y decisiones

- Rama: `feature/US-{usId}-{slug}` (`code-repo-manager`). Una por User Story — si varios devs
  trabajan la misma US, cada uno en una rama por Task: `feature/US-{usId}-T{taskId}-{slug}`.
- Commits: `AB#{taskId}` en el mensaje.
- PR: `workItems` = `"{taskId} {usId}"` (string separado por espacio).
- ADRs: wiki de proyecto (`adr-recorder`), link a la US.

## 7. Estados

| Work item | Quién lo mueve | Cuándo |
|---|---|---|
| US → en curso (`Active`/`Committed`/`Doing`) | Funcional (`ado-us-planner`) | Al aprobar el plan y crear las Tasks |
| Task → en curso | Quien la toma | Al empezar |
| Task low-code → cerrada | Customizador | Construida y verificada en DEV |
| Task pro-code → cerrada | Dev | PR mergeado + registro/deploy en DEV verificado |
| US → resuelta (`Resolved`/`Done`) | Funcional | AC Gherkin validados en DEV y todas las Tasks cerradas |

Los nombres exactos de estado salen de la §9 según el proceso — nunca se escriben a ciegas.
Para **filtrar** abiertos/cerrados en WIQL, `[System.State] NOT IN ('Closed', 'Done',
'Removed', 'Resolved')` funciona con los cuatro procesos (los estados que no existen en un
proceso simplemente no matchean).

## 8. Lo que ningún agente hace

- Mover una US a resuelta sin que el Funcional valide los AC.
- Asignar una Task pro-code a un dev que no la tomó.
- Marcar `plan-aprobado` sin aprobación explícita (y del tech lead, si hay pro-code).
- Borrar work items, tags ajenos o comentarios.
- Pedir o guardar PATs: el acceso es vía el servidor MCP oficial de Azure DevOps.

## 9. Process template (Agile, Scrum, Basic, CMMI)

Se declara en `.d365-project.md` → `## Azure DevOps` → `- Proceso: {Agile | Scrum | Basic |
CMMI}` (se ve en ADO → Project settings → Process). Si falta, el agente lo pregunta antes de
**escribir** work items y sugiere agregarlo al archivo. Las **lecturas** no lo necesitan.

| | Agile | Scrum | Basic | CMMI |
|---|---|---|---|---|
| **Tipo de requerimiento** | User Story | Product Backlog Item | Issue | Requirement |
| **Campo de esfuerzo** | `Microsoft.VSTS.Scheduling.StoryPoints` | `Microsoft.VSTS.Scheduling.Effort` | `Microsoft.VSTS.Scheduling.Effort` ⚠️ | `Microsoft.VSTS.Scheduling.Size` |
| **Estados del requerimiento** | New, Active, Resolved, Closed, Removed | New, Approved, Committed, Done, Removed | To Do, Doing, Done | Proposed, Active, Resolved, Closed |
| **"En curso" del requerimiento** | Active | Committed | Doing | Active |
| **"Resuelto" del requerimiento** | Resolved | Done | Done | Resolved |
| **Retirar sin borrar** | Removed | Removed | (no hay) → tag `reemplazada-fase1` + comentario | Closed |
| **Estimación de la Task** | Original Estimate, Remaining Work, Completed Work | Remaining Work | Remaining Work | Original Estimate, Remaining Work, Completed Work |
| **Disciplina de la Task** | `Activity` | `Activity` | — | `Discipline` |

**Reglas:**
- **Consultas:** usar `[System.WorkItemType] IN GROUP 'Microsoft.RequirementCategory'` en vez
  del nombre del tipo — funciona con cualquier proceso, incluso customizado.
- **Lectura de esfuerzo:** el primero con valor entre StoryPoints, Effort y Size.
- **Estados de la Task:** no se escriben de memoria; se toman del proyecto (leyendo una Task
  existente) o se preguntan una vez.
- **Procesos heredados customizados:** el mapeo vale para el proceso base; si el proyecto
  renombró tipos o estados, el agente lo detecta al primer error y pregunta.
- Scripts Python: `process_map.py` (vendorizado en cada carpeta `scripts/`) implementa esta
  tabla; los que escriben work items exigen `--process` (o `ADO_PROCESS`).

Fuentes (Microsoft Learn, verificadas 2026-11-04): *Default processes and process templates*
(tipos, estados, estimación de Task) y *Query by numeric fields* (StoryPoints = Agile,
Effort = Scrum, Size = CMMI, Activity = Agile/Scrum, Discipline = CMMI). ⚠️ Basic + Effort:
observado en un proyecto real, no figura en esas páginas — verificar.
