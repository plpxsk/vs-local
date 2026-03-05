# Quickstart Guide

Get productive with on-device AI coding in under 5 minutes.

## Prerequisites

- Python 3.10+
- VS Code
- 8 GB+ RAM recommended (4 GB minimum)

## Step 1: Install

```bash
git clone https://github.com/your-org/on-device.git
cd on-device
pip install -e ".[dev]"
```

## Step 2: Setup

```bash
python -m cli setup
```

This will:
1. Detect your OS and available RAM
2. Recommend a model tier based on your hardware
3. Check that Ollama is installed (and guide you if not)
4. Pull the recommended coding model
5. Generate a Continue.dev config locked to localhost
6. Run a verification check

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

## Try the Examples

Work through the demo exercises in `examples/`:

1. [Code Generation](../examples/01_code_generation.md) - Generate a CSV parser
2. [Refactoring](../examples/02_refactoring.md) - Clean up messy code
3. [Code Review](../examples/03_code_review.md) - Find bugs and vulnerabilities
4. [Test Generation](../examples/04_test_generation.md) - Generate pytest tests

## Troubleshooting

See [TROUBLESHOOTING.md](TROUBLESHOOTING.md) for common issues.
