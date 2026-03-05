# Project Review: Local LLM Setup for VS Code

This document summarizes a review of the repo with focus on **getting started quickly**, **implementation**, **simplification**, and **refactoring**.

---

## What Works Well

- **Clear value proposition**: 100% local, zero external calls, well documented.
- **Single-command setup**: `python -m cli setup` (or `on-device setup`) drives runtime + model + Continue.dev config.
- **Dual runtime support**: Ollama (default) and LM Studio with consistent CLI flags (`--lmstudio`).
- **Verification pipeline**: `verify` checks server, model, inference, and network audit in one place.
- **Modular CLI**: `detect`, `models`, `ollama`, `lmstudio`, `verify`, `continue_config`, `firewall` are focused and testable.
- **Security story**: Localhost-only config, telemetry off, optional firewall templates.
- **Tests**: Core logic is covered with mocks; tests are clear and runnable.

---

## 1. Naming and Branding Consistency

**Issue:** The project uses two names: **vs-local** (repo/README) and **on-device** (package, CLI, script). Docs say `python -m cli`; the package also installs a script `on-device`.

**Suggestions:**

- **Pick one product name** (e.g. `vs-local` or `on-device`) and use it everywhere: `pyproject.toml` name, CLI `name=`, README, and any “On-Device LLM” copy.
- **Single recommended entrypoint** in docs:
  - Either: `pip install -e ".[dev]"` then **`python -m cli setup`** (no script),  
  - Or: **`on-device setup`** (script) and mention `python -m cli` as alternative.
- Align **project name** in `pyproject.toml` with the repo name if you want “clone vs-local → run vs-local” to feel consistent.

---

## 2. Implementation Fixes

### 2.1 Tier validation

**Issue:** `setup --tier foo` calls `models.get_model("foo")`, which does `TIERS["foo"]` and raises `KeyError` for invalid tiers.

**Fix:** Validate `--tier` and fail with a clear message:

```python
# In main.py setup():
VALID_TIERS = set(models.get_all_models())
if tier and tier not in VALID_TIERS:
    console.print(f"[red]Invalid tier: {tier}. Choose from: {', '.join(sorted(VALID_TIERS))}[/red]")
    raise typer.Exit(1)
```

Optionally add `get_model(tier: str) -> ModelInfo | None` or a dedicated `validate_tier(tier: str) -> bool` in `models.py` and use it from the CLI.

### 2.2 Model tier docs vs code

**Issue:** `docs/MODELS.md` says small tier is `qwen2.5-coder:1.5b`; `cli/models.py` (and README table) use `phi4-mini` for small. Autocomplete is `qwen2.5-coder:1.5b` in code, which matches MODELS.md for autocomplete but not for the “small” chat tier.

**Fix:** Either:
- Update **MODELS.md** so the “small” row matches `models.py` (e.g. `phi4-mini`, ~2.5 GB), and keep “Autocomplete model” as `qwen2.5-coder:1.5b`, or  
- Change **models.py** so the small tier is `qwen2.5-coder:1.5b` and adjust README/MODELS.md accordingly.

Choose one source of truth (code) and make docs match.

### 2.3 `install_to_home` overwrites user config

**Issue:** `install_to_home()` renames existing `~/.continue/config.json` to `config.json.backup` and writes the new config. That’s destructive if the user had a custom setup and ran `setup` or `config --install` without realizing.

**Suggestions:**

- **Prompt before overwrite** when `config_path.exists()` (e.g. “Overwrite ~/.continue/config.json? [y/N]”) unless a `--force` / `--yes` flag is set.
- **Merge instead of replace** (advanced): e.g. only set `models`, `tabAutocompleteModel`, and `allowAnonymousTelemetry` while leaving other keys intact. Document this behavior.
- At minimum, **document** in README and in `config --install` help that installing to home backs up and replaces the file.

### 2.4 `models` command and LM Studio

**Issue:** `models` only lists/pulls **Ollama** models. With `setup --lmstudio`, users never pull via this repo; that’s correct. But `python -m cli models` still says “Local models:” and only shows `ollama.list_local_models()`, which can be empty or misleading when the user is on LM Studio.

**Suggestion:** If `--lmstudio` is not passed, keep current behavior. Optionally: add `models --lmstudio` that lists `lmstudio.list_models()` and in the default `models` output add one line when no local Ollama models are found: “Using LM Studio? Start server and load a model in the app; use `config --lmstudio` to generate Continue config.”

---

## 3. Simplification

### 3.1 Fewer entrypoints in docs

- **One canonical way** to run: e.g. “Install: `pip install -e .` then run `python -m cli setup`” (or “run `on-device setup`”). Mention the other form only as an alternative.
- **Quickstart in one block**: Clone → install → `setup` → `code .` → install Continue. Keep “Verify” and “Try the examples” as next steps so the “get started in 5 minutes” path is a single copy-paste.

### 3.2 Optional security

- **Default path**: No firewall; just localhost config + verify. That’s enough for “nothing leaves my machine” for the app itself.
- **Firewall**: Keep as optional, documented under Security/Advanced. Avoid making firewall setup part of the minimal quickstart so “get started quickly” stays true.

### 3.3 Config output location

- Today: config is written to **repo** `config/continue/config.json` and optionally to **home** `~/.continue/config.json`.
- Simplification: Either “config only in repo” (user copies or symlinks) or “config only in home” (so one place to look). Supporting both is fine but document the recommended flow (e.g. “we write to repo; use `config --install` to copy to ~/.continue for all projects”).

### 3.4 Default verify model

- `verify` defaults to `--model qwen2.5-coder:7b`. If the user ran `setup --tier small`, they have `phi4-mini`; verify then checks a model they might not have pulled.
- **Suggestion:** Default `verify --model` to the same model that would be recommended by `detect.recommend_tier(get_ram_gb())` (or the model from the last `setup`). Alternatively, document that after `setup --tier small` they should run `verify --model phi4-mini`.

---

## 4. Refactoring

### 4.1 Runtime abstraction

**Current:** `main.py` and `verify.py` branch on `use_lmstudio` and call `ollama.*` or `lmstudio.*` directly.

**Idea:** Introduce a small runtime abstraction so the rest of the code talks to “a runtime” instead of Ollama vs LM Studio:

- `cli/runtime.py`: define a protocol or abstract class with `is_available()`, `is_running()`, `install_instructions()`, `list_models()`, `test_inference(model?)`, and optionally `start_server()`, `pull_model(name)` (no-op for LM Studio).
- `ollama.py` and `lmstudio.py` implement that interface; `main.py` and `verify.py` receive “runtime” and call one set of methods.

**Benefit:** Adding a third backend (e.g. MLX server) is one new implementation and a flag; no branching in `main`/`verify`.

### 4.2 Config generation and install

- **Split “generate config” from “write to disk”**: Already mostly done (`generate_config` vs `write_config` + `install_to_home`). You could go one step further: a small `ConfigWriter` or functions that take “target: repo | home | both” and “overwrite: bool” so all behaviors (prompt, merge, backup) live in one place.
- **Continue config schema**: If the format grows, consider a dataclass or Pydantic model for the config and serialize to JSON from that (one place to validate and document shape).

### 4.3 Detect and models

- **RAM fallback:** `detect.get_ram_gb()` can return `0.0`; `recommend_tier(0)` returns `"small"`. That’s safe but you could explicitly treat `ram_gb < 4` as “unknown, default to small” and log a warning in setup.
- **get_model:** Add `get_model_or_default(tier: str | None) -> ModelInfo` that returns `TIERS.get(tier, TIERS[DEFAULT_TIER])` (or validate and raise) so CLI has one function for “resolve tier to ModelInfo”.

---

## 5. Quick Wins for “Get Started Quickly”

1. **README:** One copy-paste block: clone → `pip install -e ".[dev]"` → `python -m cli setup` → `code .` → install Continue. Then “Next: run `python -m cli verify`.”
2. **Unify naming:** One product name and one primary command form in all docs.
3. **Validate `--tier`** and align MODELS.md with `models.py` so the small tier is unambiguous.
4. **Document** that `config --install` overwrites (and backs up) `~/.continue/config.json`; optionally add a prompt or `--force`.
5. **Verify default model:** Either derive from recommended tier or document `verify --model <your-model>` after setup.

---

## 6. Summary Table

| Area              | Suggestion                                      | Effort |
|-------------------|--------------------------------------------------|--------|
| Naming            | Single product name + one canonical CLI form    | Low    |
| Implementation    | Validate `--tier`; fix MODELS.md vs models.py   | Low    |
| Implementation    | Safer or documented `install_to_home`           | Low    |
| Simplification    | One quickstart block; optional firewall         | Low    |
| Simplification    | Verify default model aligned with tier          | Low    |
| Refactor          | Runtime abstraction for Ollama/LM Studio/MLX    | Medium |
| Refactor          | Config dataclass + single “write/install” flow   | Medium |

Implementing the low-effort items will already improve clarity and safety. The refactors pay off if you add more runtimes or more config options later.
