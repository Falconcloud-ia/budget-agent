"""Main CLI entry point."""

import sys
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.prompt import Prompt
from src.db import init_db, get_summary, get_all_expenses, get_all_incomes, get_all_tasks
from src.agent import NaamanAgent

console = Console()


def display_welcome():
    """Display welcome message."""
    welcome_text = """[bold cyan]💰 Naaman - Asistente Financiero[/bold cyan]

Tu asistente financiero y personal, impulsado por Claude.
¡Escribe 'help' para comandos o pregunta cualquier cosa sobre tus finanzas!"""

    console.print(Panel(welcome_text, border_style="cyan"))


def display_summary():
    """Display budget summary."""
    summary = get_summary()

    table = Table(title="📊 Budget Summary", show_header=False)
    table.add_column("Metric", style="cyan")
    table.add_column("Value", style="green")

    table.add_row("Monthly Income", f"${summary['monthly_income']:.2f}")
    table.add_row("Monthly Expenses", f"${summary['monthly_expenses']:.2f}")
    balance = summary['balance']
    balance_style = "green" if balance >= 0 else "red"
    table.add_row(f"[{balance_style}]Balance[/{balance_style}]", f"[{balance_style}]${balance:.2f}[/{balance_style}]")
    table.add_row("Payments (Last 30 days)", f"${summary['recent_payments_30days']:.2f}")
    table.add_row("Pending Tasks", str(summary['pending_tasks']))

    console.print(table)
    console.print()


def display_expenses():
    """Display all expenses."""
    expenses = get_all_expenses()

    if not expenses:
        console.print("[yellow]No expenses registered yet.[/yellow]")
        return

    table = Table(title="📋 Fixed Expenses")
    table.add_column("ID", style="cyan")
    table.add_column("Name", style="magenta")
    table.add_column("Amount", style="green")
    table.add_column("Frequency", style="blue")
    table.add_column("Description")

    for exp in expenses:
        table.add_row(
            str(exp["id"]),
            exp["nombre"],
            f"${exp['monto']:.2f}",
            exp["frecuencia"],
            exp.get("descripcion", "")
        )

    console.print(table)
    console.print()


def display_incomes():
    """Display all incomes."""
    incomes = get_all_incomes()

    if not incomes:
        console.print("[yellow]No incomes registered yet.[/yellow]")
        return

    table = Table(title="💵 Income Sources")
    table.add_column("ID", style="cyan")
    table.add_column("Description", style="magenta")
    table.add_column("Amount", style="green")
    table.add_column("Frequency", style="blue")
    table.add_column("Source")

    for inc in incomes:
        table.add_row(
            str(inc["id"]),
            inc["descripcion"],
            f"${inc['monto']:.2f}",
            inc["frecuencia"],
            inc.get("fuente", "")
        )

    console.print(table)
    console.print()


def display_tasks():
    """Display all pending tasks."""
    tasks = get_all_tasks()

    if not tasks:
        console.print("[yellow]No pending tasks.[/yellow]")
        return

    table = Table(title="✅ Budget Tasks")
    table.add_column("ID", style="cyan")
    table.add_column("Description", style="magenta")
    table.add_column("Priority", style="blue")
    table.add_column("Amount")
    table.add_column("Due Date")

    priority_colors = {"baja": "green", "media": "yellow", "alta": "red"}

    for task in tasks:
        priority = task.get("prioridad", "media")
        color = priority_colors.get(priority, "white")
        table.add_row(
            str(task["id"]),
            task["descripcion"],
            f"[{color}]{priority}[/{color}]",
            f"${task.get('monto_asociado', 0):.2f}" if task.get('monto_asociado') else "-",
            task.get("fecha_vencimiento", "").split()[0] if task.get('fecha_vencimiento') else "-"
        )

    console.print(table)
    console.print()


def display_help():
    """Display help information."""
    help_text = """[bold cyan]Available Commands:[/bold cyan]

  [green]summary[/green]    - Show budget summary
  [green]expenses[/green]   - List all fixed expenses
  [green]incomes[/green]    - List all income sources
  [green]tasks[/green]      - Show pending tasks
  [green]help[/green]       - Show this help message
  [green]exit[/green]       - Exit the program

[bold cyan]Natural Language:[/bold cyan]
  Ask anything about your budget in natural language!
  Examples:
    - "Add a monthly expense of $1200 for rent"
    - "Record a payment of $500 towards expense 1"
    - "What's my monthly balance?"
    - "Create a task to pay bills by Friday"
    - "Show me my financial summary"
"""
    console.print(Panel(help_text, border_style="cyan"))


def main():
    """Main CLI loop."""
    try:
        # Initialize database
        init_db()

        # Display welcome
        display_welcome()

        # Initialize agent
        agent = NaamanAgent()

        console.print("[bold]Starting interactive mode (type 'help' for commands)[/bold]\n")

        while True:
            try:
                user_input = Prompt.ask("[bold cyan]You[/bold cyan]").strip()

                if not user_input:
                    continue

                # Handle commands
                if user_input.lower() == "exit":
                    console.print("[yellow]Goodbye! 👋[/yellow]")
                    break

                elif user_input.lower() == "help":
                    display_help()

                elif user_input.lower() == "summary":
                    display_summary()

                elif user_input.lower() == "expenses":
                    display_expenses()

                elif user_input.lower() == "incomes":
                    display_incomes()

                elif user_input.lower() == "tasks":
                    display_tasks()

                else:
                    # Send to AI agent
                    console.print("[bold cyan]Naaman:[/bold cyan]", end=" ")
                    response = agent.chat(user_input)
                    console.print(response)
                    console.print()

            except KeyboardInterrupt:
                console.print("\n[yellow]Interrupted. Type 'exit' to quit.[/yellow]")
                continue

    except KeyboardInterrupt:
        console.print("\n[yellow]Goodbye! 👋[/yellow]")
        sys.exit(0)
    except Exception as e:
        console.print(f"[red]Error: {str(e)}[/red]")
        sys.exit(1)


if __name__ == "__main__":
    main()
