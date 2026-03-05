"""OS detection and RAM check using stdlib only."""

import platform
import os


def get_os() -> str:
    """Return normalized OS name: 'macos', 'linux', or 'windows'."""
    system = platform.system().lower()
    if system == "darwin":
        return "macos"
    if system == "linux":
        return "linux"
    if system == "windows":
        return "windows"
    return system


def get_ram_gb() -> float:
    """Return total system RAM in GB."""
    system = get_os()
    if system == "macos":
        try:
            import subprocess

            result = subprocess.run(
                ["sysctl", "-n", "hw.memsize"],
                capture_output=True,
                text=True,
                check=True,
            )
            return int(result.stdout.strip()) / (1024**3)
        except Exception:
            pass
    elif system == "linux":
        try:
            with open("/proc/meminfo") as f:
                for line in f:
                    if line.startswith("MemTotal:"):
                        kb = int(line.split()[1])
                        return kb / (1024**2)
        except Exception:
            pass
    elif system == "windows":
        try:
            import subprocess

            result = subprocess.run(
                [
                    "wmic",
                    "computersystem",
                    "get",
                    "TotalPhysicalMemory",
                    "/value",
                ],
                capture_output=True,
                text=True,
                check=True,
            )
            for line in result.stdout.strip().splitlines():
                if "=" in line:
                    return int(line.split("=")[1]) / (1024**3)
        except Exception:
            pass

    # Fallback: try os.sysconf (Linux/macOS)
    try:
        pages = os.sysconf("SC_PHYS_PAGES")
        page_size = os.sysconf("SC_PAGE_SIZE")
        return (pages * page_size) / (1024**3)
    except (ValueError, OSError, AttributeError):
        return 0.0


def recommend_tier(ram_gb: float) -> str:
    """Recommend a model tier based on available RAM."""
    if ram_gb >= 16:
        return "large"
    if ram_gb >= 8:
        return "medium"
    return "small"
