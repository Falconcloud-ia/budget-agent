#!/usr/bin/env python
"""
Example of using budget-agent programmatically.
This demonstrates the modular design where you can use
the agent without the CLI.
"""

import sys
from src.db import init_db, get_summary, get_all_expenses
from src.agent import BudgetAgent


def example_direct_db():
    """Example 1: Direct database usage without agent."""
    print("=" * 50)
    print("Example 1: Direct Database Operations")
    print("=" * 50)

    from src.db import create_expense, create_income

    # Add some test data
    create_income(
        descripcion="Monthly Salary",
        monto=3500.00,
        frecuencia="mensual",
        fuente="Employment"
    )

    create_expense(
        nombre="Rent",
        monto=1200.00,
        frecuencia="mensual",
        descripcion="Apartment rent"
    )

    create_expense(
        nombre="Utilities",
        monto=150.00,
        frecuencia="mensual",
        descripcion="Electric, water, internet"
    )

    # Get summary
    summary = get_summary()
    print(f"\nBudget Summary:")
    print(f"  Monthly Income: ${summary['monthly_income']:.2f}")
    print(f"  Monthly Expenses: ${summary['monthly_expenses']:.2f}")
    print(f"  Balance: ${summary['balance']:.2f}")
    print()


def example_agent_interaction():
    """Example 2: Using the agent with natural language."""
    print("=" * 50)
    print("Example 2: Agent Interaction")
    print("=" * 50)

    agent = BudgetAgent()

    # Example queries
    queries = [
        "Show me my current budget summary",
        "List all my expenses",
        "Create a task to review my budget this week"
    ]

    for query in queries:
        print(f"\nUser: {query}")
        response = agent.chat(query)
        print(f"Agent: {response}")
        print()


def example_tools_directly():
    """Example 3: Using tools directly."""
    print("=" * 50)
    print("Example 3: Direct Tool Usage")
    print("=" * 50)

    from src.tools import process_tool
    import json

    # Create an expense using tool
    tool_input = {
        "nombre": "Groceries",
        "monto": 300.00,
        "frecuencia": "mensual",
        "descripcion": "Weekly groceries"
    }

    result = process_tool("add_expense", tool_input)
    result_data = json.loads(result)

    print(f"Result: {result_data}")
    print()


def main():
    """Run examples."""
    print("\n🚀 Budget Agent Examples\n")

    try:
        # Initialize database
        init_db()

        # Run examples
        example_direct_db()
        example_agent_interaction()
        example_tools_directly()

        # Show final summary
        print("=" * 50)
        print("Final Summary")
        print("=" * 50)

        summary = get_summary()
        expenses = get_all_expenses()

        print(f"\nTotal Expenses Tracked: {len(expenses)}")
        print(f"Total Monthly Income: ${summary['monthly_income']:.2f}")
        print(f"Total Monthly Expenses: ${summary['monthly_expenses']:.2f}")
        print(f"Monthly Balance: ${summary['balance']:.2f}")

        print("\n✅ Examples completed successfully!")

    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    main()
