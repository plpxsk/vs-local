"""Typer CLI app: setup, verify, models, config commands."""

from pathlib import Path
from typing import Optional
import click
import typer
from rich.console import Console
from rich.table import Table
from rich.panel import Panel

from cli import detect, models, ollama, lmstudio, verify, firewall
from cli.continue_config import generate_config, write_config, install_to_home

app = typer.Typer(
    name="vs-local",
    help="vs-local: local LLM for software development in VS Code. Zero external network calls.",
)
console = Console()


@app.command()
def setup(
    use_lmstudio: Optional[bool] = typer.Option(
        None, "--lmstudio", help="Use LM Studio instead of Ollama (skips prompt)"
    ),
    tier: str = typer.Option(
        "", "--tier", help="Model tier: small, medium, large (auto-detected if empty). Ollama only, ignored for LM Studio."
    ),
    skip_pull: bool = typer.Option(
        False, "--skip-pull", help="Skip model download"
    ),
    force: bool = typer.Option(
        False, "--force", help="Overwrite ~/.continue/config.json without prompting"
    ),
):
    """Full guided setup: runtime + model + Continue.dev config."""
    console.print(Panel("vs-local Setup", style="bold blue"))

    # Step 1: Detect OS and RAM
    os_name = detect.get_os()
    ram_gb = detect.get_ram_gb()
    console.print(f"  OS: {os_name}")
    console.print(f"  RAM: {ram_gb:.1f} GB")

    # Step 2: Select runtime
    if use_lmstudio is None:
        choice = click.prompt(
            "\nSelect runtime",
            type=click.Choice(["ollama", "lmstudio"]),
            default="ollama",
        )
        use_lmstudio = choice == "lmstudio"

    # Step 3: Select model tier and model (Ollama only)
    if not use_lmstudio:
        valid_tiers = set(models.get_all_models())
        if tier and tier not in valid_tiers:
            console.print(
                f"[red]Invalid tier: {tier}. Choose from: {', '.join(sorted(valid_tiers))}[/red]"
            )
            raise typer.Exit(1)
        recommended = detect.recommend_tier(ram_gb)
        if not tier:
            console.print("")
            for t, info in models.get_all_models().items():
                tag = "  ← recommended" if t == recommended else ""
                console.print(f"  {t:<8} {info.name:<30} ~{info.size_gb:.1f} GB  {info.min_ram_gb} GB RAM{tag}")
            tier = click.prompt(
                "\nSelect tier",
                type=click.Choice(list(models.get_all_models())),
                default=recommended,
            )
        model_info = models.get_model(tier)

    # Step 4: Check/install runtime
    if use_lmstudio:
        console.print("\n[bold]Checking LM Studio...[/bold]")
        if not lmstudio.is_running():
            console.print("[yellow]LM Studio server not detected.[/yellow]")
            console.print(lmstudio.install_instructions())
            raise typer.Exit(1)
        console.print("[green]LM Studio is running.[/green]")
        loaded = lmstudio.list_models()
        if loaded:
            model_name = loaded[0]
            console.print(f"  Using model: {model_name}")
        else:
            console.print("[yellow]No models loaded in LM Studio. Load a model and restart.[/yellow]")
            raise typer.Exit(1)
    else:
        console.print("\n[bold]Checking Ollama...[/bold]")
        if not ollama.is_installed():
            console.print("[yellow]Ollama not found.[/yellow]")
            console.print(ollama.install_instructions(os_name))
            raise typer.Exit(1)
        console.print("[green]Ollama is installed.[/green]")

        if not ollama.is_running():
            console.print("  Starting Ollama server...")
            proc = ollama.start_server()
            if not ollama.is_running():
                console.print("[red]Failed to start Ollama. Run 'ollama serve' manually.[/red]")
                raise typer.Exit(1)
        console.print("[green]Ollama server is running.[/green]")

        model_name = click.prompt(
            "\nModel to download (press Enter to confirm, or type a custom name)",
            default=model_info.name,
        )

        # Step 5: Pull model
        if not skip_pull:
            local = ollama.list_local_models()
            needed = [model_name]
            if models.AUTOCOMPLETE_MODEL not in [model_name]:
                needed.append(models.AUTOCOMPLETE_MODEL)

            for m in needed:
                if m not in local:
                    console.print(f"\n  Pulling {m}... (this may take a while)")
                    if not ollama.pull_model(m):
                        console.print(f"[red]Failed to pull {m}[/red]")
                        raise typer.Exit(1)
                    console.print(f"  [green]{m} pulled successfully.[/green]")
                else:
                    console.print(f"  {m} already available.")

    # Step 6: Generate Continue.dev config
    console.print("\n[bold]Generating Continue.dev config...[/bold]")
    provider = "lmstudio" if use_lmstudio else "ollama"
    config = generate_config(model_name, provider=provider)
    repo_path = write_config(config)
    console.print(f"  Config written to: {repo_path}")

    continue_home = Path.home() / ".continue" / "config.json"
    overwrite_home = force or not continue_home.exists()
    if not overwrite_home:
        overwrite_home = typer.confirm(
            "Overwrite ~/.continue/config.json? (existing file will be backed up)",
            default=False,
        )
    if overwrite_home:
        home_path = install_to_home(config, overwrite=True)
        if home_path:
            console.print(f"  Config installed to: {home_path}")

    # Step 7: Verify
    console.print("\n[bold]Running verification...[/bold]")
    if use_lmstudio:
        console.print("  [dim]Inference test will call LM Studio — check the app if this hangs.[/dim]")
    report = verify.run_all(model_name, use_lmstudio=use_lmstudio)
    _print_report(report)

    if report.all_passed:
        console.print("\n[bold green]Setup complete![/bold green]")
    else:
        console.print("\n[bold yellow]Setup completed with warnings. See above.[/bold yellow]")
    console.print(
        "\nTo use in your own project:\n"
        "  1. Open any repo in VS Code — Continue.dev is already configured globally.\n"
        "  2. Optionally copy VS Code settings (security, telemetry off) into that repo:\n"
        "       cd /path/to/your-project && python -m cli vscode-init\n"
        "  3. Chat: Cmd+L  |  Inline edit: Cmd+I  |  Autocomplete: Tab"
    )


@app.command(name="verify")
def verify_cmd(
    use_lmstudio: bool = typer.Option(False, "--lmstudio", help="Check LM Studio instead of Ollama"),
    model: str = typer.Option("phi4-mini", "--model", help="Model to verify"),
):
    """Health check: server, model, inference, network audit."""
    console.print(Panel("Verification", style="bold blue"))
    report = verify.run_all(model, use_lmstudio=use_lmstudio)
    _print_report(report)
    if not report.all_passed:
        raise typer.Exit(1)


@app.command(name="models")
def models_cmd(
    pull: str = typer.Option("", "--pull", help="Pull a specific model by name"),
):
    """List available model tiers or pull a model."""
    if pull:
        console.print(f"Pulling {pull}...")
        if ollama.pull_model(pull):
            console.print(f"[green]{pull} pulled successfully.[/green]")
        else:
            console.print(f"[red]Failed to pull {pull}[/red]")
            raise typer.Exit(1)
        return

    table = Table(title="Model Tiers")
    table.add_column("Tier", style="bold")
    table.add_column("Model")
    table.add_column("Size")
    table.add_column("Min RAM")
    table.add_column("Description")

    for tier_name, info in models.get_all_models().items():
        table.add_row(
            tier_name,
            info.name,
            f"{info.size_gb:.1f} GB",
            f"{info.min_ram_gb} GB",
            info.description,
        )
    console.print(table)

    console.print("\n[bold]Local models:[/bold]")
    local = ollama.list_local_models()
    if local:
        for m in local:
            console.print(f"  - {m}")
    else:
        console.print("  (none)")


@app.command(name="config")
def config_cmd(
    use_lmstudio: bool = typer.Option(False, "--lmstudio", help="Generate config for LM Studio"),
    model: str = typer.Option("phi4-mini", "--model", help="Model name (Ollama only)"),
    install: bool = typer.Option(False, "--install", help="Also install to ~/.continue/"),
    force: bool = typer.Option(
        False, "--force", help="Overwrite ~/.continue/config.json without prompting"
    ),
):
    """Regenerate Continue.dev config. With --install, copies to ~/.continue/ (backs up existing)."""
    provider = "lmstudio" if use_lmstudio else "ollama"
    config = generate_config(model, provider=provider)
    path = write_config(config)
    console.print(f"Config written to: {path}")

    if install:
        continue_home = Path.home() / ".continue" / "config.json"
        overwrite_home = force or not continue_home.exists()
        if not overwrite_home:
            overwrite_home = typer.confirm(
                "Overwrite ~/.continue/config.json? (existing file will be backed up)",
                default=False,
            )
        if overwrite_home:
            home_path = install_to_home(config, overwrite=True)
            if home_path:
                console.print(f"Installed to: {home_path}")


@app.command(name="vscode-init")
def vscode_init():
    """Copy VS Code settings (telemetry off, Continue.dev) into the current project."""
    src = Path(__file__).parent.parent / ".vscode"
    dest = Path.cwd() / ".vscode"
    dest.mkdir(exist_ok=True)
    for fname in ["settings.json", "extensions.json"]:
        src_file = src / fname
        dest_file = dest / fname
        if dest_file.exists():
            backup = dest / f"{fname}.backup"
            dest_file.rename(backup)
            console.print(f"  Backed up existing {fname} → {fname}.backup")
        dest_file.write_text(src_file.read_text())
        console.print(f"  Written: {dest_file}")
    console.print("\n[green]Done.[/green] Reopen the folder in VS Code to apply settings.")


@app.command(name="firewall")
def firewall_cmd():
    """Show firewall rule information for your OS."""
    console.print(Panel("Firewall Rules", style="bold blue"))
    console.print(firewall.get_firewall_info())


def _print_report(report: verify.VerifyReport):
    """Pretty-print a verification report."""
    for check in report.checks:
        icon = "[green]PASS[/green]" if check.passed else "[red]FAIL[/red]"
        console.print(f"  {icon}  {check.name}: {check.message}")


if __name__ == "__main__":
    app()
