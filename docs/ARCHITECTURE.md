# Architecture

## Overview

```
User -> VS Code + Continue.dev -> Ollama (or LM Studio) -> Local Model
```

Everything runs on your machine. No cloud APIs, no telemetry, no external network calls.

## Components

### Ollama (Default Runtime)
- Runs models locally via a REST API at `http://localhost:11434`
- Manages model downloads, quantization, and inference
- Cross-platform (macOS, Linux, Windows)

### LM Studio (Alternative)
- GUI-based model management
- OpenAI-compatible API at `http://localhost:1234/v1`
- Good for users who prefer a visual interface

### Continue.dev (VS Code Extension)
- Open-source AI coding assistant
- Connects to local Ollama/LM Studio
- Provides chat, inline edit, and autocomplete
- Config at `~/.continue/config.json`

### CLI Tool
- Python CLI built with Typer
- Handles setup, verification, model management
- Generates Continue.dev config locked to localhost
- Runs network audits to verify no external calls

## Data Flow

1. User types in VS Code (chat, inline edit, or autocomplete trigger)
2. Continue.dev extension formats the prompt with code context
3. Request sent to `localhost:11434` (Ollama) or `localhost:1234` (LM Studio)
4. Model runs inference on local GPU/CPU
5. Response streamed back to Continue.dev
6. Result displayed in VS Code

## Security Layers

1. **Application config** - API endpoints locked to localhost, telemetry off
2. **Network verification** - CLI audit checks for external connections
3. **OS firewall** - Templates to block outbound traffic for LLM processes

## Key Decisions

| Decision | Choice | Rationale |
|----------|--------|-----------|
| Runtime | Ollama (default) | Cross-platform, easy CLI, active community |
| VS Code integration | Continue.dev | Open-source, native Ollama support |
| CLI framework | Typer (Python) | Minimal dependencies, great UX |
| Default model | qwen2.5-coder:7b | Best quality/size ratio for coding |
| Security | 3-layer defense | Defense in depth for air-gap guarantee |
