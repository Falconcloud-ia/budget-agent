# Budget Agent - Inicio Rápido 🚀

## En 5 minutos

### 1. Preparar el entorno
```bash
cd budget-agent
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate
```

### 2. Instalar dependencias
```bash
pip install -e .
```

### 3. Configurar API Key
```bash
cp .env.example .env
# Abre .env y reemplaza YOUR_API_KEY_HERE con tu clave de Anthropic
```

### 4. ¡Ejecutar!
```bash
python -m src.cli.main
```

## Primeros comandos

```
> help
  (Ver todos los comandos disponibles)

> summary
  (Ver resumen presupuestario)

> Add a monthly income of $3000 from my job
  (El agente IA entiende lenguaje natural)

> Add a monthly expense of $1200 for rent
  (Agregar gastos fijos)

> What's my balance?
  (Preguntar sobre el balance)

> summary
  (Ver el resumen actualizado)

> exit
  (Salir)
```

## ¿Qué puedo hacer?

### Comandos disponibles
| Comando | Descripción |
|---------|------------|
| `summary` | Ver resumen presupuestario |
| `expenses` | Listar todos los gastos |
| `incomes` | Listar ingresos |
| `tasks` | Ver tareas pendientes |
| `help` | Mostrar ayuda |
| `exit` | Salir |

### Preguntar en lenguaje natural
El agente IA puede entender y responder a:
- "Agrega un gasto mensual de $1200 por renta"
- "Registra un pago de $500"
- "¿Cuál es mi balance?"
- "Crea una tarea para pagar las facturas"
- "Muéstrame el resumen financiero"

## Estructura del proyecto

```
src/
├── db/         → Base de datos SQLite
├── agent/      → Integración con Claude API
├── tools/      → 9 herramientas IA
└── cli/        → Interfaz terminal

data/          → Base de datos (se crea automáticamente)
```

## Bases de datos

### 4 Tablas principales:

1. **gastos_fijos** - Gastos fijos/recurrentes
2. **pagos_parciales** - Pagos registrados
3. **tareas** - Tareas de presupuesto
4. **ingresos** - Fuentes de ingreso

## Funcionalidades

✅ Agregar gastos con frecuencia (mensual, trimestral, anual)  
✅ Registrar ingresos  
✅ Grabar pagos parciales  
✅ Crear tareas presupuestarias  
✅ Ver resumen financiero (ingresos, gastos, balance)  
✅ Interfaz con IA que entiende lenguaje natural  
✅ Almacenamiento persistente en SQLite  

## Ejemplos de conversación

```
> Add monthly income of $3000
Agent: He agregado un ingreso mensual de $3000...

> Add expense of $1200 for rent
Agent: He agregado un gasto mensual de $1200 por renta...

> What's my balance?
Agent: Basándome en tus ingresos y gastos, tu balance mensual es...

> Show me my budget
Agent: Aquí está tu resumen presupuestario...

> Create task: pay bills by Friday
Agent: Tarea creada. Necesitas pagar las facturas antes del viernes.

> summary
(Muestra una tabla formateada con todo el resumen)
```

## Requisitos

- Python 3.11+
- Clave API de Anthropic (gratuita en claude.ai)
- ~50MB de espacio en disco

## Próximos pasos

1. **Entender**: Lee [README.md](README.md) para ver todas las funciones
2. **Diseño**: Revisa [ARCHITECTURE.md](ARCHITECTURE.md) para entender cómo funciona
3. **Extender**: Usa [DEVELOPMENT.md](DEVELOPMENT.md) para agregar nuevas características
4. **Navegar**: [INDEX.md](INDEX.md) tiene referencias a todos los archivos

## Solución de problemas

### "ANTHROPIC_API_KEY not set"
```bash
# Asegúrate de que .env tenga tu clave
cat .env
# Debe tener: ANTHROPIC_API_KEY=sk-ant-...
```

### "No module named 'anthropic'"
```bash
# Reinstala las dependencias
pip install -e .
```

### "Database is locked"
```bash
# Elimina la base de datos y comienza de nuevo
rm data/budget.db
# Ejecuta nuevamente la app
```

## Archivos importantes

- **[QUICKSTART.md](QUICKSTART.md)** - Guía en inglés
- **[README.md](README.md)** - Documentación completa
- **[ARCHITECTURE.md](ARCHITECTURE.md)** - Diseño del sistema
- **[DEVELOPMENT.md](DEVELOPMENT.md)** - Guía para desarrolladores

## ¡Listo! 🎉

Ejecuta `python -m src.cli.main` y comienza a administrar tu presupuesto con IA.

---

¿Preguntas? Revisa la documentación o prueba el comando `help` dentro de la app.
