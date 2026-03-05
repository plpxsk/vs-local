# LM Studio Setup

LM Studio is an alternative to Ollama with a graphical interface.

## Installation

1. Download from https://lmstudio.ai/
2. Install and open LM Studio
3. Search for and download a coding model (recommended: `qwen2.5-coder`)
4. Go to the **Local Server** tab
5. Load your model and click **Start Server**

The server runs at `http://localhost:1234/v1` (OpenAI-compatible API).

## Setup with CLI

```bash
python -m cli setup --lmstudio
```

This generates a Continue.dev config pointing to LM Studio's API.

Ensure LM Studio's server is running before running setup.

## Manual Config

If you prefer to configure manually, edit `~/.continue/config.json`:

```json
{
  "models": [
    {
      "title": "Local Coder (LM Studio)",
      "provider": "openai",
      "model": "your-model-name",
      "apiBase": "http://localhost:1234/v1",
      "apiKey": "lm-studio"
    }
  ],
  "tabAutocompleteModel": {
    "title": "Local Autocomplete (LM Studio)",
    "provider": "openai",
    "model": "your-model-name",
    "apiBase": "http://localhost:1234/v1",
    "apiKey": "lm-studio"
  },
  "allowAnonymousTelemetry": false
}
```

The `apiKey` field is required by the OpenAI provider but LM Studio ignores it.

## Verification

```bash
python -m cli verify --lmstudio
```

## LM Studio vs Ollama

| Feature | Ollama | LM Studio |
|---------|--------|-----------|
| Interface | CLI | GUI |
| Setup | Automated via CLI | Manual download |
| Model format | GGUF (auto-managed) | GGUF (manual download) |
| API | Custom + OpenAI-compatible | OpenAI-compatible |
| Resource usage | Lightweight | Heavier (Electron app) |
| Best for | Automation, CI/CD | Visual model management |
