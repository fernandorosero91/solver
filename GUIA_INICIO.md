# 📋 Guía de Inicio - QuizSnap para Windows

## ✅ Solución al problema de la ventana CMD

Ahora QuizSnap se ejecuta **completamente en segundo plano** sin dejar ventanas abiertas.

---

## 🚀 Inicio Rápido

### Opción 1: Sin ventana (Recomendado) ⭐

**Doble clic en:**
```
start_quizsnap.bat
```

- ✅ No muestra ninguna ventana
- ✅ Aparece un mensaje de confirmación
- ✅ Listo para usar con los hotkeys

### Opción 2: Ventana minimizada 🪟

**Doble clic en:**
```
start_quizsnap_simple.bat
```

- ✅ Ventana minimizada en la barra de tareas
- ✅ Fácil de cerrar (clic derecho → Cerrar)

### Opción 3: Modo debug 🔍

**Doble clic en:**
```
start_quizsnap_debug.bat
```

- ✅ Ventana visible con logs en tiempo real
- ✅ Útil para ver errores

---

## 🛑 Detener QuizSnap

### Opción 1: Hotkey
Presiona `Ctrl+Shift+X` desde cualquier ventana

### Opción 2: Script
Doble clic en:
```
stop_quizsnap.bat
```

---

## 📝 Archivos explicados

| Archivo | Descripción | Cuándo usar |
|---------|-------------|-------------|
| `start_quizsnap.bat` | Inicio sin ventana | Uso diario ⭐ |
| `start_quizsnap.vbs` | Script VBS (usado por el .bat) | No ejecutar directamente |
| `start_quizsnap_simple.bat` | Ventana minimizada | Alternativa |
| `start_quizsnap_debug.bat` | Ventana visible con logs | Debugging |
| `stop_quizsnap.bat` | Detener aplicación | Cuando necesites cerrar |

---

## ✨ Cómo funciona (sin ventana)

1. Ejecutas `start_quizsnap.bat`
2. El .bat llama a `start_quizsnap.vbs`
3. El VBS ejecuta `pythonw.exe` (Python sin ventana)
4. Aparece un mensaje confirmando que inició
5. QuizSnap queda corriendo en segundo plano
6. Usas los hotkeys desde cualquier ventana

---

## 🔍 Verificar si está corriendo

### Método 1: Probar hotkey
Presiona `Ctrl+Shift+Q` → Si captura pantalla, está corriendo ✅

### Método 2: Ver procesos
```bash
tasklist | findstr pythonw
```
Si ves `pythonw.exe`, está corriendo ✅

### Método 3: Ver log
```bash
type quizsnap.log
```
Busca: `🚀 QuizSnap activo`

---

## ⚙️ Hotkeys por defecto

| Hotkey | Acción |
|--------|--------|
| `Ctrl+Shift+Q` | Captura pantalla completa |
| `Ctrl+Shift+S` | Selección de región |
| `Ctrl+Shift+X` | Salir |

Para cambiar los hotkeys, edita el archivo `.env`

---

## 🆘 Solución de problemas

### No aparece el mensaje de confirmación
- Ejecuta `start_quizsnap_debug.bat` para ver errores
- Verifica que el entorno virtual esté instalado

### Los hotkeys no funcionan
1. Ejecuta como **Administrador** (clic derecho → Ejecutar como administrador)
2. Verifica que los hotkeys no estén en uso
3. Revisa `quizsnap.log`

### No puedo detener la aplicación
```bash
stop_quizsnap.bat
```

### "No se encontró el entorno virtual"
```bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

---

## 📊 Comparación de métodos

| Método | Ventana | Logs visibles | Recomendado |
|--------|---------|---------------|-------------|
| `start_quizsnap.bat` | ❌ Ninguna | Solo archivo | ✅ Uso diario |
| `start_quizsnap_simple.bat` | 🪟 Minimizada | Solo archivo | Alternativa |
| `start_quizsnap_debug.bat` | ✅ Visible | En tiempo real | Debugging |

---

## 💡 Consejos

1. **Primera vez**: Usa `start_quizsnap_debug.bat` para verificar que todo funciona
2. **Uso diario**: Usa `start_quizsnap.bat` para ejecución invisible
3. **Problemas**: Siempre revisa `quizsnap.log`
4. **Administrador**: Ejecuta como administrador para que los hotkeys globales funcionen

---

## 📖 Más información

- Ver `README.md` para instalación completa
- Ver `quizsnap.log` para logs detallados
- Ver `.env` para configuración de hotkeys y API keys
