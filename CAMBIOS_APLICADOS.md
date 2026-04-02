# 📋 Cambios Aplicados - Budget Agent

**Fecha:** 2026-04-02  
**Descripción:** Se agregaron 5 nuevos campos a 3 tablas para categorización y filtrado avanzado

---

## 📊 Resumen de Cambios

| Tabla | Campos Agregados | Estado |
|-------|-----------------|--------|
| `gastos_fijos` | categoria, mes_periodo | ✅ Aplicado |
| `pagos_parciales` | mes_periodo, es_gasto_hormiga | ✅ Aplicado |
| `tareas` | categoria | ✅ Aplicado |

---

## 1️⃣ Cambios en `src/db/connection.py`

### Schema CREATE TABLE

**gastos_fijos** — ANTES vs DESPUÉS:

```python
# ANTES
CREATE TABLE IF NOT EXISTS gastos_fijos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre TEXT NOT NULL,
    monto REAL NOT NULL,
    frecuencia TEXT NOT NULL,
    descripcion TEXT,
    estado TEXT DEFAULT 'activo',
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    fecha_actualizacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)

# DESPUÉS
CREATE TABLE IF NOT EXISTS gastos_fijos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre TEXT NOT NULL,
    monto REAL NOT NULL,
    frecuencia TEXT NOT NULL,
    descripcion TEXT,
    estado TEXT DEFAULT 'activo',
    categoria TEXT DEFAULT 'fijo',              # ✨ NUEVO
    mes_periodo TEXT,                           # ✨ NUEVO
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    fecha_actualizacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
```

---

**pagos_parciales** — ANTES vs DESPUÉS:

```python
# ANTES
CREATE TABLE IF NOT EXISTS pagos_parciales (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    gasto_id INTEGER NOT NULL,
    monto REAL NOT NULL,
    fecha_pago TIMESTAMP NOT NULL,
    descripcion TEXT,
    metodo_pago TEXT,
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (gasto_id) REFERENCES gastos_fijos(id)
)

# DESPUÉS
CREATE TABLE IF NOT EXISTS pagos_parciales (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    gasto_id INTEGER NOT NULL,
    monto REAL NOT NULL,
    fecha_pago TIMESTAMP NOT NULL,
    descripcion TEXT,
    metodo_pago TEXT,
    mes_periodo TEXT,                           # ✨ NUEVO
    es_gasto_hormiga INTEGER DEFAULT 0,         # ✨ NUEVO
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (gasto_id) REFERENCES gastos_fijos(id)
)
```

---

**tareas** — ANTES vs DESPUÉS:

```python
# ANTES
CREATE TABLE IF NOT EXISTS tareas (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    descripcion TEXT NOT NULL,
    estado TEXT DEFAULT 'pendiente',
    prioridad TEXT DEFAULT 'media',
    monto_asociado REAL,
    fecha_vencimiento TIMESTAMP,
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    fecha_actualizacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)

# DESPUÉS
CREATE TABLE IF NOT EXISTS tareas (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    descripcion TEXT NOT NULL,
    estado TEXT DEFAULT 'pendiente',
    prioridad TEXT DEFAULT 'media',
    monto_asociado REAL,
    fecha_vencimiento TIMESTAMP,
    categoria TEXT DEFAULT 'personal',          # ✨ NUEVO
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    fecha_actualizacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
```

---

### Migraciones

Se agregaron 5 migraciones idempotentes (seguras para BD existente):

```python
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
```

---

## 2️⃣ Cambios en `src/db/models.py`

### create_expense()

**ANTES:**
```python
def create_expense(
    nombre: str,
    monto: float,
    frecuencia: str,
    descripcion: str = "",
    estado: str = "activo"
) -> Dict[str, Any]:
    cursor.execute("""
    INSERT INTO gastos_fijos (nombre, monto, frecuencia, descripcion, estado)
    VALUES (?, ?, ?, ?, ?)
    """, (nombre, monto, frecuencia, descripcion, estado))
    
    return {"id": expense_id, "nombre": nombre, "monto": monto, "frecuencia": frecuencia}
```

**DESPUÉS:**
```python
def create_expense(
    nombre: str,
    monto: float,
    frecuencia: str,
    descripcion: str = "",
    estado: str = "activo",
    categoria: str = "fijo",                    # ✨ NUEVO
    mes_periodo: str = ""                       # ✨ NUEVO
) -> Dict[str, Any]:
    cursor.execute("""
    INSERT INTO gastos_fijos (nombre, monto, frecuencia, descripcion, estado, categoria, mes_periodo)
    VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (nombre, monto, frecuencia, descripcion, estado, categoria, mes_periodo if mes_periodo else None))
    
    return {"id": expense_id, "nombre": nombre, "monto": monto, "frecuencia": frecuencia, "categoria": categoria}
```

---

### create_partial_payment()

**ANTES:**
```python
def create_partial_payment(
    gasto_id: int,
    monto: float,
    fecha_pago: str,
    descripcion: str = "",
    metodo_pago: str = ""
) -> Dict[str, Any]:
    cursor.execute("""
    INSERT INTO pagos_parciales (gasto_id, monto, fecha_pago, descripcion, metodo_pago)
    VALUES (?, ?, ?, ?, ?)
    """, (gasto_id, monto, fecha_pago, descripcion, metodo_pago))
    
    return {"id": payment_id, "gasto_id": gasto_id, "monto": monto}
```

**DESPUÉS:**
```python
def create_partial_payment(
    gasto_id: int,
    monto: float,
    fecha_pago: str,
    descripcion: str = "",
    metodo_pago: str = "",
    mes_periodo: str = "",                      # ✨ NUEVO
    es_gasto_hormiga: bool = False              # ✨ NUEVO
) -> Dict[str, Any]:
    cursor.execute("""
    INSERT INTO pagos_parciales (gasto_id, monto, fecha_pago, descripcion, metodo_pago, mes_periodo, es_gasto_hormiga)
    VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (gasto_id, monto, fecha_pago, descripcion, metodo_pago, mes_periodo if mes_periodo else None, 1 if es_gasto_hormiga else 0))
    
    return {"id": payment_id, "gasto_id": gasto_id, "monto": monto, "es_gasto_hormiga": es_gasto_hormiga}
```

---

### create_task()

**ANTES:**
```python
def create_task(
    descripcion: str,
    prioridad: str = "media",
    monto_asociado: float = 0.0,
    fecha_vencimiento: str = ""
) -> Dict[str, Any]:
    cursor.execute("""
    INSERT INTO tareas (descripcion, prioridad, monto_asociado, fecha_vencimiento, estado)
    VALUES (?, ?, ?, ?, 'pendiente')
    """, (descripcion, prioridad, monto_asociado if monto_asociado > 0 else None,
          fecha_vencimiento if fecha_vencimiento else None))
    
    return {"id": task_id, "descripcion": descripcion, "prioridad": prioridad}
```

**DESPUÉS:**
```python
def create_task(
    descripcion: str,
    prioridad: str = "media",
    monto_asociado: float = 0.0,
    fecha_vencimiento: str = "",
    categoria: str = "personal"                 # ✨ NUEVO
) -> Dict[str, Any]:
    cursor.execute("""
    INSERT INTO tareas (descripcion, prioridad, monto_asociado, fecha_vencimiento, estado, categoria)
    VALUES (?, ?, ?, ?, 'pendiente', ?)
    """, (descripcion, prioridad, monto_asociado if monto_asociado > 0 else None,
          fecha_vencimiento if fecha_vencimiento else None, categoria))
    
    return {"id": task_id, "descripcion": descripcion, "prioridad": prioridad, "categoria": categoria}
```

---

## 3️⃣ Cambios en `src/tools/__init__.py`

### Tool: add_expense

**ANTES:**
```json
{
  "name": "add_expense",
  "properties": {
    "nombre": {"type": "string"},
    "monto": {"type": "number"},
    "frecuencia": {"type": "string", "enum": [...]},
    "descripcion": {"type": "string"}
  },
  "required": ["nombre", "monto", "frecuencia"]
}
```

**DESPUÉS:**
```json
{
  "name": "add_expense",
  "properties": {
    "nombre": {"type": "string"},
    "monto": {"type": "number"},
    "frecuencia": {"type": "string", "enum": [...]},
    "descripcion": {"type": "string"},
    "categoria": {                              // ✨ NUEVO
      "type": "string",
      "enum": ["fijo", "variable", "deuda", "servicio"]
    },
    "mes_periodo": {                            // ✨ NUEVO
      "type": "string",
      "description": "YYYY-MM format"
    }
  },
  "required": ["nombre", "monto", "frecuencia"]
}
```

**Handler (process_tool)** — ANTES vs DESPUÉS:

```python
# ANTES
result = create_expense(
    nombre=tool_input["nombre"],
    monto=tool_input["monto"],
    frecuencia=tool_input["frecuencia"],
    descripcion=tool_input.get("descripcion", "")
)

# DESPUÉS
result = create_expense(
    nombre=tool_input["nombre"],
    monto=tool_input["monto"],
    frecuencia=tool_input["frecuencia"],
    descripcion=tool_input.get("descripcion", ""),
    categoria=tool_input.get("categoria", "fijo"),              # ✨ NUEVO
    mes_periodo=tool_input.get("mes_periodo", "")              # ✨ NUEVO
)
```

---

### Tool: record_payment

**ANTES:**
```json
{
  "name": "record_payment",
  "properties": {
    "gasto_id": {"type": "integer"},
    "monto": {"type": "number"},
    "fecha_pago": {"type": "string"},
    "metodo_pago": {"type": "string"}
  },
  "required": ["gasto_id", "monto", "fecha_pago"]
}
```

**DESPUÉS:**
```json
{
  "name": "record_payment",
  "properties": {
    "gasto_id": {"type": "integer"},
    "monto": {"type": "number"},
    "fecha_pago": {"type": "string"},
    "metodo_pago": {"type": "string"},
    "mes_periodo": {                            // ✨ NUEVO
      "type": "string",
      "description": "YYYY-MM format"
    },
    "es_gasto_hormiga": {                       // ✨ NUEVO
      "type": "boolean",
      "description": "Small impulse purchase?"
    }
  },
  "required": ["gasto_id", "monto", "fecha_pago"]
}
```

**Handler (process_tool)** — ANTES vs DESPUÉS:

```python
# ANTES
result = create_partial_payment(
    gasto_id=tool_input["gasto_id"],
    monto=tool_input["monto"],
    fecha_pago=tool_input["fecha_pago"],
    metodo_pago=tool_input.get("metodo_pago", "")
)

# DESPUÉS
result = create_partial_payment(
    gasto_id=tool_input["gasto_id"],
    monto=tool_input["monto"],
    fecha_pago=tool_input["fecha_pago"],
    metodo_pago=tool_input.get("metodo_pago", ""),
    mes_periodo=tool_input.get("mes_periodo", ""),              # ✨ NUEVO
    es_gasto_hormiga=tool_input.get("es_gasto_hormiga", False)  # ✨ NUEVO
)
```

---

### Tool: add_task

**ANTES:**
```json
{
  "name": "add_task",
  "properties": {
    "descripcion": {"type": "string"},
    "prioridad": {"type": "string", "enum": [...]},
    "monto_asociado": {"type": "number"},
    "fecha_vencimiento": {"type": "string"}
  },
  "required": ["descripcion"]
}
```

**DESPUÉS:**
```json
{
  "name": "add_task",
  "properties": {
    "descripcion": {"type": "string"},
    "prioridad": {"type": "string", "enum": [...]},
    "monto_asociado": {"type": "number"},
    "fecha_vencimiento": {"type": "string"},
    "categoria": {                              // ✨ NUEVO
      "type": "string",
      "enum": ["personal", "parcela", "trabajo", "casa"]
    }
  },
  "required": ["descripcion"]
}
```

**Handler (process_tool)** — ANTES vs DESPUÉS:

```python
# ANTES
result = create_task(
    descripcion=tool_input["descripcion"],
    prioridad=tool_input.get("prioridad", "media"),
    monto_asociado=tool_input.get("monto_asociado", 0),
    fecha_vencimiento=tool_input.get("fecha_vencimiento", "")
)

# DESPUÉS
result = create_task(
    descripcion=tool_input["descripcion"],
    prioridad=tool_input.get("prioridad", "media"),
    monto_asociado=tool_input.get("monto_asociado", 0),
    fecha_vencimiento=tool_input.get("fecha_vencimiento", ""),
    categoria=tool_input.get("categoria", "personal")           # ✨ NUEVO
)
```

---

## ✅ Tests Ejecutados

```
TEST 1: Inicializar BD con nuevos campos
   ✓ init_db() ejecutado exitosamente

TEST 2: Crear gasto con categoría y mes_periodo
   ✓ Gasto creado correctamente

TEST 3: Crear pago con gasto_hormiga y mes_periodo
   ✓ Pago creado correctamente

TEST 4: Crear tarea con categoría
   ✓ Tarea creada correctamente

TEST 5: Verificar campos en BD
   ✓ Todos los campos presentes en la BD
```

---

## 🔄 Compatibilidad

✅ **100% backward compatible:**
- Todos los nuevos parámetros tienen defaults
- Código existente sigue funcionando sin cambios
- Las migraciones `ALTER TABLE` son idempotentes
- BD existente se actualiza automáticamente al ejecutar `init_db()`

---

## 📝 Archivos Modificados

1. `src/db/connection.py` — Schema + migraciones
2. `src/db/models.py` — CRUD functions actualizadas
3. `src/tools/__init__.py` — Tools + handlers actualizados

**Total de cambios:** 3 archivos, ~100 líneas agregadas/modificadas

---

## 🎯 Valores Permitidos

### categoria (gastos_fijos)
- `fijo` — Gasto fijo/periódico
- `variable` — Gasto variable
- `deuda` — Pago de deuda
- `servicio` — Servicios (utilidades, suscripciones, etc.)

### categoria (tareas)
- `personal` — Tareas personales
- `parcela` — Tareas de la parcela
- `trabajo` — Tareas de trabajo
- `casa` — Tareas de la casa

### es_gasto_hormiga
- `0` o `False` — No es un gasto hormiga
- `1` o `True` — Es un gasto hormiga (pequeña compra impulsiva)

### mes_periodo
- Formato: `YYYY-MM` (ej: `2026-04`, `2026-12`)
- Nullable — Puede ser NULL

---
