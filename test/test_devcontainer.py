import json
import re
import subprocess
from pathlib import Path

DEVCONTAINER = Path(__file__).resolve().parents[1] / ".devcontainer"


def _home_bind_sources():
    text = (DEVCONTAINER / "devcontainer.json").read_text()
    config = json.loads(re.sub(r"^\s*//.*$", "", text, flags=re.MULTILINE))
    for mount in config["mounts"]:
        fields = dict(part.split("=", 1) for part in mount.split(","))
        if fields["type"] == "bind" and fields["source"].startswith("${localEnv:HOME}/"):
            yield fields["source"].removeprefix("${localEnv:HOME}/")


def test_init_host_creates_every_home_bind_source(tmp_path):
    # docker refuses a bind mount whose source is missing, so a host without
    # one of these directories cannot create the container at all.
    subprocess.run(
        [DEVCONTAINER / "claude-code" / "init-host.sh"],
        env={"HOME": str(tmp_path), "PATH": "/usr/bin:/bin"},
        check=True,
    )
    sources = list(_home_bind_sources())
    assert sources
    for source in sources:
        assert (tmp_path / source).is_dir(), source
