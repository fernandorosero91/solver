# Project Structure

## Current Architecture

QuizSnap uses a **monolithic single-file architecture** for simplicity and portability.

```
quizsnap/
├── quiz_solver.py           # Main application (all functionality)
├── quizsnap_prompt.md       # Technical specification document
├── requirements.txt         # Python dependencies
├── .env                     # Configuration (API keys, hotkeys)
├── README.md                # User documentation
└── quizsnap.log             # Runtime logs (generated)
```

## Main Application Structure (`quiz_solver.py`)

The file is organized into logical sections with clear separators:

```python
# 1. Imports and logging setup
# 2. Environment configuration (API keys, hotkeys, models)
# 3. System prompt for AI
# 4. Screen capture functions
#    - capture_fullscreen()
#    - capture_region()
#    - image_to_base64()
# 5. AI provider functions
#    - query_gemini()
#    - query_openrouter()
#    - query_groq()
# 6. Load balancer
#    - PROVIDERS list
#    - get_next_provider()
#    - solve_with_ai()
# 7. Result window (tkinter UI)
#    - show_result()
# 8. Hotkey handlers
#    - handle_capture()
#    - handle_region()
# 9. Main entry point
#    - check_api_keys()
#    - print_banner()
#    - main()
```

## Code Organization Principles

- **Top-to-bottom flow**: Configuration → Utilities → Core Logic → UI → Entry Point
- **Section separators**: ASCII art dividers mark major sections
- **Self-contained functions**: Each function handles one responsibility
- **Global state**: Minimal (only `_provider_index` and `_processing` flag with locks)

## Configuration Files

### `.env` (user-created)
```
GEMINI_API_KEY=...
OPENROUTER_API_KEY=...
GROQ_API_KEY=...
HOTKEY_CAPTURE=ctrl+shift+q
HOTKEY_REGION=ctrl+shift+w
HOTKEY_EXIT=ctrl+shift+x
```

### `requirements.txt`
Lists all Python dependencies with version constraints.

## Documentation Files

- **`README.md`**: User-facing installation and usage guide (Spanish)
- **`quizsnap_prompt.md`**: Comprehensive technical specification for developers

## Generated Files

- **`quizsnap.log`**: Timestamped application logs (INFO level by default)

## Design Rationale

**Why single-file?**
- Easy deployment (copy one file + requirements.txt)
- No import path issues
- Simple debugging (everything in one place)
- Suitable for ~500 LOC application

**When to refactor into modules:**
- If file exceeds 1000 lines
- If adding new capture methods or UI modes
- If implementing plugin system for additional AI providers
- If building installer/packager (PyInstaller, etc.)

## Potential Module Structure (Future)

```
quizsnap/
├── quizsnap/
│   ├── __init__.py
│   ├── config.py           # Environment and constants
│   ├── capture.py          # Screen capture logic
│   ├── providers.py        # AI provider implementations
│   ├── balancer.py         # Load balancing and failover
│   ├── ui.py               # Result window and tray icon
│   └── main.py             # Entry point and hotkey handlers
├── requirements.txt
├── .env
└── README.md
```

## Naming Conventions

- **Functions**: `snake_case` (e.g., `capture_fullscreen`, `query_gemini`)
- **Constants**: `UPPER_SNAKE_CASE` (e.g., `GEMINI_API_KEY`, `SYSTEM_PROMPT`)
- **Private globals**: Leading underscore (e.g., `_provider_index`, `_processing`)
- **Locks**: Descriptive names with `_lock` suffix (e.g., `_processing_lock`)
