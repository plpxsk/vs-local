# AI-Powered Coding in VS Code – 100% Local, Zero External Calls

Write, refactor, and review code with AI that runs entirely on your machine. **Nothing leaves your device.**

**Integrated features:** Chat | Inline Editing | Autocomplete | Code Review | Test Generation

All powered by local LLMs through VS Code's Continue.dev extension—offline, private, and fast.

**For better model management:** Use LM Studio instead of Ollama for superior visual controls, model switching, and usage monitoring.

**Privacy-first:** Telemetry and external tracking are disabled by default. Your code stays yours.

## Quickstart

```bash
# 1. Clone and install
git clone https://github.com/your-org/on-device.git
cd on-device
pip install -e ".[dev]"

# 2. Run guided setup (installs Ollama, pulls model, configures Continue.dev)
# add --lmstudio to use it
python -m cli setup

# 3. Open in VS Code
code .
# Install the recommended Continue.dev extension when prompted

# 4. Start coding with AI
# Cmd+L (chat) | Cmd+I (inline edit) | Tab (autocomplete)
```

## What You Get

- **Chat** - Ask questions, generate code, explain code (Cmd+L)
- **Inline edit** - Select code and describe changes (Cmd+I)
- **Autocomplete** - Tab completions as you type
- **Code review** - Find bugs, security issues, code smells
- **Test generation** - Generate pytest tests from your code

All powered by local models. Nothing leaves your machine.

## Model Tiers

| Tier | Model | Download | RAM | Best For |
|------|-------|----------|-----|----------|
| small | `phi4-mini` | ~2.5 GB | 4 GB | Fast completions, low-end hardware |
| medium | `qwen2.5-coder:7b` | ~4.5 GB | 8 GB | **Recommended default** |
| large | `deepseek-coder-v2:16b` | ~9 GB | 16 GB | Highest quality |

The setup command auto-detects your RAM and recommends a tier.

## CLI Commands

```bash
python -m cli setup              # Full guided setup
python -m cli setup --lmstudio   # Use LM Studio instead of Ollama
python -m cli verify             # Health check + network audit
python -m cli models             # List model tiers and local models
python -m cli models --pull qwen2.5-coder:7b  # Pull a specific model
python -m cli config             # Regenerate Continue.dev config
python -m cli firewall           # Show firewall setup instructions
```

## Security

Three layers ensure no data leaves your machine:

1. **App config** - All API endpoints locked to `localhost`, telemetry disabled
2. **Network audit** - `python -m cli verify` checks for external connections
3. **Firewall templates** - OS-specific rules in `security/` to block outbound traffic

See [docs/SECURITY.md](docs/SECURITY.md) for details.

## Project Structure

```
cli/           CLI tool (setup, verify, models, config)
config/        Pre-built Continue.dev configuration
security/      Firewall templates and network audit script
examples/      Demo exercises and sample app
docs/          Detailed documentation
tests/         Unit tests
.vscode/       VS Code settings (telemetry off, extension recommendations)
```

## Documentation

- [Quickstart Guide](docs/QUICKSTART.md)
- [Architecture](docs/ARCHITECTURE.md)
- [Model Guide](docs/MODELS.md)
- [Security](docs/SECURITY.md)
- [Troubleshooting](docs/TROUBLESHOOTING.md)
- [LM Studio Setup](docs/LM_STUDIO.md)

## Requirements

- Python 3.10+
- 4 GB+ RAM (8 GB+ recommended)
- macOS, Linux, or Windows
- VS Code (for IDE integration)

## License

MIT
