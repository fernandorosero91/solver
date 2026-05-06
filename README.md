# ⚡ QuizSnap — Solucionador de Cuestionarios con IA

Presiona un hotkey desde **cualquier ventana**, toma captura de pantalla y obtiene la respuesta correcta al instante.

## Características

- **3 proveedores de IA** con balanceo automático: Gemini → OpenRouter → Groq
- Si un proveedor falla, el siguiente toma el relevo automáticamente
- **Todos los modelos procesan imágenes** (visión) y tienen capa gratuita
- Dos modos: captura completa o selección de región con el mouse
- Ventana de resultado flotante con syntax highlighting
- Hotkeys globales que funcionan en cualquier aplicación

## Instalación

### 1. Instalar dependencias

```bash
pip install -r requirements.txt
```

> **Linux:** También puede necesitar: `sudo apt install python3-tk xclip`
> **Windows:** Ejecutar como Administrador para que los hotkeys globales funcionen

### 2. Configurar API Keys (todas gratuitas)

```bash
cp .env.example .env
```

Edita `.env` y agrega tus keys:

| Proveedor | Dónde obtenerla | Modelo gratuito |
|-----------|----------------|-----------------|
| **Gemini** | [aistudio.google.com](https://aistudio.google.com/app/apikey) | `gemini-1.5-flash` |
| **OpenRouter** | [openrouter.ai/keys](https://openrouter.ai/keys) | `llama-4-maverick:free` |
| **Groq** | [console.groq.com/keys](https://console.groq.com/keys) | `llama-4-scout-17b` |

> Con una sola key funciona. Con las tres, mayor resiliencia.

### 3. Ejecutar

**Windows (sin ventana):**
```bash
start_quizsnap.bat
```
La aplicación se ejecutará en segundo plano sin ventana visible.

**Windows (con ventana para debugging):**
```bash
start_quizsnap_debug.bat
```
Mantiene la ventana abierta para ver logs en tiempo real.

**Linux/Mac o manual:**
```bash
python quiz_solver.py
```

**Para detener la aplicación (Windows):**
```bash
stop_quizsnap.bat
```
O presiona `Ctrl+Shift+X` desde cualquier ventana.

## Uso

| Hotkey | Acción |
|--------|--------|
| `Ctrl+Shift+Q` | Captura **pantalla completa** y resuelve |
| `Ctrl+Shift+W` | **Selecciona región** con el mouse y resuelve |
| `Ctrl+Shift+X` | Salir |

### Cómo funciona

1. Abre el cuestionario en cualquier app (navegador, PDF, etc.)
2. Presiona el hotkey
3. Aparece una ventana con la respuesta en ~2-5 segundos

### Cambiar hotkeys

Edita el archivo `.env`:

```
HOTKEY_CAPTURE=ctrl+t
HOTKEY_REGION=ctrl+b
HOTKEY_EXIT=ctrl+shift+x
```

## Formato de respuesta

```
[Gemini]
RESPUESTA: B
OPCIÓN: La fotosíntesis ocurre en los cloroplastos
RAZÓN: Los cloroplastos contienen clorofila, el pigmento que captura la luz solar...
```

## Balanceo de proveedores

- **Round-robin:** cada consulta rota entre Gemini, OpenRouter y Groq
- **Failover automático:** si uno falla (límite de rate, error de red, etc.), el siguiente procesa la imagen
- Los errores se registran en `quizsnap.log`

## Notas

- En **Linux**, el script puede necesitar permisos root para capturar hotkeys globales: `sudo python quiz_solver.py`
- En **macOS**, conceder permisos de accesibilidad en Preferencias del Sistema → Privacidad → Accesibilidad
