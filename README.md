# Budget Agent 💰

An AI-powered personal budget assistant using Claude API and SQLite.

## Features

- 🤖 **AI-Powered**: Uses Claude with tool use for intelligent budget management
- 📊 **Budget Tracking**: Fixed expenses, variable payments, income sources
- ✅ **Task Management**: Budget-related tasks and reminders
- 💾 **SQLite Database**: Persistent storage with 4 main tables
- 🎯 **Natural Language**: Talk to your budget in natural language
- 📈 **Analytics**: Monthly summaries and financial insights

## Project Structure

```
budget-agent/
├── src/
│   ├── __init__.py
│   ├── config.py              # Configuration management
│   ├── db/                    # Database layer
│   │   ├── connection.py      # SQLite connection
│   │   └── models.py          # CRUD operations
│   ├── tools/                 # Agent tools
│   │   └── __init__.py        # Tool definitions
│   ├── agent/                 # AI Agent
│   │   └── budget_agent.py    # Claude agent with tool use
│   └── cli/                   # CLI interface
│       └── main.py            # Main entry point
├── tests/                     # Test suite
├── data/                      # SQLite database (created at runtime)
├── pyproject.toml             # Project configuration
├── .env.example               # Environment template
└── README.md
```

## Database Schema

### gastos_fijos (Fixed Expenses)
```sql
id, nombre, monto, frecuencia, descripcion, estado, fecha_creacion, fecha_actualizacion
```

### pagos_parciales (Partial Payments)
```sql
id, gasto_id, monto, fecha_pago, descripcion, metodo_pago, fecha_creacion
```

### tareas (Tasks)
```sql
id, descripcion, estado, prioridad, monto_asociado, fecha_vencimiento, fecha_creacion, fecha_actualizacion
```

### ingresos (Income)
```sql
id, descripcion, monto, frecuencia, fuente, estado, fecha_creacion, fecha_actualizacion
```

## Installation

1. **Clone or create the project**:
```bash
cd budget-agent
```

2. **Create virtual environment**:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**:
```bash
pip install -e .
```

4. **Configure environment**:
```bash
cp .env.example .env
# Edit .env and add your ANTHROPIC_API_KEY
```

5. **Run the CLI**:
```bash
python -m src.cli.main
```

Or if the script entry point is installed:
```bash
budget-agent
```

## Usage

### Interactive Mode

Start the interactive CLI:
```bash
python -m src.cli.main
```

### Available Commands

- **summary** - Show budget summary
- **expenses** - List all fixed expenses
- **incomes** - List all income sources
- **tasks** - Show pending tasks
- **help** - Show help message
- **exit** - Exit program

### Natural Language Examples

Ask the agent anything about your budget:

```
You: Add a monthly expense of $1200 for rent
Agent: I'll add rent as a monthly expense...

You: What's my current balance?
Agent: Based on your income and expenses...

You: Record a payment of $500 for expense 1
Agent: Payment recorded successfully...

You: Create a reminder to pay bills by Friday
Agent: Task created...

You: Show me my financial summary
Agent: Here's your budget overview...
```

## Agent Tools

The agent has access to these tools:

1. **add_expense** - Add fixed expenses
2. **add_income** - Add income sources
3. **record_payment** - Record partial payments
4. **add_task** - Create budget tasks
5. **get_budget_summary** - Get financial summary
6. **list_expenses** - List all expenses
7. **list_incomes** - List all incomes
8. **list_tasks** - List pending tasks
9. **complete_task** - Mark tasks as completed

## Architecture

### Modular Design

- **Config Layer**: Centralized configuration
- **DB Layer**: SQLite abstractions with CRUD operations
- **Tools Layer**: Agent tool definitions and processing
- **Agent Layer**: Claude integration with tool use
- **CLI Layer**: Rich terminal UI

### Tool Use Flow

```
User Input
    ↓
CLI/Agent
    ↓
Claude API (with tools)
    ↓
Tool Processing (add_expense, record_payment, etc.)
    ↓
Database Updates
    ↓
Response to User
```

## Development

### Running Tests

```bash
pytest tests/
```

### Adding New Features

1. **New Database Feature**: Add model in `src/db/models.py`
2. **New Agent Tool**: Define in `src/tools/__init__.py`
3. **New CLI Command**: Add in `src/cli/main.py`

### File Organization

Keep these principles:
- **Separation of Concerns**: DB, Agent, CLI are independent
- **Reusability**: Tools can be used by any interface
- **Testability**: Each module has clear responsibilities

## Environment Variables

```
ANTHROPIC_API_KEY=sk-ant-...
DATABASE_PATH=./data/budget.db
LOG_LEVEL=INFO
```

## License

MIT

## Author

Created with Claude Code
