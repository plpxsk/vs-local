# Troubleshooting

## Ollama Issues

### "Ollama not found"
Install Ollama:
- **macOS**: `brew install ollama` or download from https://ollama.com/download/mac
- **Linux**: `curl -fsSL https://ollama.com/install.sh | sh`
- **Windows**: Download from https://ollama.com/download/windows

### "Ollama server not responding"
Start the server:
```bash
ollama serve
```
Or on macOS, open the Ollama app.

### Model pull fails
Check disk space. The 7B model needs ~4.5 GB free.
```bash
df -h .
ollama pull qwen2.5-coder:7b
```

### Slow inference
- Check RAM: `python -m cli setup` shows your RAM
- Try a smaller model: `python -m cli setup --tier small`
- Close other memory-intensive apps
- On macOS, ensure Ollama is using the GPU (it does by default on Apple Silicon)

## Continue.dev Issues

### Extension not working
1. Ensure Continue.dev is installed: check Extensions panel in VS Code
2. Verify config: `cat ~/.continue/config.json`
3. Regenerate: `python -m cli config --install`

### "Could not connect to Ollama"
1. Check Ollama is running: `curl http://localhost:11434/api/tags`
2. Regenerate config: `python -m cli config --install`
3. Restart VS Code

### Autocomplete not working
1. Check the autocomplete model is pulled: `ollama list`
2. Pull if missing: `ollama pull qwen2.5-coder:1.5b`
3. Verify config has `tabAutocompleteModel` section

## Verification Issues

### "Telemetry endpoints reachable"
This is a warning, not a blocker. For maximum security, apply firewall rules:
```bash
python -m cli firewall
```

### "Non-localhost connections detected"
Check which process is making external connections:
```bash
lsof -i -n -P | grep -i ollama
```
Apply firewall rules to block external traffic.

## General

### Reset everything
```bash
# Regenerate config
python -m cli config --install

# Re-run setup
python -m cli setup

# Verify
python -m cli verify
```

### Check Python version
```bash
python --version  # Needs 3.10+
```

### Reinstall CLI
```bash
pip install -e ".[dev]"
```
