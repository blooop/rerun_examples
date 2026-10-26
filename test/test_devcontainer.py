import re
import subprocess
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
DEVCONTAINER = REPO / ".devcontainer"


def host_bind_sources() -> list[str]:
    config = (DEVCONTAINER / "devcontainer.json").read_text(encoding="utf-8")
    live = "\n".join(line for line in config.splitlines() if not line.lstrip().startswith("//"))
    sources = []
    for mount in re.findall(r'"([^"]*\btype=bind\b[^"]*)"', live):
        fields = dict(field.split("=", 1) for field in mount.split(",") if "=" in field)
        home, _, rest = fields.get("source", "").partition("${localEnv:HOME}/")
        if not home and rest:
            sources.append(rest)
    return sources


def test_init_host_creates_every_home_bind_source(tmp_path):
    """docker refuses to create the container when a bind source is missing."""
    sources = host_bind_sources()
    assert sources, "found no ${localEnv:HOME} bind mounts in devcontainer.json"

    subprocess.run(
        [str(DEVCONTAINER / "claude-code" / "init-host.sh")],
        env={"HOME": str(tmp_path), "PATH": "/usr/bin:/bin"},
        check=True,
    )

    missing = [s for s in sources if not (tmp_path / s).is_dir()]
    assert not missing, f"init-host.sh did not create: {missing}"


def test_init_host_keeps_existing_dirs(tmp_path):
    """A second run must not fail or touch what is already there."""
    gh = tmp_path / ".config" / "gh"
    gh.mkdir(parents=True)
    (gh / "hosts.yml").write_text("token", encoding="utf-8")

    for _ in range(2):
        subprocess.run(
            [str(DEVCONTAINER / "claude-code" / "init-host.sh")],
            env={"HOME": str(tmp_path), "PATH": "/usr/bin:/bin"},
            check=True,
        )

    assert (gh / "hosts.yml").read_text(encoding="utf-8") == "token"
