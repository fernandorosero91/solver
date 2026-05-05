# Product Overview

**QuizSnap** is a background desktop application that captures quiz questions from any window using global hotkeys and returns AI-powered answers instantly.

## Core Functionality

- **Global hotkey capture**: Works from any application (browser, PDF, Teams, Zoom)
- **Two capture modes**: Full screen or mouse-selected region
- **AI-powered solving**: Analyzes multiple-choice questions using vision-capable AI models
- **Non-intrusive UX**: Floating result window that doesn't steal focus
- **Multi-provider resilience**: Automatic failover between 3 AI providers (Gemini, OpenRouter, Groq)

## Target Use Case

Students or professionals taking online quizzes/exams who need quick answers without leaving their current application. The tool runs silently in the background and activates only when hotkeys are pressed.

## Key Design Principles

- **Invisibility**: No main window, runs as background daemon
- **Speed**: < 5 seconds from capture to answer
- **Reliability**: Round-robin load balancing with automatic failover
- **Accessibility**: All providers have free tiers, configurable via `.env`
