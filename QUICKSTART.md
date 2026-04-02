# Quick Start Guide

## 5-Minute Setup

### 1. Install Dependencies
```bash
cd budget-agent
python -m venv venv
source venv/bin/activate
pip install -e .
```

### 2. Setup API Key
```bash
cp .env.example .env
# Edit .env and add your ANTHROPIC_API_KEY (get from claude.ai/code)
```

### 3. Run the Agent
```bash
python -m src.cli.main
```

## First Steps in CLI

```
You: help
# See available commands

You: summary
# View your budget overview (empty at first)

You: Add a monthly expense of $1200 for rent
# Use natural language to interact with the agent!

You: Add a monthly income of $3000 from my salary
# Agent will record it

You: What's my balance?
# Agent analyzes and tells you

You: expenses
# See list of expenses

You: exit
# Quit the app
```

## What You Can Do

### Natural Language Queries
- "Add an expense for $50 for groceries"
- "Record a payment of $200 for rent"
- "What's my financial situation?"
- "Create a task to pay bills by Friday"
- "Show me my summary"

### Built-in Commands
```
summary   → Budget overview
expenses  → List all expenses
incomes   → List all incomes  
tasks     → Show pending tasks
help      → Show this help
exit      → Quit
```

## Project Structure

```
src/
├── db/           # Database operations
├── agent/        # Claude integration
├── tools/        # Agent capabilities
└── cli/          # User interface
```

## API Requirements

- Claude API key (free tier available)
- Python 3.11+
- ~50MB disk space

## Next Steps

- Read [README.md](README.md) for full documentation
- Check [src/agent/budget_agent.py](src/agent/budget_agent.py) to understand tool use
- Modify tools in [src/tools/__init__.py](src/tools/__init__.py) to add features
- Extend database in [src/db/models.py](src/db/models.py)

Enjoy your AI budget assistant! 🚀
