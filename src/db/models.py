"""Database models and operations."""

from datetime import datetime
from typing import List, Dict, Any
from .connection import get_connection


# Gastos Fijos (Fixed Expenses)

def create_expense(
    nombre: str,
    monto: float,
    frecuencia: str,
    descripcion: str = "",
    estado: str = "activo"
) -> Dict[str, Any]:
    """Create a fixed expense."""
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    INSERT INTO gastos_fijos (nombre, monto, frecuencia, descripcion, estado)
    VALUES (?, ?, ?, ?, ?)
    """, (nombre, monto, frecuencia, descripcion, estado))

    conn.commit()
    expense_id = cursor.lastrowid
    conn.close()

    return {"id": expense_id, "nombre": nombre, "monto": monto, "frecuencia": frecuencia}


def get_all_expenses() -> List[Dict[str, Any]]:
    """Get all expenses."""
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM gastos_fijos WHERE estado = 'activo'")
    expenses = [dict(row) for row in cursor.fetchall()]

    conn.close()
    return expenses


def update_expense_status(expense_id: int, status: str) -> bool:
    """Update expense status."""
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    UPDATE gastos_fijos
    SET estado = ?, fecha_actualizacion = CURRENT_TIMESTAMP
    WHERE id = ?
    """, (status, expense_id))

    conn.commit()
    success = cursor.rowcount > 0
    conn.close()

    return success


# Pagos Parciales (Partial Payments)

def create_partial_payment(
    gasto_id: int,
    monto: float,
    fecha_pago: str,
    descripcion: str = "",
    metodo_pago: str = ""
) -> Dict[str, Any]:
    """Create a partial payment."""
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    INSERT INTO pagos_parciales (gasto_id, monto, fecha_pago, descripcion, metodo_pago)
    VALUES (?, ?, ?, ?, ?)
    """, (gasto_id, monto, fecha_pago, descripcion, metodo_pago))

    conn.commit()
    payment_id = cursor.lastrowid
    conn.close()

    return {"id": payment_id, "gasto_id": gasto_id, "monto": monto}


def get_all_partial_payments() -> List[Dict[str, Any]]:
    """Get all partial payments."""
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM pagos_parciales ORDER BY fecha_pago DESC")
    payments = [dict(row) for row in cursor.fetchall()]

    conn.close()
    return payments


# Tareas (Tasks)

def create_task(
    descripcion: str,
    prioridad: str = "media",
    monto_asociado: float = 0.0,
    fecha_vencimiento: str = ""
) -> Dict[str, Any]:
    """Create a task."""
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    INSERT INTO tareas (descripcion, prioridad, monto_asociado, fecha_vencimiento, estado)
    VALUES (?, ?, ?, ?, 'pendiente')
    """, (descripcion, prioridad, monto_asociado if monto_asociado > 0 else None,
          fecha_vencimiento if fecha_vencimiento else None))

    conn.commit()
    task_id = cursor.lastrowid
    conn.close()

    return {"id": task_id, "descripcion": descripcion, "prioridad": prioridad}


def get_all_tasks() -> List[Dict[str, Any]]:
    """Get all pending tasks."""
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    SELECT * FROM tareas
    WHERE estado != 'completada'
    ORDER BY prioridad DESC, fecha_vencimiento ASC
    """)
    tasks = [dict(row) for row in cursor.fetchall()]

    conn.close()
    return tasks


def update_task_status(task_id: int, status: str) -> bool:
    """Update task status."""
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    UPDATE tareas
    SET estado = ?, fecha_actualizacion = CURRENT_TIMESTAMP
    WHERE id = ?
    """, (status, task_id))

    conn.commit()
    success = cursor.rowcount > 0
    conn.close()

    return success


# Ingresos (Income)

def create_income(
    descripcion: str,
    monto: float,
    frecuencia: str,
    fuente: str = "",
    estado: str = "activo"
) -> Dict[str, Any]:
    """Create an income entry."""
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    INSERT INTO ingresos (descripcion, monto, frecuencia, fuente, estado)
    VALUES (?, ?, ?, ?, ?)
    """, (descripcion, monto, frecuencia, fuente, estado))

    conn.commit()
    income_id = cursor.lastrowid
    conn.close()

    return {"id": income_id, "descripcion": descripcion, "monto": monto}


def get_all_incomes() -> List[Dict[str, Any]]:
    """Get all active incomes."""
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM ingresos WHERE estado = 'activo'")
    incomes = [dict(row) for row in cursor.fetchall()]

    conn.close()
    return incomes


# Summary

def get_summary() -> Dict[str, Any]:
    """Get budget summary."""
    conn = get_connection()
    cursor = conn.cursor()

    # Total monthly expenses
    cursor.execute("SELECT COALESCE(SUM(monto), 0) as total FROM gastos_fijos WHERE estado = 'activo' AND frecuencia = 'mensual'")
    monthly_expenses = cursor.fetchone()["total"]

    # Total monthly income
    cursor.execute("SELECT COALESCE(SUM(monto), 0) as total FROM ingresos WHERE estado = 'activo' AND frecuencia = 'mensual'")
    monthly_income = cursor.fetchone()["total"]

    # Recent payments
    cursor.execute("SELECT COALESCE(SUM(monto), 0) as total FROM pagos_parciales WHERE date(fecha_pago) >= date('now', '-30 days')")
    recent_payments = cursor.fetchone()["total"]

    # Pending tasks
    cursor.execute("SELECT COUNT(*) as count FROM tareas WHERE estado = 'pendiente'")
    pending_tasks = cursor.fetchone()["count"]

    conn.close()

    return {
        "monthly_income": monthly_income,
        "monthly_expenses": monthly_expenses,
        "balance": monthly_income - monthly_expenses,
        "recent_payments_30days": recent_payments,
        "pending_tasks": pending_tasks,
    }
