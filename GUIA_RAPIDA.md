# 🚀 Guía Rápida - QuizSnap

## ✅ Estado de la Instalación

- [x] Entorno virtual creado (`venv/`)
- [x] Dependencias instaladas
- [x] Archivo `.env` creado
- [ ] **API Keys configuradas** ← **PENDIENTE**

---

## 📋 Próximos Pasos

### 1. Obtener API Keys (Elige al menos UNA)

#### Opción A: Google Gemini (⭐ Recomendado)
```
1. Ve a: https://aistudio.google.com/app/apikey
2. Inicia sesión con Google
3. Clic en "Create API Key"
4. Copia la key
```

#### Opción B: OpenRouter
```
1. Ve a: https://openrouter.ai/keys
2. Crea cuenta (Google/GitHub)
3. Clic en "Create Key"
4. Copia la key
```

#### Opción C: Groq
```
1. Ve a: https://console.groq.com/keys
2. Crea cuenta
3. Clic en "Create API Key"
4. Copia la key
```

### 2. Configurar el archivo `.env`

Abre el archivo `.env` y pega tu(s) API key(s):

```env
GEMINI_API_KEY=tu_key_aqui
OPENROUTER_API_KEY=tu_key_aqui
GROQ_API_KEY=tu_key_aqui
```

### 3. Iniciar la Aplicación

#### Opción A: Usando el script (Recomendado)
```bash
start_quizsnap.bat
```

#### Opción B: Manual
```bash
venv\Scripts\activate
python quiz_solver.py
```

#### Opción C: Como Administrador (para hotkeys globales)
```
1. Clic derecho en start_quizsnap.bat
2. "Ejecutar como administrador"
```

---

## 🎮 Uso

Una vez iniciada la aplicación:

| Hotkey | Acción |
|--------|--------|
| `Ctrl+Shift+Q` | Captura pantalla completa y resuelve |
| `Ctrl+Shift+W` | Selecciona región con el mouse |
| `Ctrl+Shift+X` | Salir |

### Ejemplo de Flujo:
1. Abre un cuestionario en tu navegador
2. Presiona `Ctrl+Shift+Q`
3. Espera 2-5 segundos
4. Aparece una ventana con la respuesta
5. Lee la respuesta y cierra con `ESC`

---

## 🔧 Solución de Problemas

### Error: "No hay ninguna API key configurada"
- Verifica que hayas pegado al menos UNA key en el archivo `.env`
- Asegúrate de que no haya espacios antes o después de la key

### Los hotkeys no funcionan
- Ejecuta la aplicación como **Administrador** (Windows)
- Verifica que no haya otra aplicación usando las mismas combinaciones

### Error de permisos en Linux
```bash
sudo python quiz_solver.py
```

### La ventana de resultado no aparece
- Verifica que tengas `python3-tk` instalado (Linux)
- Revisa el archivo `quizsnap.log` para ver errores

---

## 📊 Verificación del Sistema

### Verificar Python
```bash
python --version
# Debe ser 3.8 o superior
```

### Verificar dependencias
```bash
venv\Scripts\activate
pip list
```

### Probar captura de pantalla
```bash
venv\Scripts\activate
python -c "import pyautogui; pyautogui.screenshot().show()"
```

### Verificar API Key (ejemplo con Gemini)
```bash
venv\Scripts\activate
python -c "from dotenv import load_dotenv; import os; load_dotenv(); print('✓ Key cargada' if os.getenv('GEMINI_API_KEY') else '✗ Key no encontrada')"
```

---

## 📝 Logs

Los logs se guardan en: `quizsnap.log`

Para ver los últimos logs:
```bash
type quizsnap.log
```

---

## 🎯 Resumen de Archivos

```
quizsnap/
├── venv/                    # Entorno virtual (creado ✓)
├── quiz_solver.py           # Aplicación principal
├── requirements.txt         # Dependencias
├── .env                     # Configuración (EDITAR AQUÍ)
├── start_quizsnap.bat       # Script de inicio rápido
├── GUIA_RAPIDA.md          # Este archivo
├── README.md               # Documentación completa
└── quizsnap.log            # Logs (se crea al ejecutar)
```

---

## 💡 Consejos

1. **Configura las 3 API keys** para máxima resiliencia
2. **Ejecuta como Administrador** en Windows para hotkeys globales
3. **Usa `Ctrl+Shift+W`** para seleccionar solo la pregunta (más preciso)
4. **Revisa `quizsnap.log`** si algo no funciona
5. **Cierra con `Ctrl+Shift+X`** para salir limpiamente

---

## 🆘 Soporte

Si tienes problemas:
1. Revisa `quizsnap.log`
2. Verifica que las API keys sean válidas
3. Asegúrate de tener permisos de Administrador (Windows)
4. Consulta el README.md para más detalles

---

**¡Listo para usar! 🎉**

Configura tu API key y ejecuta `start_quizsnap.bat`
