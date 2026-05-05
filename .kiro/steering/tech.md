# Technology Stack

## Language & Runtime

- **Python 3.8+**: Core language
- **Execution**: Background daemon process (no console window)

## Core Dependencies

```
keyboard>=0.13.5        # Global hotkey registration across all OS
pyautogui>=0.9.54       # Screen capture (full/region)
Pillow>=10.0.0          # Image processing and base64 encoding
requests>=2.31.0        # HTTP client for AI provider APIs
python-dotenv>=1.0.0    # Environment variable management
```

## AI Providers

All providers support **vision models** with **free tiers**:

| Provider | Model | Endpoint |
|----------|-------|----------|
| Google Gemini | `gemini-1.5-flash` | `generativelanguage.googleapis.com` |
| OpenRouter | `meta-llama/llama-4-maverick:free` | `openrouter.ai/api/v1` |
| Groq | `meta-llama/llama-4-scout-17b-16e-instruct` | `api.groq.com/openai/v1` |

## Architecture Patterns

- **Round-robin load balancing**: Distributes requests across providers
- **Automatic failover**: If provider fails (rate limit, network error), next provider handles request
- **Threaded execution**: Capture/processing runs in background threads to avoid blocking hotkey listener
- **Mutex locking**: Prevents concurrent processing of multiple captures

## Configuration

- **`.env` file**: All API keys, hotkeys, and behavior settings
- **No hardcoded credentials**: Everything configurable without code changes

## Common Commands

### Installation
```bash
pip install -r requirements.txt
```

### Run Application
```bash
python quiz_solver.py
```

**Windows**: Run with `pythonw.exe quiz_solver.py` to hide console window

**Linux**: May require `sudo` for global hotkey permissions:
```bash
sudo python quiz_solver.py
```

### Testing Individual Components
```python
# Test screen capture
python -c "import pyautogui; pyautogui.screenshot().show()"

# Test API key (Gemini example)
python -c "from dotenv import load_dotenv; import os; load_dotenv(); print('Key loaded' if os.getenv('GEMINI_API_KEY') else 'Missing')"
```

## Platform-Specific Notes

- **Windows**: Requires Administrator privileges for global hotkeys
- **Linux**: Needs `python3-tk` and `xclip` packages
- **macOS**: Requires Accessibility permissions in System Preferences

## Logging

- **Console output**: Real-time status messages
- **File logging**: `quizsnap.log` with timestamps and error details
- **Log level**: Configurable via environment (INFO by default)
