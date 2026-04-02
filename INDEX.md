# Budget Agent - Project Index

## 📚 Documentation Files

- **[README.md](README.md)** - Complete project overview and features
- **[QUICKSTART.md](QUICKSTART.md)** - 5-minute setup guide
- **[ARCHITECTURE.md](ARCHITECTURE.md)** - System design and data flow
- **[DEVELOPMENT.md](DEVELOPMENT.md)** - Developer guide and best practices

## 🏗️ Source Code Structure

### Configuration
- **[src/config.py](src/config.py)** - Environment configuration and settings

### Database Layer (`src/db/`)
- **[src/db/connection.py](src/db/connection.py)** - SQLite connection management
- **[src/db/models.py](src/db/models.py)** - CRUD operations (40+ operations)
  - `create_expense()` / `get_all_expenses()` - Fixed expenses
  - `create_income()` / `get_all_incomes()` - Income sources
  - `create_task()` / `get_all_tasks()` - Budget tasks
  - `create_partial_payment()` / `get_all_partial_payments()` - Payments
  - `get_summary()` - Financial overview

### Agent Layer (`src/agent/`)
- **[src/agent/budget_agent.py](src/agent/budget_agent.py)** - Claude API integration
  - `BudgetAgent` class with tool use support
  - Conversation history management
  - Tool execution loop

### Tools Layer (`src/tools/`)
- **[src/tools/__init__.py](src/tools/__init__.py)** - Agent tool definitions
  - 9 tools for expense, income, task, and data retrieval
  - `process_tool()` handler for all tools

### CLI Layer (`src/cli/`)
- **[src/cli/main.py](src/cli/main.py)** - Interactive terminal interface
  - Rich terminal UI with tables
  - Commands: summary, expenses, incomes, tasks
  - Agent conversation loop

## 🧪 Testing

- **[tests/test_db.py](tests/test_db.py)** - Database operation tests
  - Tests for create_expense, create_income, get_summary

## 📝 Examples

- **[example_usage.py](example_usage.py)** - Programmatic usage examples
  - Direct database operations
  - Agent interaction
  - Direct tool usage

## ⚙️ Configuration Files

- **[pyproject.toml](pyproject.toml)** - Project metadata and dependencies
- **[.env.example](.env.example)** - Environment variables template
- **[.gitignore](.gitignore)** - Git ignore patterns

## 🎯 Key Features

### Database Schema
```
4 tables:
├─ gastos_fijos (fixed expenses)
├─ pagos_parciales (partial payments)
├─ tareas (tasks)
└─ ingresos (income sources)
```

### Agent Tools (9 total)
```
Expense: add_expense, record_payment
Income: add_income
Tasks: add_task, complete_task
Query: get_budget_summary, list_expenses, list_incomes, list_tasks
```

### CLI Commands
```
summary    - Budget overview
expenses   - List expenses
incomes    - List income
tasks      - Pending tasks
help       - Show help
exit       - Quit
```

## 🚀 Quick Start

```bash
# Setup
python -m venv venv
source venv/bin/activate
pip install -e .

# Configure
cp .env.example .env
# Add your ANTHROPIC_API_KEY to .env

# Run
python -m src.cli.main
```

## 📊 Architecture Summary

```
CLI ↔ BudgetAgent ↔ Claude API
 ↓       ↓
DB ← Tools
```

**5 layers:**
1. CLI - User interface (Rich)
2. Config - Settings management
3. Agent - Claude integration
4. Tools - Capability definitions
5. DB - Data persistence (SQLite)

## 🔧 Modular Design

- **Independent modules** - Each can be tested/used separately
- **Clear interfaces** - Well-defined input/output
- **Easy extension** - Add features by following patterns
- **Single responsibility** - Each module has one job

## 📈 Project Statistics

- **Files**: 18 total
- **Python modules**: 12
- **Database tables**: 4
- **Agent tools**: 9
- **CLI commands**: 6
- **Lines of code**: ~600 (excluding comments)

## 🎓 Learning Path

1. Start with **QUICKSTART.md** to run the app
2. Read **README.md** for full overview
3. Check **ARCHITECTURE.md** to understand design
4. Review **DEVELOPMENT.md** to extend features
5. Study **src/** modules in order:
   - config.py (settings)
   - db/ (data layer)
   - tools/ (capabilities)
   - agent/ (AI integration)
   - cli/ (interface)

## 💡 Example Conversations

```
You: Add monthly expense of $1200 for rent
Agent: I've added 'Rent' as a monthly expense...

You: What's my balance?
Agent: Based on your income and expenses...

You: List my expenses
Agent: Here are your active expenses...

You: Create a task to review budget
Agent: Task created with status 'pendiente'...

You: summary
(Shows formatted table with summary)
```

## 🔗 Module Dependencies

```
cli/main.py
├── config.py
├── agent/budget_agent.py
│   ├── tools/__init__.py
│   │   └── db/models.py
│   │       └── db/connection.py
│   └── config.py
└── db/models.py
    └── db/connection.py
```

## 📋 Checklist for Use

- [ ] Copy .env.example to .env
- [ ] Add ANTHROPIC_API_KEY
- [ ] Install dependencies (`pip install -e .`)
- [ ] Run: `python -m src.cli.main`
- [ ] Try a command: `summary`
- [ ] Ask agent something: `Add monthly income of $3000`
- [ ] Check results: `summary`

## 🎯 Next Steps

### To Extend:
1. Add new database table → See DEVELOPMENT.md
2. Add new tool → See src/tools/__init__.py
3. Add CLI command → See src/cli/main.py
4. Add test → See tests/test_db.py

### To Use:
1. Read QUICKSTART.md
2. Run `python -m src.cli.main`
3. Start budgeting with AI assistance!

---

**Created with Claude Code** ✨
