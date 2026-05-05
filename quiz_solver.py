#!/usr/bin/env python3
"""
QuizSnap - Solucionador de cuestionarios por captura de pantalla
Hotkeys configurables, balanceo entre Gemini, OpenRouter y Groq
"""

import os
import sys
import time
import base64
import json
import threading
import logging
from io import BytesIO
from datetime import datetime
from typing import Optional

import keyboard
import pyautogui
from PIL import Image
import requests
from dotenv import load_dotenv
from google import genai

# ─── Configuración de logging ──────────────────────────────────────────────────
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler("quizsnap.log", encoding="utf-8"),
    ],
)
log = logging.getLogger("QuizSnap")

load_dotenv()

# ─── Configuración de APIs ─────────────────────────────────────────────────────
GEMINI_API_KEY    = os.getenv("GEMINI_API_KEY", "")
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY", "")
GROQ_API_KEY      = os.getenv("GROQ_API_KEY", "")

# ─── Modelos con visión (capas gratuitas / económicos) ─────────────────────────
GEMINI_MODEL      = "gemini-3-flash-preview"    # Modelo Gemini 3 Flash
OPENROUTER_MODEL  = "openrouter/free"  # Router automático de modelos gratuitos con visión
GROQ_MODEL        = "meta-llama/llama-4-scout-17b-16e-instruct"  # Soporta visión

# ─── Hotkeys ──────────────────────────────────────────────────────────────────
HOTKEY_CAPTURE    = os.getenv("HOTKEY_CAPTURE", "ctrl+shift+q")   # Captura y resuelve
HOTKEY_REGION     = os.getenv("HOTKEY_REGION",  "ctrl+shift+w")   # Selección de región
HOTKEY_EXIT       = os.getenv("HOTKEY_EXIT",    "ctrl+shift+x")   # Salir

# ─── Prompt del sistema ────────────────────────────────────────────────────────
SYSTEM_PROMPT = """Eres un asistente experto en resolver cuestionarios de opción múltiple.

INSTRUCCIONES:
- Analiza la imagen y determina la respuesta correcta
- NO transcritas la pregunta ni las opciones
- Responde ÚNICAMENTE con este formato:

RESPUESTA: [Letra]
RAZÓN: [Explicación breve en 1-2 oraciones del por qué es correcta]

IMPORTANTE: Responde SOLO UNA pregunta, aunque haya múltiples en la imagen.
Si no hay pregunta clara, responde: "No se detectó pregunta de opción múltiple."""

# ─────────────────────────────────────────────────────────────────────────────
#  CAPTURA DE PANTALLA
# ─────────────────────────────────────────────────────────────────────────────

def capture_fullscreen() -> Image.Image:
    """Captura toda la pantalla."""
    screenshot = pyautogui.screenshot()
    log.info("📸 Captura de pantalla completa tomada")
    return screenshot


def capture_region() -> Optional[Image.Image]:
    """Captura una región seleccionada por el usuario."""
    try:
        import tkinter as tk
        from tkinter import ttk

        result = {"region": None}

        root = tk.Tk()
        root.attributes("-fullscreen", True)
        root.attributes("-alpha", 0.3)
        root.configure(bg="black")
        root.attributes("-topmost", True)

        canvas = tk.Canvas(root, cursor="cross", bg="gray10")
        canvas.pack(fill=tk.BOTH, expand=True)

        start_x = start_y = 0
        rect = None

        label = tk.Label(
            root,
            text="Arrastra para seleccionar región • ESC para cancelar",
            fg="white", bg="#1a1a2e", font=("Consolas", 13),
            padx=10, pady=5
        )
        label.place(relx=0.5, rely=0.02, anchor="n")

        def on_press(event):
            nonlocal start_x, start_y, rect
            start_x, start_y = event.x, event.y
            rect = canvas.create_rectangle(
                start_x, start_y, start_x, start_y,
                outline="#00ff88", width=2, dash=(4, 4)
            )

        def on_drag(event):
            canvas.coords(rect, start_x, start_y, event.x, event.y)

        def on_release(event):
            x1 = min(start_x, event.x)
            y1 = min(start_y, event.y)
            x2 = max(start_x, event.x)
            y2 = max(start_y, event.y)
            if (x2 - x1) > 10 and (y2 - y1) > 10:
                result["region"] = (x1, y1, x2 - x1, y2 - y1)
            root.destroy()

        def on_escape(event):
            root.destroy()

        canvas.bind("<ButtonPress-1>", on_press)
        canvas.bind("<B1-Motion>", on_drag)
        canvas.bind("<ButtonRelease-1>", on_release)
        root.bind("<Escape>", on_escape)
        root.mainloop()

        if result["region"]:
            x, y, w, h = result["region"]
            screenshot = pyautogui.screenshot(region=(x, y, w, h))
            log.info(f"📸 Región capturada: {w}x{h}px en ({x},{y})")
            return screenshot
        return None

    except Exception as e:
        log.error(f"Error en captura de región: {e}")
        # Fallback: captura completa
        return capture_fullscreen()


def image_to_base64(img: Image.Image) -> str:
    """Convierte una imagen PIL a base64."""
    buffer = BytesIO()
    img.save(buffer, format="PNG", optimize=True)
    return base64.b64encode(buffer.getvalue()).decode("utf-8")


# ─────────────────────────────────────────────────────────────────────────────
#  PROVEEDORES DE IA
# ─────────────────────────────────────────────────────────────────────────────

def query_gemini(image_b64: str) -> str:
    """Consulta Google Gemini con visión usando el nuevo SDK."""
    if not GEMINI_API_KEY:
        raise ValueError("GEMINI_API_KEY no configurado")

    try:
        # Configurar el cliente con la API key
        os.environ["GEMINI_API_KEY"] = GEMINI_API_KEY
        client = genai.Client()
        
        # Decodificar la imagen base64
        image_bytes = base64.b64decode(image_b64)
        
        # Crear el contenido con formato correcto
        response = client.models.generate_content(
            model=GEMINI_MODEL,
            contents={
                "parts": [
                    {"text": SYSTEM_PROMPT + "\n\nAnaliza la siguiente imagen:"},
                    {"inline_data": {"mime_type": "image/png", "data": image_b64}}
                ]
            }
        )
        
        return response.text
    except Exception as e:
        raise ValueError(f"Error en Gemini: {str(e)}")


def query_openrouter(image_b64: str) -> str:
    """Consulta OpenRouter con un modelo de visión gratuito usando formato OpenAI."""
    if not OPENROUTER_API_KEY:
        raise ValueError("OPENROUTER_API_KEY no configurado")

    url = "https://openrouter.ai/api/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json",
        "HTTP-Referer": "https://quizsnap.local",  # Opcional para rankings
        "X-Title": "QuizSnap",  # Opcional para rankings
    }

    payload = {
        "model": OPENROUTER_MODEL,
        "messages": [
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": SYSTEM_PROMPT + "\n\nAnaliza esta imagen y resuelve la pregunta:"},
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/png;base64,{image_b64}"
                        }
                    }
                ]
            }
        ],
        "max_tokens": 512,
        "temperature": 0.1,
    }

    resp = requests.post(url, headers=headers, json=payload, timeout=30)
    resp.raise_for_status()
    data = resp.json()

    choices = data.get("choices", [])
    if choices:
        return choices[0]["message"]["content"]
    raise ValueError("Respuesta vacía de OpenRouter")


def query_groq(image_b64: str) -> str:
    """Consulta Groq con modelo de visión."""
    if not GROQ_API_KEY:
        raise ValueError("GROQ_API_KEY no configurado")

    url = "https://api.groq.com/openai/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json",
    }

    payload = {
        "model": GROQ_MODEL,
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": "Analiza esta imagen y resuelve la pregunta:"},
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/png;base64,{image_b64}"
                        }
                    }
                ]
            }
        ],
        "max_tokens": 512,
        "temperature": 0.1,
    }

    resp = requests.post(url, headers=headers, json=payload, timeout=30)
    resp.raise_for_status()
    data = resp.json()

    choices = data.get("choices", [])
    if choices:
        return choices[0]["message"]["content"]
    raise ValueError("Respuesta vacía de Groq")


# ─────────────────────────────────────────────────────────────────────────────
#  BALANCEADOR DE PROVEEDORES
# ─────────────────────────────────────────────────────────────────────────────

PROVIDERS = [
    ("Gemini",      query_gemini),
    ("OpenRouter",  query_openrouter),
    ("Groq",        query_groq),
]

_provider_index = 0  # Round-robin actual
_lock = threading.Lock()


def get_next_provider():
    """Retorna el siguiente proveedor en round-robin."""
    global _provider_index
    with _lock:
        idx = _provider_index
        _provider_index = (_provider_index + 1) % len(PROVIDERS)
        return idx


def solve_with_ai(image: Image.Image) -> str:
    """
    Intenta resolver la pregunta balanceando entre proveedores.
    Si uno falla, prueba el siguiente automáticamente.
    """
    image_b64 = image_to_base64(image)
    start_idx = get_next_provider()

    for i in range(len(PROVIDERS)):
        idx = (start_idx + i) % len(PROVIDERS)
        name, func = PROVIDERS[idx]
        try:
            log.info(f"🤖 Consultando {name}...")
            answer = func(image_b64)
            log.info(f"✅ Respuesta recibida de {name}")
            return f"[{name}]\n{answer}"
        except Exception as e:
            log.warning(f"⚠️  {name} falló: {e}")
            if i < len(PROVIDERS) - 1:
                log.info("🔄 Intentando con el siguiente proveedor...")

    return "❌ Todos los proveedores fallaron. Verifica tus API keys y conexión."


# ─────────────────────────────────────────────────────────────────────────────
#  VENTANA DE RESULTADOS (tkinter overlay)
# ─────────────────────────────────────────────────────────────────────────────

def show_result(answer: str, provider: str = ""):
    """Muestra la respuesta en una ventana flotante."""
    try:
        import tkinter as tk
        from tkinter import font as tkfont

        root = tk.Tk()
        root.title("QuizSnap — Respuesta")
        root.attributes("-topmost", True)
        root.attributes("-alpha", 0.92)  # Transparencia del 92%
        root.configure(bg="#1a1a1a")
        root.resizable(True, True)

        # Geometría inicial
        root.geometry("520x320+50+50")

        # Header minimalista
        header = tk.Frame(root, bg="#2a2a2a", pady=6)
        header.pack(fill=tk.X)

        tk.Label(
            header, text="QuizSnap",
            fg="#b0b0b0", bg="#2a2a2a",
            font=("Segoe UI", 10)
        ).pack(side=tk.LEFT, padx=14)

        ts = datetime.now().strftime("%H:%M:%S")
        tk.Label(
            header, text=ts,
            fg="#707070", bg="#2a2a2a",
            font=("Segoe UI", 9)
        ).pack(side=tk.RIGHT, padx=14)

        # Área de texto
        frame = tk.Frame(root, bg="#1a1a1a")
        frame.pack(fill=tk.BOTH, expand=True, padx=12, pady=(8, 0))

        scrollbar = tk.Scrollbar(frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        text = tk.Text(
            frame,
            bg="#1a1a1a", fg="#d0d0d0",
            font=("Segoe UI", 10),
            relief=tk.FLAT,
            padx=8, pady=8,
            wrap=tk.WORD,
            yscrollcommand=scrollbar.set,
            selectbackground="#404040",
        )
        text.pack(fill=tk.BOTH, expand=True)
        scrollbar.config(command=text.yview)

        # Colores discretos y sutiles
        text.tag_config("answer",  foreground="#c0c0c0", font=("Segoe UI", 11, "bold"))
        text.tag_config("option",  foreground="#b0b0b0")
        text.tag_config("reason",  foreground="#a0a0a0")
        text.tag_config("provider",foreground="#707070", font=("Segoe UI", 9))
        text.tag_config("normal",  foreground="#d0d0d0")

        for line in answer.split("\n"):
            if line.startswith("RESPUESTA:"):
                text.insert(tk.END, line + "\n", "answer")
            elif line.startswith("OPCIÓN:"):
                text.insert(tk.END, line + "\n", "option")
            elif line.startswith("RAZÓN:"):
                text.insert(tk.END, line + "\n", "reason")
            elif line.startswith("[") and line.endswith("]"):
                text.insert(tk.END, line + "\n", "provider")
            else:
                text.insert(tk.END, line + "\n", "normal")

        text.config(state=tk.DISABLED)

        # Botones minimalistas
        btn_frame = tk.Frame(root, bg="#1a1a1a", pady=8)
        btn_frame.pack(fill=tk.X, padx=12)

        def copy_to_clipboard():
            root.clipboard_clear()
            root.clipboard_append(answer)
            btn_copy.config(text="✓ Copiado")
            root.after(1500, lambda: btn_copy.config(text="Copiar"))

        btn_copy = tk.Button(
            btn_frame, text="Copiar",
            command=copy_to_clipboard,
            bg="#2a2a2a", fg="#b0b0b0",
            relief=tk.FLAT, padx=12, pady=5,
            font=("Segoe UI", 9),
            cursor="hand2",
            activebackground="#3a3a3a",
        )
        btn_copy.pack(side=tk.LEFT, padx=(0, 6))

        btn_close = tk.Button(
            btn_frame, text="Cerrar",
            command=root.destroy,
            bg="#2a2a2a", fg="#b0b0b0",
            relief=tk.FLAT, padx=12, pady=5,
            font=("Segoe UI", 9),
            cursor="hand2",
            activebackground="#3a3a3a",
        )
        btn_close.pack(side=tk.RIGHT)

        # Cerrar con ESC
        root.bind("<Escape>", lambda e: root.destroy())

        root.mainloop()

    except Exception as e:
        # Fallback: imprimir en consola
        log.error(f"Error mostrando ventana: {e}")
        print("\n" + "="*50)
        print(answer)
        print("="*50 + "\n")


# ─────────────────────────────────────────────────────────────────────────────
#  HANDLERS DE HOTKEYS
# ─────────────────────────────────────────────────────────────────────────────

_processing = False
_processing_lock = threading.Lock()


def handle_capture():
    """Handler para captura de pantalla completa."""
    global _processing
    with _processing_lock:
        if _processing:
            log.warning("⏳ Ya hay una consulta en proceso, espera...")
            return
        _processing = True

    def run():
        global _processing
        try:
            time.sleep(0.1)  # Pequeña pausa para evitar capturar el cursor
            screenshot = capture_fullscreen()
            answer = solve_with_ai(screenshot)
            print(f"\n{'─'*50}\n{answer}\n{'─'*50}\n")
            threading.Thread(target=show_result, args=(answer,), daemon=True).start()
        except Exception as e:
            log.error(f"Error en captura: {e}")
        finally:
            with _processing_lock:
                _processing = False

    threading.Thread(target=run, daemon=True).start()


def handle_region():
    """Handler para selección de región."""
    global _processing
    with _processing_lock:
        if _processing:
            log.warning("⏳ Ya hay una consulta en proceso, espera...")
            return
        _processing = True

    def run():
        global _processing
        try:
            screenshot = capture_region()
            if screenshot is None:
                log.info("Captura cancelada")
                return
            answer = solve_with_ai(screenshot)
            print(f"\n{'─'*50}\n{answer}\n{'─'*50}\n")
            threading.Thread(target=show_result, args=(answer,), daemon=True).start()
        except Exception as e:
            log.error(f"Error en captura de región: {e}")
        finally:
            with _processing_lock:
                _processing = False

    threading.Thread(target=run, daemon=True).start()


# ─────────────────────────────────────────────────────────────────────────────
#  INICIO
# ─────────────────────────────────────────────────────────────────────────────

def check_api_keys():
    """Verifica qué API keys están configuradas."""
    configured = []
    missing = []
    for name, key in [("Gemini", GEMINI_API_KEY), ("OpenRouter", OPENROUTER_API_KEY), ("Groq", GROQ_API_KEY)]:
        if key:
            configured.append(name)
        else:
            missing.append(name)

    if not configured:
        log.error("❌ No hay ninguna API key configurada. Edita el archivo .env")
        sys.exit(1)

    log.info(f"✅ Proveedores activos: {', '.join(configured)}")
    if missing:
        log.warning(f"⚠️  Sin configurar: {', '.join(missing)}")

    return configured


def print_banner():
    banner = """
╔══════════════════════════════════════════════════════╗
║          ⚡ QuizSnap — Solucionador IA               ║
╠══════════════════════════════════════════════════════╣
║  Captura pantalla completa : {h1:<24}║
║  Seleccionar región        : {h2:<24}║
║  Salir                     : {h3:<24}║
╚══════════════════════════════════════════════════════╝
""".format(h1=HOTKEY_CAPTURE, h2=HOTKEY_REGION, h3=HOTKEY_EXIT)
    print(banner)


def main():
    print_banner()
    check_api_keys()

    # Registrar hotkeys globales
    keyboard.add_hotkey(HOTKEY_CAPTURE, handle_capture)
    keyboard.add_hotkey(HOTKEY_REGION,  handle_region)

    log.info("🚀 QuizSnap activo. Presiona los hotkeys desde cualquier ventana.")
    log.info(f"   {HOTKEY_CAPTURE} → Captura completa")
    log.info(f"   {HOTKEY_REGION}  → Selección de región")
    log.info(f"   {HOTKEY_EXIT}    → Salir\n")

    # Esperar hasta que se presione el hotkey de salida
    keyboard.wait(HOTKEY_EXIT)
    log.info("👋 QuizSnap cerrado.")


if __name__ == "__main__":
    main()
