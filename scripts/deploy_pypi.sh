#!/usr/bin/env bash
set -euo pipefail

python3 -m venv .venv
source .venv/bin/activate

python3 -m pip install --upgrade pip
python3 -m pip install --upgrade build twine

usage() {
  cat <<'USAGE'
Usage:
  scripts/deploy_pypi.sh [--skip-build]

Options:
  --skip-build  Reuse existing files in dist/ instead of rebuilding.
  -h, --help    Show this help text.

Authentication:
  Export TWINE_USERNAME=__token__ and TWINE_PASSWORD=<pypi-api-token>,
  or use a configured ~/.pypirc for production PyPI.
USAGE
}

skip_build=0

while [ "$#" -gt 0 ]; do
  case "$1" in
    --skip-build)
      skip_build=1
      ;;
    -h|--help)
      usage
      exit 0
      ;;
    *)
      echo "Unknown option: $1" >&2
      usage >&2
      exit 2
      ;;
  esac
  shift
done

require_module() {
  local module="$1"
  local package="$2"

  if ! python3 -c "import ${module}" >/dev/null 2>&1; then
    echo "Missing Python package: ${package}" >&2
    echo "Install It With: python3 -m pip install ${package}" >&2
    exit 1
  fi
}

project_version() {
  python3 - <<'PY'
import pathlib
import tomllib

with pathlib.Path("pyproject.toml").open("rb") as fh:
    data = tomllib.load(fh)

print(data["project"]["version"])
PY
}

require_module build build
require_module twine twine

if [ ! -f pyproject.toml ]; then
  echo "Run this script from the project root." >&2
  exit 1
fi

version="$(project_version)"
echo "Preparing django-simorgh ${version}"

if [ "$skip_build" -eq 0 ]; then
  echo "Removing old build artifacts"
  rm -rf build dist *.egg-info

  echo "Building source distribution and wheel"
  python3 -m build
else
  echo "Skipping build and reusing dist/"
fi

if ! compgen -G "dist/*" >/dev/null; then
  echo "No distribution files found in dist/." >&2
  exit 1
fi

echo "Checking distributions"
python3 -m twine check dist/*

echo "Uploading to PyPI"
python3 -m twine upload --repository pypi dist/*

deactivate
rm -rf .venv