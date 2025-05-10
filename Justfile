# Recipes for the `just` task-runner:
# https://github.com/casey/just

_default: help

e := ""
repo-url := "https://github.com/infused-kim/kb_trackpoint_extension"

#
# Local development
#

alias activate := venv-activate
alias deactivate := venv-deactivate

# Run the app in dev mode
[group("local dev")]
run *args:
    uv run tp_extension_builder {{ args }}

# Install python app and pre-commit hooks
[group("local dev")]
setup: uv-sync pre-commit-install venv-activate

# Run all checks
[group("local dev")]
check: pre-commit-run

# Lint the code
[group("local dev")]
lint:
    uv run ruff check .
    uv run mypy .

# Format the code
[group("local dev")]
format:
    uv run ruff format .

#
# Virtual environment
#

venv-activate-cmd := if os_family() == "windows" { "source .venv/Scripts/activate" } else if env('SHELL') =~ 'fish$' { "source .venv/bin/activate.fish" } else { "source .venv/bin/activate" }

# Show how to activate the python environment
[group("virtual environment")]
venv-activate:
    @echo
    @echo "To activate the python environment, run:"
    @echo "\t{{ venv-activate-cmd }}"

# Show how to deactivate the python environment
[group("virtual environment")]
venv-deactivate:
    @echo
    @echo "To deactivate the python environment, run:"
    @echo "\tdeactivate"

#
# uv - python package manager
#

alias uv-install := uv-sync
alias uvs := uv-sync
alias uvi := uv-sync
alias uva := uv-add
alias uva-dev := uv-add-dev
alias uvr := uv-remove

# Install python app with all dependencies
[group("uv")]
uv-sync *extra-args:
    uv sync {{ extra-args }}

# Add a python dependency
[group("uv")]
uv-add pkg_name *extra-args:
    uv add {{ pkg_name }} {{ extra-args }}

# Add a python dev dependency
[group("uv")]
uv-add-dev pkg_name *extra-args:
    uv add --dev {{ pkg_name }} {{ extra-args }}

# Remove a python dependency
[group("uv")]
uv-remove pkg_name *extra-args:
    uv remove {{ pkg_name }} {{ extra-args }}

# Upgrade python dependencies
[group("uv")]
uv-upgrade *extra-args:
    uv sync --upgrade {{ extra-args }}

# Run uv command
[group("uv")]
uv *args:
    uv {{ args }}

#
# Pre-commit
#

alias pc := pre-commit
alias pcr := pre-commit-run

# Run pre-commit push hooks
[group("pre-commit")]
pre-commit-run:
    uv run pre-commit run --hook-stage push --all-files

# Set up pre-commit hooks
[group("pre-commit")]
pre-commit-install:
    uv run pre-commit install

# Update all pre-commit hooks
[group("pre-commit")]
pre-commit-update:
    uv run pre-commit autoupdate --freeze

# Run pre-commit command command
[group("pre-commit")]
pre-commit *args:
    uv run pre-commit {{ args }}

#
# Other
#

# Show this help
[group("other")]
help:
    @echo "Info:"
    @echo "    - Git repo: {{ repo-url }}"
    @echo
    @just --list --unsorted

# Print and open the git repo url
[group("other")]
repo:
    @echo "git repo: {{ repo-url }}"
    @open "{{ repo-url }}"
