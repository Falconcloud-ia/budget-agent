# Development Guide

## Architecture Overview

### Module Responsibilities

**src/config.py**
- Loads environment variables
- Centralizes configuration
- Creates data directory

**src/db/**
- `connection.py`: SQLite connection management
- `models.py`: CRUD operations for all tables
- Schema: 4 main tables (gastos_fijos, pagos_parciales, tareas, ingresos)

**src/tools/**
- Defines 9 agent tools
- `process_tool()` handles tool execution
- Returns JSON results back to agent

**src/agent/**
- `NaamanAgent` class wraps Claude API
- Manages conversation history
- Handles tool use loop
- System prompt for agent behavior

**src/cli/**
- Rich terminal UI
- Commands: summary, expenses, incomes, tasks
- Interactive loop with user input
- Agent integration

## Adding New Features

### Add a Database Table

1. Create migration in `src/db/connection.py`:
```python
cursor.execute("""
CREATE TABLE IF NOT EXISTS nueva_tabla (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    ...
)
""")
```

2. Add CRUD operations in `src/db/models.py`:
```python
def create_nueva(param: str) -> Dict[str, Any]:
    # Implementation
    pass

def get_all_nueva() -> List[Dict[str, Any]]:
    # Implementation
    pass
```

3. Export in `src/db/__init__.py`

### Add an Agent Tool

1. Define in `src/tools/__init__.py`:
```python
{
    "name": "my_tool",
    "description": "What it does",
    "input_schema": {
        "type": "object",
        "properties": {...},
        "required": [...]
    }
}
```

2. Add handler in `process_tool()`:
```python
elif tool_name == "my_tool":
    result = some_function(tool_input["param"])
    return json.dumps({"success": True, "data": result})
```

### Add a CLI Command

1. Create display function in `src/cli/main.py`:
```python
def display_newfeature():
    data = get_newfeature()
    # Use Rich for formatting
    console.print(...)
```

2. Add to command handler:
```python
elif user_input.lower() == "newcommand":
    display_newfeature()
```

## Tool Use Loop

The agent interaction follows this pattern:

```
1. User input → Chat message
2. Claude API called with tools
3. Check response.stop_reason
   - "tool_use": Process tools, loop back to step 2
   - "end_turn": Return text response
4. Display to user
```

## Testing

### Run Tests
```bash
pytest tests/ -v
```

### Add Tests
Create in `tests/test_*.py`:
```python
@patch('src.config.DATABASE_PATH')
def test_something(self, mock_path):
    # Use temp database
    # Test your function
    pass
```

## Database Queries

Common patterns in `src/db/models.py`:

```python
# Connection
conn = get_connection()
cursor = conn.cursor()

# INSERT
cursor.execute("INSERT INTO table (...) VALUES (...)", params)
conn.commit()
id = cursor.lastrowid

# SELECT
cursor.execute("SELECT * FROM table WHERE ...")
rows = [dict(row) for row in cursor.fetchall()]

# UPDATE
cursor.execute("UPDATE table SET ... WHERE ...", params)
conn.commit()
success = cursor.rowcount > 0

# Close
conn.close()
```

## Modular Design Principles

1. **Database Independence**: Models don't know about Agent or CLI
2. **Tool Portability**: Tools work with any interface
3. **Configuration Centralization**: All config in one place
4. **Clear Contracts**: Each module has clear input/output

## Environment Setup for Development

```bash
# Virtual environment
python -m venv venv
source venv/bin/activate

# Editable install with test dependencies
pip install -e ".[dev]"  # if dev extras are added

# Run with debug
PYTHONDEBUG=1 python -m src.cli.main

# Test with coverage
pytest --cov=src tests/
```

## Debugging Tips

### Enable Logging
```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

### Test Database Operations
```bash
sqlite3 data/budget.db ".schema"
sqlite3 data/budget.db "SELECT * FROM gastos_fijos;"
```

### Test Agent Directly
```python
from src.agent import NaamanAgent
agent = NaamanAgent()
response = agent.chat("Add a monthly expense of $1000")
print(response)
```

## Performance Considerations

- Database queries are blocking (fine for CLI)
- Consider connection pooling for multi-user
- Agent conversation history grows with use
- Tool processing is fast (local JSON)

## Future Enhancements

- [ ] Web API (FastAPI)
- [ ] Data export (CSV, PDF)
- [ ] Recurring transaction automation
- [ ] Budget forecasting
- [ ] Multi-user support
- [ ] Expense categories
- [ ] Budget goals/targets
