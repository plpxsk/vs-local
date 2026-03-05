# Quickstart Guide

Get productive with vs-local — local AI coding in VS Code — in under 5 minutes.

## Prerequisites

- Python 3.10+
- VS Code
- 8 GB+ RAM recommended (4 GB minimum)

## Step 1: Install

```bash
git clone https://github.com/plpxsk/vs-local.git
cd vs-local
pip install -e .
```

## Step 2: Setup

```bash
python -m cli setup
```

This will:
1. Detect your OS and available RAM
2. **Prompt you to choose a model tier** (small / medium / large, with a recommendation based on your RAM)
3. **Prompt you to confirm the model** to download — or type a custom model name
4. **Prompt you to choose a runtime** (Ollama or LM Studio)
5. Check that the chosen runtime is available (and guide you if not)
6. Pull the selected model (Ollama only)
7. Generate a Continue.dev config locked to localhost
8. Run a verification check

## Step 3: Open in VS Code

```bash
code .
```

When prompted, install the recommended **Continue.dev** extension.

## Step 4: Start Using

### Chat (Cmd+L / Ctrl+L)
Ask questions, generate code, or explain existing code.

### Inline Edit (Cmd+I / Ctrl+I)
Select code, describe what you want changed. The model edits in-place.

### Autocomplete (Tab)
Get completions as you type. A smaller model handles autocomplete for speed.

## Step 5: Verify

```bash
python -m cli verify
```

Confirms the server is running, model is loaded, inference works, and no external network calls are detected.

## Use in Your Own Project

The Continue.dev config (`~/.continue/config.json`) is global and already works in any VS Code project after setup.

To also apply the VS Code privacy settings (telemetry off, no auto-updates) to your own repo:

**Option A — CLI:**
```bash
cd /path/to/your-project
python -m cli vscode-init
```

**Option B — Manual:** Copy these two files into your project's `.vscode/` folder:

`.vscode/settings.json`:
```json
{
  "telemetry.telemetryLevel": "off",
  "http.proxySupport": "off",
  "extensions.autoCheckUpdates": false,
  "extensions.autoUpdate": false,
  "update.mode": "none"
}
```

`.vscode/extensions.json`:
```json
{
  "recommendations": ["continue.continue"]
}
```

> The `python.defaultInterpreterPath` line from vs-local's own settings is omitted here — add it back if your project also uses `.venv`.

## Try the Examples

Work through the demo exercises in `examples/`:

1. [Code Generation](../examples/01_code_generation.md) - Generate a CSV parser
2. [Refactoring](../examples/02_refactoring.md) - Clean up messy code
3. [Code Review](../examples/03_code_review.md) - Find bugs and vulnerabilities
4. [Test Generation](../examples/04_test_generation.md) - Generate pytest tests

## Troubleshooting

See [TROUBLESHOOTING.md](TROUBLESHOOTING.md) for common issues.
