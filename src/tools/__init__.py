"""Agent tools definitions."""

import json
from typing import Any
from src.db.models import (
    create_expense,
    create_income,
    create_task,
    create_partial_payment,
    get_all_expenses,
    get_all_incomes,
    get_all_tasks,
    get_all_partial_payments,
    get_summary,
    update_task_status,
)


TOOLS = [
    {
        "name": "add_expense",
        "description": "Add a fixed expense (e.g., rent, utilities, subscriptions)",
        "input_schema": {
            "type": "object",
            "properties": {
                "nombre": {
                    "type": "string",
                    "description": "Name of the expense"
                },
                "monto": {
                    "type": "number",
                    "description": "Amount in currency units"
                },
                "frecuencia": {
                    "type": "string",
                    "enum": ["mensual", "trimestral", "anual", "semanal"],
                    "description": "Payment frequency"
                },
                "descripcion": {
                    "type": "string",
                    "description": "Optional description"
                }
            },
            "required": ["nombre", "monto", "frecuencia"]
        }
    },
    {
        "name": "add_income",
        "description": "Add an income source",
        "input_schema": {
            "type": "object",
            "properties": {
                "descripcion": {
                    "type": "string",
                    "description": "Description of income source"
                },
                "monto": {
                    "type": "number",
                    "description": "Amount in currency units"
                },
                "frecuencia": {
                    "type": "string",
                    "enum": ["mensual", "trimestral", "anual", "semanal"],
                    "description": "Payment frequency"
                },
                "fuente": {
                    "type": "string",
                    "description": "Source of income (e.g., salary, freelance)"
                }
            },
            "required": ["descripcion", "monto", "frecuencia"]
        }
    },
    {
        "name": "record_payment",
        "description": "Record a partial payment towards an expense",
        "input_schema": {
            "type": "object",
            "properties": {
                "gasto_id": {
                    "type": "integer",
                    "description": "ID of the expense"
                },
                "monto": {
                    "type": "number",
                    "description": "Payment amount"
                },
                "fecha_pago": {
                    "type": "string",
                    "description": "Payment date (YYYY-MM-DD)"
                },
                "metodo_pago": {
                    "type": "string",
                    "description": "Payment method (cash, card, transfer, etc.)"
                }
            },
            "required": ["gasto_id", "monto", "fecha_pago"]
        }
    },
    {
        "name": "add_task",
        "description": "Add a budget-related task or reminder",
        "input_schema": {
            "type": "object",
            "properties": {
                "descripcion": {
                    "type": "string",
                    "description": "Task description"
                },
                "prioridad": {
                    "type": "string",
                    "enum": ["baja", "media", "alta"],
                    "description": "Task priority"
                },
                "monto_asociado": {
                    "type": "number",
                    "description": "Associated cost (optional)"
                },
                "fecha_vencimiento": {
                    "type": "string",
                    "description": "Due date (YYYY-MM-DD, optional)"
                }
            },
            "required": ["descripcion"]
        }
    },
    {
        "name": "get_budget_summary",
        "description": "Get a summary of income, expenses, balance and pending tasks",
        "input_schema": {
            "type": "object",
            "properties": {},
            "required": []
        }
    },
    {
        "name": "list_expenses",
        "description": "List all active fixed expenses",
        "input_schema": {
            "type": "object",
            "properties": {},
            "required": []
        }
    },
    {
        "name": "list_incomes",
        "description": "List all active income sources",
        "input_schema": {
            "type": "object",
            "properties": {},
            "required": []
        }
    },
    {
        "name": "list_tasks",
        "description": "List all pending budget-related tasks",
        "input_schema": {
            "type": "object",
            "properties": {},
            "required": []
        }
    },
    {
        "name": "complete_task",
        "description": "Mark a task as completed",
        "input_schema": {
            "type": "object",
            "properties": {
                "task_id": {
                    "type": "integer",
                    "description": "ID of the task to complete"
                }
            },
            "required": ["task_id"]
        }
    }
]


def process_tool(tool_name: str, tool_input: dict) -> str:
    """Process a tool call and return the result."""
    try:
        if tool_name == "add_expense":
            result = create_expense(
                nombre=tool_input["nombre"],
                monto=tool_input["monto"],
                frecuencia=tool_input["frecuencia"],
                descripcion=tool_input.get("descripcion", "")
            )
            return json.dumps({"success": True, "data": result})

        elif tool_name == "add_income":
            result = create_income(
                descripcion=tool_input["descripcion"],
                monto=tool_input["monto"],
                frecuencia=tool_input["frecuencia"],
                fuente=tool_input.get("fuente", "")
            )
            return json.dumps({"success": True, "data": result})

        elif tool_name == "record_payment":
            result = create_partial_payment(
                gasto_id=tool_input["gasto_id"],
                monto=tool_input["monto"],
                fecha_pago=tool_input["fecha_pago"],
                metodo_pago=tool_input.get("metodo_pago", "")
            )
            return json.dumps({"success": True, "data": result})

        elif tool_name == "add_task":
            result = create_task(
                descripcion=tool_input["descripcion"],
                prioridad=tool_input.get("prioridad", "media"),
                monto_asociado=tool_input.get("monto_asociado", 0),
                fecha_vencimiento=tool_input.get("fecha_vencimiento", "")
            )
            return json.dumps({"success": True, "data": result})

        elif tool_name == "get_budget_summary":
            result = get_summary()
            return json.dumps({"success": True, "data": result})

        elif tool_name == "list_expenses":
            result = get_all_expenses()
            return json.dumps({"success": True, "data": result})

        elif tool_name == "list_incomes":
            result = get_all_incomes()
            return json.dumps({"success": True, "data": result})

        elif tool_name == "list_tasks":
            result = get_all_tasks()
            return json.dumps({"success": True, "data": result})

        elif tool_name == "complete_task":
            success = update_task_status(tool_input["task_id"], "completada")
            return json.dumps({
                "success": success,
                "message": "Task completed" if success else "Task not found"
            })

        else:
            return json.dumps({"success": False, "error": f"Unknown tool: {tool_name}"})

    except Exception as e:
        return json.dumps({"success": False, "error": str(e)})
