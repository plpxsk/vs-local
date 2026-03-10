# Use local LLMs in VS Code – 100% Local, Zero External Calls

Write, refactor, and review code with AI that runs entirely on your machine. **Nothing leaves your device.**

**Integrated features:** Chat | Inline Editing | Autocomplete | Code Review | Test Generation

**Privacy-first:** Telemetry and external tracking are disabled by default. Your code stays yours.

All powered by local LLMs through VS Code's Continue.dev extension—offline, private, and fast.


_Note: we provide no guarantees on security, but turn off Wifi on your macbook to confirm ;)_

# Quickstart

## Install

_Use the **LM Studio** setup option, instead of Ollama, for superior visual control, model switching, and usage monitoring._

_Prerequisites: Install [Ollama](https://ollama.com) or [LM Studio](https://lmstudio.ai), Python 3.10+, VS Code, 8 GB+ RAM recommended (4 GB minimum)_



```bash
# clone and install (into a virtual env)
git clone https://github.com/plpxsk/vs-local.git
cd vs-local
pip install -e .

# 2. Run guided setup — prompts you to choose Ollama or LM Studio
python -m cli setup

# 3. Open in VS Code and install the Continue.dev extension when prompted
code . # or open project in VSCode

# 4. Start coding with AI: Cmd+L (chat) | Cmd+I (inline edit) | Tab (autocomplete)
```

Setup will: detect OS and RAM, recommend a model tier (default small = `phi4-mini`), check or install Ollama, pull the model, generate a Continue.dev config locked to localhost, and optionally install it to `~/.continue/` (prompts before overwriting). If `~/.continue/config.json` already exists, use `--force` to overwrite without prompting.

For help selecting local models, see below, [Model Tiers](#model-tiers).

To verify install, run: `python -m cli verify`

## Use in your own project

After setup, the Continue.dev config is global and works in any repo. To also copy the VS Code privacy settings into your project:

```bash
# activate venv as needed
cd /path/to/your-project
python -m cli vscode-init
```

## Usage

Run the app with `python -m cli`

```bash
python -m cli setup              # Full guided setup (prompts for runtime)
python -m cli setup --lmstudio   # Skip prompt, use LM Studio
python -m cli verify             # Health check + network audit
python -m cli models             # List model tiers and local models
python -m cli models --pull qwen2.5-coder:7b  # Pull a specific model
python -m cli config             # Regenerate Continue.dev config
python -m cli firewall           # Show firewall setup instructions
python -m cli vscode-init        # Copy VS Code settings into current project
```

## Examples

See `examples/` for exercises (code generation, refactoring, code review, test generation). Troubleshooting: [docs/TROUBLESHOOTING.md](docs/TROUBLESHOOTING.md).

# What You Get

- **Chat** - Ask questions, generate code, explain code (Cmd+L)
- **Inline edit** - Select code and describe changes (Cmd+I)
- **Autocomplete** - Tab completions as you type
- **Code review** - Find bugs, security issues, code smells
- **Test generation** - Generate pytest tests from your code

All powered by local models. Nothing leaves your machine.

# Model Tiers

| Tier | Model | Download | RAM | Best For |
|------|-------|----------|-----|----------|
| small | `phi4-mini` | ~2.5 GB | 4 GB | Fast completions, low-end hardware |
| medium | `qwen2.5-coder:7b` | ~4.5 GB | 8 GB | **Recommended default** |
| large | `deepseek-coder-v2:16b` | ~9 GB | 16 GB | Highest quality |

The setup command auto-detects your RAM and _recommends a tier_.

# Security

Three layers ensure no data leaves your machine:

1. **App config** - All API endpoints locked to `localhost`, telemetry disabled
2. **Network audit** - `python -m cli verify` checks for external connections
3. **Firewall templates** - OS-specific rules in `security/` to block outbound traffic

See [docs/SECURITY.md](docs/SECURITY.md) for details.

# Learn more

- [Models](docs/MODELS.md) — Model tiers, hardware requirements, and top picks
- [Runtimes](docs/RUNTIMES.md) — Ollama vs LM Studio vs MLX
- [Security](docs/SECURITY.md)
- [Troubleshooting](docs/TROUBLESHOOTING.md)


# License

MIT
