#!/usr/bin/env python3
"""Contrôles déterministes et sans dépendance pour le toolkit."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path
from urllib.parse import unquote


ROOT = Path(__file__).resolve().parents[1]
REQUIRED = (
    "README.md",
    "AGENTS.md",
    "standards/README.md",
    "skills/README.md",
    "agents/README.md",
    "templates/README.md",
    "docs/codex-compatibility.md",
    "docs/installation.md",
    "docs/versioning.md",
    "docs/project-audit.md",
    "docs/project-audit-evaluation.md",
    "toolkit-manifest.json",
    "skills/project-audit/SKILL.md",
    ".github/workflows/toolkit-ci.yml",
)
IGNORED_PARTS = {".git", ".idea", ".venv", "node_modules", "build", "dist"}
MARKDOWN_LINK = re.compile(r"\[[^\]]*\]\(([^)]+)\)")
SECRET_PATTERNS = {
    "private key": re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----"),
    "AWS access key": re.compile(r"\bAKIA[0-9A-Z]{16}\b"),
    "GitHub token": re.compile(r"\bgh[pousr]_[A-Za-z0-9]{30,}\b"),
    "OpenAI key": re.compile(r"\bsk-[A-Za-z0-9_-]{20,}\b"),
    "GitLab token": re.compile(r"\bglpat-[A-Za-z0-9_-]{20,}\b"),
    "Slack token": re.compile(r"\bxox[baprs]-[A-Za-z0-9-]{20,}\b"),
}
FRONTMATTER = re.compile(r"\A---\n(?P<body>.*?)\n---\n", re.DOTALL)
SKILL_NAME = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
SEMVER = re.compile(r"^\d+\.\d+\.\d+(?:-[0-9A-Za-z.-]+)?$")


def files() -> list[Path]:
    return sorted(
        path
        for path in ROOT.rglob("*")
        if path.is_file() and not any(part in IGNORED_PARTS for part in path.parts)
    )


def check_required(errors: list[str]) -> None:
    for relative in REQUIRED:
        if not (ROOT / relative).is_file():
            errors.append(f"fichier requis absent: {relative}")


def check_manifest(errors: list[str]) -> None:
    path = ROOT / "toolkit-manifest.json"
    try:
        manifest = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeDecodeError, json.JSONDecodeError) as error:
        errors.append(f"manifeste illisible: {error}")
        return
    if not isinstance(manifest, dict):
        errors.append("le manifeste doit être un objet JSON")
        return
    if manifest.get("schema_version") != 1:
        errors.append("version de schéma du manifeste non supportée")
    if not SEMVER.fullmatch(str(manifest.get("toolkit_version", ""))):
        errors.append("version du toolkit invalide dans le manifeste")
    resources = manifest.get("resources")
    if not isinstance(resources, dict) or not resources:
        errors.append("aucune ressource dans le manifeste")
        return
    for name, resource in resources.items():
        if not SKILL_NAME.fullmatch(name) or not isinstance(resource, dict):
            errors.append(f"ressource invalide dans le manifeste: {name}")
            continue
        if resource.get("kind") != "skill":
            errors.append(f"type de ressource non supporté: {name}")
        if not SEMVER.fullmatch(str(resource.get("version", ""))):
            errors.append(f"version de ressource invalide: {name}")
        technologies = resource.get("technologies")
        valid_technologies = (
            isinstance(technologies, list)
            and bool(technologies)
            and all(isinstance(item, str) and item for item in technologies)
        )
        if not valid_technologies or len(technologies) != len(set(technologies)):
            errors.append(f"technologies invalides: {name}")
        source_value = resource.get("source")
        if not valid_relative_path(source_value):
            errors.append(f"chemin source invalide: {name}")
            continue
        source = (ROOT / source_value).resolve()
        try:
            source.relative_to(ROOT)
        except ValueError:
            errors.append(f"source de ressource hors dépôt: {name}")
            continue
        if not source.exists():
            errors.append(f"source de ressource absente: {name}")
        if resource.get("kind") == "skill" and not (source / "SKILL.md").is_file():
            errors.append(f"SKILL.md absent pour la ressource: {name}")
        if resource.get("kind") == "skill" and source.name != name:
            errors.append(f"nom de source incohérent pour la ressource: {name}")
        destinations = resource.get("destinations")
        if not isinstance(destinations, dict):
            errors.append(f"destinations invalides: {name}")
        else:
            for scope in ("project", "user"):
                if not valid_relative_path(destinations.get(scope)):
                    errors.append(f"destination {scope} invalide: {name}")


def valid_relative_path(value: object) -> bool:
    if not isinstance(value, str) or not value:
        return False
    path = Path(value)
    return path != Path(".") and not path.is_absolute() and ".." not in path.parts


def check_skill(path: Path, errors: list[str]) -> None:
    try:
        content = path.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError):
        return
    match = FRONTMATTER.match(content)
    if not match:
        errors.append(f"frontmatter absent ou invalide: {path.relative_to(ROOT)}")
        return
    fields = {}
    for line in match.group("body").splitlines():
        if ":" in line:
            key, value = line.split(":", 1)
            fields[key.strip()] = value.strip().strip('"')
    name = fields.get("name", "")
    if not SKILL_NAME.fullmatch(name) or path.parent.name != name:
        errors.append(f"nom de skill invalide ou incohérent: {path.relative_to(ROOT)}")
    if not fields.get("description"):
        errors.append(f"description de skill absente: {path.relative_to(ROOT)}")
    metadata = path.parent / "agents/openai.yaml"
    if metadata.is_file():
        check_openai_metadata(metadata, name, errors)


def check_workflow(errors: list[str]) -> None:
    path = ROOT / ".github/workflows/toolkit-ci.yml"
    try:
        content = path.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError) as error:
        errors.append(f"workflow CI illisible: {error}")
        return
    required_fragments = (
        "pull_request:",
        "permissions:\n  contents: read",
        "timeout-minutes:",
        "actions/checkout@v4",
        "actions/setup-python@v5",
        "python3 scripts/check_toolkit.py",
        "python3 -m unittest discover -s tests -v",
    )
    for fragment in required_fragments:
        if fragment not in content:
            errors.append(f"workflow CI incomplet: {fragment}")
    if "pull_request_target" in content:
        errors.append("workflow CI interdit: pull_request_target")
    if "secrets." in content:
        errors.append("workflow CI ne doit pas lire de secret")


def check_openai_metadata(path: Path, skill_name: str, errors: list[str]) -> None:
    try:
        content = path.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError):
        errors.append(f"métadonnées illisibles: {path.relative_to(ROOT)}")
        return
    values = {}
    for key in ("display_name", "short_description", "default_prompt"):
        match = re.search(rf'^\s{{2}}{key}:\s*"([^"]+)"\s*$', content, flags=re.MULTILINE)
        if not match:
            errors.append(f"champ {key} absent ou non cité: {path.relative_to(ROOT)}")
            continue
        values[key] = match.group(1)
    short = values.get("short_description", "")
    if short and not 25 <= len(short) <= 64:
        errors.append(f"short_description hors limites: {path.relative_to(ROOT)}")
    prompt = values.get("default_prompt", "")
    if prompt and f"${skill_name}" not in prompt:
        errors.append(f"default_prompt sans ${skill_name}: {path.relative_to(ROOT)}")


def check_content(path: Path, errors: list[str]) -> None:
    relative = path.relative_to(ROOT)
    if path.stat().st_size == 0:
        errors.append(f"fichier vide: {relative}")
        return

    try:
        content = path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        return

    if re.search(r"^(?:<{7}|={7}|>{7})", content, flags=re.MULTILINE):
        errors.append(f"marqueur de conflit Git: {relative}")

    for label, pattern in SECRET_PATTERNS.items():
        if pattern.search(content):
            errors.append(f"secret potentiel ({label}): {relative}")

    if path.suffix.lower() == ".md":
        check_links(path, content, errors)


def check_links(path: Path, content: str, errors: list[str]) -> None:
    for raw_target in MARKDOWN_LINK.findall(content):
        target = raw_target.strip().strip("<>").split(maxsplit=1)[0]
        if not target or target.startswith(("#", "http://", "https://", "mailto:")):
            continue
        local = unquote(target.split("#", 1)[0].split("?", 1)[0])
        if not local:
            continue
        resolved = (path.parent / local).resolve()
        try:
            resolved.relative_to(ROOT)
        except ValueError:
            errors.append(f"lien hors dépôt dans {path.relative_to(ROOT)}: {target}")
            continue
        if not resolved.exists():
            errors.append(f"lien local cassé dans {path.relative_to(ROOT)}: {target}")


def main() -> int:
    errors: list[str] = []
    check_required(errors)
    check_manifest(errors)
    check_workflow(errors)
    for path in files():
        check_content(path, errors)
        if path.name == "SKILL.md":
            check_skill(path, errors)

    if errors:
        print("ÉCHEC — incohérences détectées :")
        for error in errors:
            print(f"- {error}")
        return 1

    print(f"OK — {len(files())} fichiers contrôlés, aucune incohérence détectée.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
