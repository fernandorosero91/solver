# QuizSnap — Prompt de Desarrollo Estructurado

---

## 1. NOMBRE Y PROPÓSITO

**Nombre:** QuizSnap  
**Tipo:** Aplicación de escritorio en Python, proceso en segundo plano (background daemon)  
**Propósito:** Capturar automáticamente una pregunta de opción múltiple visible en pantalla mediante un atajo de teclado, enviarla a una IA con capacidad de visión, y retornar la respuesta correcta al usuario sin interrumpir su flujo de trabajo.

---

## 2. COMPORTAMIENTO PRINCIPAL

La aplicación debe:

- **Ejecutarse completamente en segundo plano** — sin ventana principal, sin ícono en la barra de tareas visible, sin interfaz activa al iniciar.
- **Escuchar hotkeys globales** en todo momento, independientemente de qué aplicación esté en foco (navegador, PDF, Teams, Zoom, etc.).
- Al activarse el hotkey:
  1. Capturar la pantalla (completa o región seleccionada).
  2. Codificar la imagen en base64.
  3. Enviarla al proveedor de IA disponible.
  4. Mostrar la respuesta en una **notificación o ventana flotante** que aparece encima de cualquier app, sin robar el foco del teclado.
  5. Desaparecer automáticamente o cerrarse con una tecla, dejando al usuario exactamente donde estaba.

---

## 3. ARQUITECTURA TÉCNICA

### 3.1 Proceso en segundo plano

```
Inicio del sistema  →  QuizSnap se registra como proceso silencioso
                    →  No aparece en la barra de tareas
                    →  Ícono opcional en la bandeja del sistema (system tray)
                    →  Escucha hotkeys de forma permanente
```

**Implementación por OS:**
- **Windows:** `pystray` para bandeja del sistema + `pythonw.exe` para ejecutar sin consola
- **Linux:** proceso daemon + `pystray` o `AppIndicator`
- **macOS:** `rumps` o `pystray` para menu bar

### 3.2 Flujo de captura

```
HOTKEY presionado
      │
      ├─► Captura completa    →  pyautogui.screenshot()
      │
      └─► Captura de región   →  Overlay transparente con selector de mouse
                                  →  pyautogui.screenshot(region=...)
```

### 3.3 Pipeline de procesamiento

```
Imagen PIL
    │
    ▼
Convertir a PNG en memoria (BytesIO)
    │
    ▼
Codificar en Base64
    │
    ▼
Balanceador de proveedores (round-robin + failover)
    │
    ├──► Gemini API          (gemini-1.5-flash)
    ├──► OpenRouter API      (llama-4-maverick:free)
    └──► Groq API            (llama-4-scout-17b)
    │
    ▼
Respuesta parseada
    │
    ▼
Mostrar resultado (ventana flotante / notificación)
```

---

## 4. PROVEEDORES DE IA

Todos deben soportar **procesamiento de imágenes (visión)** y tener **capa gratuita**.

| # | Proveedor | Modelo | Endpoint | Capa gratuita |
|---|-----------|--------|----------|---------------|
| 1 | Google Gemini | `gemini-1.5-flash` | `generativelanguage.googleapis.com` | ✅ Sí |
| 2 | OpenRouter | `meta-llama/llama-4-maverick:free` | `openrouter.ai/api/v1` | ✅ Sí |
| 3 | Groq | `meta-llama/llama-4-scout-17b-16e-instruct` | `api.groq.com/openai/v1` | ✅ Sí |

### Estrategia de balanceo

```
Primera consulta  →  Proveedor 1 (Gemini)
Segunda consulta  →  Proveedor 2 (OpenRouter)
Tercera consulta  →  Proveedor 3 (Groq)
Cuarta consulta   →  Proveedor 1 (Gemini)  [round-robin]

Si cualquier proveedor falla:
    →  Error de red, timeout, rate limit, clave inválida
    →  Intentar automáticamente con el siguiente
    →  Si todos fallan → mostrar mensaje de error al usuario
```

---

## 5. HOTKEYS CONFIGURABLES

| Acción | Hotkey por defecto | Descripción |
|--------|-------------------|-------------|
| Captura completa | `Ctrl+Shift+Q` | Captura toda la pantalla y procesa |
| Captura de región | `Ctrl+Shift+W` | Selector visual con el mouse |
| Salir | `Ctrl+Shift+X` | Cierra la aplicación completamente |

- Los hotkeys deben ser **modificables** en el archivo `.env` sin tocar el código.
- Deben funcionar **aunque la aplicación no esté en primer plano**.

---

## 6. PROMPT DEL SISTEMA PARA LA IA

El siguiente prompt se envía a cada proveedor junto con la imagen:

```
Eres un asistente experto en resolver cuestionarios de opción múltiple.

Al recibir una imagen con una pregunta tipo ABC:

1. Identifica la pregunta principal.
2. Lee todas las opciones disponibles (A, B, C, D, etc.).
3. Determina la respuesta CORRECTA basándote en tu conocimiento.
4. Responde ÚNICAMENTE con este formato:

RESPUESTA: [Letra]
OPCIÓN: [Texto completo de la opción correcta]
RAZÓN: [Explicación breve en máximo 2 oraciones]

Si hay múltiples preguntas, responde cada una con el mismo formato separadas por una línea en blanco.
Si la imagen no contiene una pregunta clara, responde: "No se detectó pregunta de opción múltiple."
No agregues texto adicional fuera de este formato.
```

---

## 7. INTERFAZ DE RESULTADO

La respuesta debe mostrarse en una **ventana flotante sin barra de título**, con estas características:

- Aparece **siempre encima** de cualquier aplicación (`topmost=True`)
- **No roba el foco** del teclado ni interrumpe al usuario
- Muestra la respuesta con color diferenciado:
  - `RESPUESTA:` → verde brillante
  - `OPCIÓN:` → naranja
  - `RAZÓN:` → azul claro
  - Proveedor usado → gris
- Botón **Copiar** para llevar la respuesta al portapapeles
- Se cierra con `ESC` o automáticamente tras N segundos (configurable)
- Posición: esquina inferior derecha o superior derecha (configurable)

---

## 8. CONFIGURACIÓN (.env)

```env
# API Keys
GEMINI_API_KEY=
OPENROUTER_API_KEY=
GROQ_API_KEY=

# Hotkeys
HOTKEY_CAPTURE=ctrl+shift+q
HOTKEY_REGION=ctrl+shift+w
HOTKEY_EXIT=ctrl+shift+x

# Comportamiento
AUTO_CLOSE_SECONDS=15        # 0 = no cerrar automáticamente
RESULT_POSITION=bottom-right # opciones: top-right, top-left, bottom-right, bottom-left
SHOW_TRAY_ICON=true          # ícono en bandeja del sistema
LOG_LEVEL=INFO               # DEBUG, INFO, WARNING, ERROR
```

---

## 9. INICIO AUTOMÁTICO (OPCIONAL)

El instalador puede configurar QuizSnap para iniciar con el sistema operativo:

- **Windows:** entrada en `HKCU\Software\Microsoft\Windows\CurrentVersion\Run`  
- **Linux:** archivo `.desktop` en `~/.config/autostart/`  
- **macOS:** `LaunchAgent` en `~/Library/LaunchAgents/`

---

## 10. ESTRUCTURA DE ARCHIVOS

```
quizsnap/
├── quiz_solver.py        # Entrada principal — proceso daemon
├── capture.py            # Módulo de captura de pantalla
├── ai_providers.py       # Gemini, OpenRouter, Groq + balanceador
├── result_window.py      # Ventana flotante de resultados
├── tray.py               # Ícono en bandeja del sistema
├── config.py             # Lectura de .env y constantes
├── requirements.txt      # Dependencias
├── .env.example          # Plantilla de configuración
└── README.md             # Instrucciones de instalación
```

---

## 11. DEPENDENCIAS PYTHON

```
keyboard>=0.13.5       # Hotkeys globales en cualquier OS
pyautogui>=0.9.54      # Captura de pantalla
Pillow>=10.0.0         # Procesamiento de imágenes
requests>=2.31.0       # Llamadas HTTP a APIs
python-dotenv>=1.0.0   # Variables de entorno
pystray>=0.19.0        # Ícono en bandeja del sistema
```

---

## 12. REQUISITOS NO FUNCIONALES

| Requisito | Especificación |
|-----------|---------------|
| Latencia máxima | < 5 segundos desde hotkey hasta mostrar respuesta |
| Consumo de memoria | < 80 MB en reposo |
| CPU en reposo | < 1% (proceso durmiente esperando hotkeys) |
| Compatibilidad | Windows 10+, Ubuntu 20.04+, macOS 12+ |
| Sin dependencias de UI | No requiere entorno gráfico activo para el daemon |
| Invisibilidad | No aparece en Alt+Tab, no tiene ventana principal |
| Resiliencia | Funciona con mínimo 1 API key configurada |

---

## 13. CASOS DE USO

### Caso principal
> El usuario tiene un examen o cuestionario abierto en el navegador.  
> Presiona `Ctrl+Shift+Q` → QuizSnap captura la pantalla → en ~3 segundos aparece una ventana discreta con "**RESPUESTA: B — Los cloroplastos realizan la fotosíntesis**" → el usuario lee, cierra con ESC, y selecciona la opción.

### Caso de región
> La pregunta está en una ventana pequeña o hay elementos visuales que distraen.  
> Presiona `Ctrl+Shift+W` → aparece un overlay semitransparente → el usuario arrastra para seleccionar solo la pregunta → QuizSnap procesa solo esa región.

### Caso de failover
> Gemini está en su límite de rate.  
> QuizSnap detecta el error HTTP 429 → automáticamente reintenta con OpenRouter → el usuario recibe la respuesta sin notar ningún fallo.

---

*QuizSnap — Versión 1.0 — Prompt de especificación técnica*
