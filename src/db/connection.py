"""Database connection management."""

import sqlite3
from pathlib import Path
from src.config import DATABASE_PATH


def get_connection():
    """Get a database connection."""
    conn = sqlite3.connect(DATABASE_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    """Initialize the database with schema."""
    conn = get_connection()
    cursor = conn.cursor()

    # Create tables
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS gastos_fijos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre TEXT NOT NULL,
        monto REAL NOT NULL,
        frecuencia TEXT NOT NULL,
        descripcion TEXT,
        estado TEXT DEFAULT 'activo',
        categoria TEXT DEFAULT 'fijo',
        mes_periodo TEXT,
        fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        fecha_actualizacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS pagos_parciales (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        gasto_id INTEGER NOT NULL,
        monto REAL NOT NULL,
        fecha_pago TIMESTAMP NOT NULL,
        descripcion TEXT,
        metodo_pago TEXT,
        mes_periodo TEXT,
        es_gasto_hormiga INTEGER DEFAULT 0,
        fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (gasto_id) REFERENCES gastos_fijos(id)
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS tareas (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        descripcion TEXT NOT NULL,
        estado TEXT DEFAULT 'pendiente',
        prioridad TEXT DEFAULT 'media',
        monto_asociado REAL,
        fecha_vencimiento TIMESTAMP,
        categoria TEXT DEFAULT 'personal',
        fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        fecha_actualizacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS ingresos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        descripcion TEXT NOT NULL,
        monto REAL NOT NULL,
        frecuencia TEXT NOT NULL,
        fuente TEXT,
        estado TEXT DEFAULT 'activo',
        fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        fecha_actualizacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)

    # Migraciones seguras para usuarios con base de datos existente
    migrations = [
        "ALTER TABLE gastos_fijos ADD COLUMN categoria TEXT DEFAULT 'fijo'",
        "ALTER TABLE gastos_fijos ADD COLUMN mes_periodo TEXT",
        "ALTER TABLE pagos_parciales ADD COLUMN mes_periodo TEXT",
        "ALTER TABLE pagos_parciales ADD COLUMN es_gasto_hormiga INTEGER DEFAULT 0",
        "ALTER TABLE tareas ADD COLUMN categoria TEXT DEFAULT 'personal'",
    ]

    for sql in migrations:
        try:
            cursor.execute(sql)
        except Exception:
            pass  # Columna ya existe

    conn.commit()
    conn.close()
