"""Typer CLI app: setup, verify, models, config commands."""

from pathlib import Path

import typer
from rich.console import Console
from rich.table import Table
from rich.panel import Panel

from cli import detect, models, ollama, lmstudio, verify, firewall
from cli.continue_config import generate_config, write_config, install_to_home

app = typer.Typer(
    name="on-device",
    help="On-device LLM for software development. Zero external network calls.",
)
console = Console()


@app.command()
def setup(
    use_lmstudio: bool = typer.Option(
        False, "--lmstudio", help="Use LM Studio instead of Ollama"
    ),
    tier: str = typer.Option(
        "", "--tier", help="Model tier: small, medium, large (auto-detected if empty)"
    ),
    skip_pull: bool = typer.Option(
        False, "--skip-pull", help="Skip model download"
    ),
    force: bool = typer.Option(
        False, "--force", help="Overwrite ~/.continue/config.json without prompting"
    ),
):
    """Full guided setup: runtime + model + Continue.dev config."""
    console.print(Panel("On-Device LLM Setup", style="bold blue"))

    # Step 1: Detect OS and RAM
    os_name = detect.get_os()
    ram_gb = detect.get_ram_gb()
    console.print(f"  OS: {os_name}")
    console.print(f"  RAM: {ram_gb:.1f} GB")

    # Step 2: Determine model tier
    valid_tiers = set(models.get_all_models())
    if not tier:
        tier = detect.recommend_tier(ram_gb)
    elif tier not in valid_tiers:
        console.print(
            f"[red]Invalid tier: {tier}. Choose from: {', '.join(sorted(valid_tiers))}[/red]"
        )
        raise typer.Exit(1)
    model_info = models.get_model(tier)
    console.print(f"  Recommended tier: {tier} ({model_info.name})")

    # Step 3: Check/install runtime
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

        model_name = model_info.name

        # Step 4: Pull model
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

    # Step 5: Generate Continue.dev config
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

    # Step 6: Verify
    console.print("\n[bold]Running verification...[/bold]")
    report = verify.run_all(model_name, use_lmstudio=use_lmstudio)
    _print_report(report)

    if report.all_passed:
        console.print("\n[bold green]Setup complete! Open this repo in VS Code to get started.[/bold green]")
    else:
        console.print("\n[bold yellow]Setup completed with warnings. See above.[/bold yellow]")


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
