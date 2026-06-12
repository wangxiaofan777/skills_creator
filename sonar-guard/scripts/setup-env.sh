#!/usr/bin/env bash
# One-time: point SONARGUARD_HOME at your skills_creator clone (any path).
set -euo pipefail

INSTALL_REL="sonar-guard/scripts/install.py"
PACKAGE_ROOT="${1:-}"

valid_root() {
  [[ -f "$1/$INSTALL_REL" ]]
}

if [[ -z "$PACKAGE_ROOT" ]]; then
  read -r -p "skills_creator clone path: " PACKAGE_ROOT
fi
PACKAGE_ROOT="$(cd "$PACKAGE_ROOT" && pwd)"

if ! valid_root "$PACKAGE_ROOT"; then
  echo "Invalid path: missing $INSTALL_REL under $PACKAGE_ROOT" >&2
  exit 1
fi

CONFIG_DIR="${HOME}/.config/sonarguard"
CONFIG_FILE="${CONFIG_DIR}/config.json"
mkdir -p "$CONFIG_DIR"

python3 - "$CONFIG_FILE" "$PACKAGE_ROOT" <<'PY'
import json, sys
from pathlib import Path
cfg_path, root = Path(sys.argv[1]), sys.argv[2]
data = {}
if cfg_path.is_file():
    try:
        data = json.loads(cfg_path.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        pass
data["packageRoot"] = root
cfg_path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
PY

echo "OK: packageRoot -> $PACKAGE_ROOT"
echo "Add to ~/.bashrc or ~/.zshrc:"
echo "  export SONARGUARD_HOME=\"$PACKAGE_ROOT\""
echo "Then from business repo:"
echo "  python \"\$SONARGUARD_HOME/sonar-guard/scripts/install_bootstrap.py\" --platform all --repo ."
