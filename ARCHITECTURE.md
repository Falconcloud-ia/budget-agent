# Architecture Document

## High-Level Architecture

```
┌─────────────────────────────────────────────────────────┐
│                    CLI Interface                         │
│  (Rich Terminal UI with commands and agent interaction)  │
└──────────────────┬──────────────────────────────────────┘
                   │
                   ├─────────────────────┬──────────────────┐
                   ▼                     ▼                  ▼
         ┌────────────────┐    ┌──────────────────┐  ┌──────────┐
         │ Naaman Agent   │    │  Direct DB Calls │  │ Commands │
         │ (Claude API)   │    │                  │  │ (summary,│
         └────────┬───────┘    └────────┬─────────┘  │ expenses)│
                  │                     │             └──────────┘
                  └─────────────┬───────┘
                                ▼
                        ┌─────────────────┐
                        │  Database Layer │
                        │  (CRUD Ops)     │
                        └────────┬────────┘
                                 ▼
                        ┌─────────────────┐
                        │  SQLite DB      │
                        │  (4 tables)     │
                        └─────────────────┘
```

## Module Dependencies

```
┌─────────────────────────────────────────────────────────┐
│                    src/cli/main.py                       │
│                  (User Interface)                        │
└─────────────────────────────────────────────────────────┘
           ▲                              ▲
           │                              │
    ┌──────┴───────┐            ┌────────┴─────────┐
    ▼              ▼            ▼                  ▼
┌─────────────┐ ┌──────────┐ ┌──────────────┐ ┌──────────┐
│   Agent     │ │Database  │ │ Commands     │ │  Config  │
│(tool use)   │ │(models)  │ │(summary,...) │ │(env vars)│
└──────┬──────┘ └────┬─────┘ └──────────────┘ └──────────┘
       ▲             ▲
       │             │
    ┌──┴─────────────┴──┐
    ▼                   ▼
┌─────────────┐    ┌──────────┐
│ Tools       │    │Connection│
│(definitions)│    │(SQLite)  │
└─────────────┘    └──────────┘
```

## Data Flow: User Interaction

```
┌─────────────────────────────────────────────────────────────┐
│ 1. User Input                                               │
│    "Add monthly expense of $1200 for rent"                  │
└──────────────────────┬────────────────────────────────────┘
                       ▼
┌─────────────────────────────────────────────────────────────┐
│ 2. CLI receives input                                        │
│    Check if command or send to agent                        │
└──────────────────────┬────────────────────────────────────┘
                       ▼
┌─────────────────────────────────────────────────────────────┐
│ 3. NaamanAgent.chat(message)                                │
│    - Add to conversation history                            │
│    - Send to Claude with tools                              │
└──────────────────────┬────────────────────────────────────┘
                       ▼
┌─────────────────────────────────────────────────────────────┐
│ 4. Claude Response (tool_use)                               │
│    - Tool name: "add_expense"                               │
│    - Tool input: {nombre, monto, frecuencia, descripcion}   │
└──────────────────────┬────────────────────────────────────┘
                       ▼
┌─────────────────────────────────────────────────────────────┐
│ 5. process_tool("add_expense", input)                       │
│    - Extract parameters                                     │
│    - Call create_expense()                                  │
└──────────────────────┬────────────────────────────────────┘
                       ▼
┌─────────────────────────────────────────────────────────────┐
│ 6. Database Operation                                       │
│    - INSERT INTO gastos_fijos (...)                         │
│    - Return JSON result                                     │
└──────────────────────┬────────────────────────────────────┘
                       ▼
┌─────────────────────────────────────────────────────────────┐
│ 7. Tool Result back to Agent                                │
│    {"success": true, "data": {id: 1, nombre: "Rent", ...}}  │
└──────────────────────┬────────────────────────────────────┘
                       ▼
┌─────────────────────────────────────────────────────────────┐
│ 8. Claude Generates Response                                │
│    Interprets tool result and creates human-friendly text   │
└──────────────────────┬────────────────────────────────────┘
                       ▼
┌─────────────────────────────────────────────────────────────┐
│ 9. Agent returns final text                                 │
│    "I've added 'Rent' as a monthly expense of $1200..."     │
└──────────────────────┬────────────────────────────────────┘
                       ▼
┌─────────────────────────────────────────────────────────────┐
│ 10. CLI displays response                                    │
│     User sees formatted output                              │
└─────────────────────────────────────────────────────────────┘
```

## Database Schema

```
┌─────────────────────────────────────────────────────────┐
│                    SQLite Database                      │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  gastos_fijos (Fixed Expenses)                         │
│  ├─ id (PK)                                            │
│  ├─ nombre                                             │
│  ├─ monto                                              │
│  ├─ frecuencia (mensual, trimestral, anual, semanal)  │
│  ├─ descripcion                                        │
│  ├─ estado (activo/inactivo)                           │
│  └─ timestamps                                         │
│                                                         │
│  pagos_parciales (Partial Payments) ──┐               │
│  ├─ id (PK)                            │               │
│  ├─ gasto_id (FK) ──────────────────────┘               │
│  ├─ monto                                              │
│  ├─ fecha_pago                                         │
│  ├─ metodo_pago                                        │
│  └─ timestamps                                         │
│                                                         │
│  tareas (Tasks)                                        │
│  ├─ id (PK)                                            │
│  ├─ descripcion                                        │
│  ├─ estado (pendiente/completada)                      │
│  ├─ prioridad (baja/media/alta)                        │
│  ├─ monto_asociado                                     │
│  ├─ fecha_vencimiento                                  │
│  └─ timestamps                                         │
│                                                         │
│  ingresos (Income Sources)                             │
│  ├─ id (PK)                                            │
│  ├─ descripcion                                        │
│  ├─ monto                                              │
│  ├─ frecuencia (mensual, trimestral, anual, semanal)  │
│  ├─ fuente (Employment, Freelance, etc.)               │
│  ├─ estado (activo/inactivo)                           │
│  └─ timestamps                                         │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

## Tool Definitions (9 Tools)

```
┌──────────────────────────────────────────────────────────┐
│                    Agent Tools                           │
├──────────────────────────────────────────────────────────┤
│                                                          │
│  Expense Management                                      │
│  ├─ add_expense                                          │
│  └─ record_payment                                       │
│                                                          │
│  Income Management                                       │
│  └─ add_income                                           │
│                                                          │
│  Task Management                                         │
│  ├─ add_task                                             │
│  └─ complete_task                                        │
│                                                          │
│  Data Retrieval                                          │
│  ├─ get_budget_summary                                   │
│  ├─ list_expenses                                        │
│  ├─ list_incomes                                         │
│  └─ list_tasks                                           │
│                                                          │
└──────────────────────────────────────────────────────────┘
```

## Modular Organization

```
src/
│
├─ config.py ─────────────────────┐ Configuration & Env
│                                 │ Variables
├─ db/
│  ├─ connection.py ─────┐        │ Database Layer
│  ├─ models.py ─────────┼─ CRUD ├─ Schema & Operations
│  └─ __init__.py ───────┘        │
│
├─ tools/
│  └─ __init__.py ───────────────┬─ Tool Definitions
│                                 │ & Processor
├─ agent/
│  └─ budget_agent.py ───────────┬─ Claude Integration
│                                 │ Tool Use Loop
├─ cli/
│  ├─ main.py ───────────────────┬─ Terminal Interface
│  └─ __init__.py ───────────────┴─ Rich UI
│
└─ __init__.py ─────────────────── Package Init
```

## Design Principles

### 1. Separation of Concerns
- **DB Layer**: Only data operations
- **Tools**: Only tool definitions and processing
- **Agent**: Only Claude API interaction
- **CLI**: Only user interface

### 2. Modularity
- Each module has one responsibility
- Clear inputs and outputs
- Reusable by different interfaces

### 3. Testability
- Mock database with temp files
- Independent module tests
- No tight coupling

### 4. Configuration
- Centralized in config.py
- Environment-based
- Easy to change

## Extension Points

### Add New Feature
```
1. Define DB schema → connection.py
2. Add CRUD operations → models.py
3. Define agent tool → tools/__init__.py
4. Add CLI command → cli/main.py
```

### Example: Add Budget Categories
```python
# 1. Schema
CREATE TABLE IF NOT EXISTS categorias (...)

# 2. CRUD
def create_category(...): ...
def get_categories(): ...

# 3. Tool
{
    "name": "add_category",
    "description": "...",
    "input_schema": {...}
}

# 4. CLI
elif user_input == "categories":
    display_categories()
```

## Performance Characteristics

| Operation | Complexity | Notes |
|-----------|-----------|-------|
| Get Summary | O(1) | SUM aggregate queries |
| List Expenses | O(n) | n = expense count |
| Add Expense | O(1) | Single INSERT |
| Agent Chat | O(n) | n = conversation length |
| Tool Processing | O(1) | Simple JSON handling |

## Security Considerations

- SQL parameterized queries (prevent injection)
- API key in environment variable (not hardcoded)
- No sensitive data in logs
- Local SQLite (no network exposure)
- Input validation at tool boundaries

## Future Architecture Improvements

```
Current                          Potential
┌──────────────┐                ┌──────────────┐
│ CLI Only     │     →          │ Multi-UI     │
│ SQLite       │                │ API/Web      │
│ In-Memory    │                │ PostgreSQL   │
└──────────────┘                │ Caching      │
                                └──────────────┘
```
