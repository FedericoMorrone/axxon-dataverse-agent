# Prerequisite — Servidor MCP de Azure DevOps (oficial de Microsoft)

> **Actualizado (2026-08-18, ADR-001 de `axxon-ado-connector`)**: este servidor **dejó de ser
> opcional**. Es la vía estándar para interactuar con Azure DevOps — `backlog-seeder` ya
> depende de él, no de `ado_client.py`. Las 7 skills restantes se migran progresivamente; hasta
> que terminen de migrar, seguí instalando esto de todos modos si vas a usar `backlog-seeder`.

Este documento es un **prerequisito de instalación** para cualquier consultor que vaya a usar
`axxon-dataverse-agent` — en particular `backlog-seeder` (ya migrada) y, a medida que avance
la migración, el resto de las skills que tocan Azure DevOps (`refinement-prep`,
`backlog-refiner`, `fit-gap-rollup`, `effort-recalibration`, `blueprint-builder`,
`ado-daily-prep`, `ado-us-planner`).

## Estado de la migración (ver ADR-001 para el detalle completo)

| Skill | Vía |
|---|---|
| `backlog-seeder` | **Servidor MCP** — migrada, piloto |
| `ado-us-planner`, `ado-daily-prep`, `ado-dev-queue` (nueva) | **Servidor MCP** — migradas 2026-11-04 (delivery-suite v0.3.0) |
| `adr-recorder`, `code-repo-manager` (architect) | **Servidor MCP** (wiki / repos) |
| `refinement-prep`, `backlog-refiner`, `fit-gap-rollup`, `effort-recalibration`, `blueprint-builder` | `ado_client.py` todavía — pendientes de migrar |

`axxon-ado-connector` (el cliente vendorizado) no se retira — queda como fallback para las
skills que todavía no migraron, y como referencia técnica.

## Repo oficial

[`microsoft/azure-devops-mcp`](https://github.com/microsoft/azure-devops-mcp) — MIT license,
mantenido por Microsoft. Verificado contra el repo real al momento de escribir esto (no es
una guía genérica copiada).

## Opción 1 — Servidor remoto (recomendado por Microsoft, sin instalación local)

Microsoft recomienda esta opción por sobre la local — no requiere Node.js ni instalar nada,
corre hosteado por Microsoft. **Para consultores usando Claude Code, esta es la vía más
simple** — confirmado que el comando de Claude Code funciona igual que para VS Code, solo
cambia la sintaxis del comando (ver abajo).

Para VS Code, crear `.vscode/mcp.json`:

```json
{
  "servers": {
    "ado-remote-mcp": {
      "url": "https://mcp.dev.azure.com/{organization}",
      "type": "http"
    }
  },
  "inputs": []
}
```

Reemplazar `{organization}` por la organización de Azure DevOps (ej. `FeMorrone`).

**Para VS Code**: crear `.vscode/mcp.json` con el bloque de arriba.

**Para Claude Code** (confirmado contra `code.claude.com/docs/en/mcp`):

```bash
claude mcp add --transport http azure-devops https://mcp.dev.azure.com/{organization}
```

Después, adentro de Claude Code, correr `/mcp` para completar el login OAuth (se abre el
browser solo) — sin Node.js, sin `npx`, sin descargar ningún paquete. Verificar con
`claude mcp list`.

## Opción 2 — Servidor local (Claude Code)

### Prerequisitos
- [Node.js 20 o superior](https://nodejs.org/en/download).
- Acceso a la organización de Azure DevOps del proyecto.

### Instalación

```bash
claude mcp add --transport stdio azure-devops -- npx -y @azure-devops/mcp {organization}
```

Reemplazar `{organization}` por la organización real (ej. `FeMorrone`). Verificar:

```bash
claude mcp list
```

### Autenticación — usar PAT, por consistencia con el resto del ecosistema

El servidor soporta 5 métodos (interactivo, Azure CLI, credential chain, bearer token env, PAT).
**Recomendado: PAT** (`-a pat`, variable `PERSONAL_ACCESS_TOKEN`) — es el mismo método que ya
usa todo `axxon-ado-connector` (`ADO_PAT`), evita que el consultor tenga que manejar dos
esquemas de autenticación distintos para lo mismo:

```bash
claude mcp add --transport stdio azure-devops -- npx -y @azure-devops/mcp {organization} -a pat
```

Con `PERSONAL_ACCESS_TOKEN` seteado en el entorno — mismo PAT que ya se genera para
`ADO_PAT` (Azure DevOps → Generate Git Credentials, o Personal Access Tokens desde el ícono
de usuario), no hace falta generar uno nuevo separado.

## Fuente

Instrucciones extraídas y verificadas contra:
- `README.md` del repo (secciones "Remote MCP Server" y "Local MCP Server Installation").
- `docs/GETTINGSTARTED.md` (sección "Claude Code", sección "Authentication").
- `code.claude.com/docs/en/mcp` (documentación oficial de Anthropic) — confirma que Claude
  Code soporta `--transport http` para servidores remotos, mismo patrón que la URL de
  Microsoft.

Si Microsoft actualiza el proyecto, estas instrucciones pueden quedar desactualizadas —
revisar el repo directamente si algo no coincide.
