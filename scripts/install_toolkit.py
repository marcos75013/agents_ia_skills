#!/usr/bin/env python3
"""Preview toolkit resource installation without modifying the target."""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_MANIFEST = ROOT / "toolkit-manifest.json"


def digest(path: Path) -> str:
    hasher = hashlib.sha256()
    if path.is_file():
        hasher.update(path.name.encode())
        hasher.update(path.read_bytes())
        return hasher.hexdigest()
    for item in sorted(candidate for candidate in path.rglob("*") if candidate.is_file()):
        hasher.update(item.relative_to(path).as_posix().encode())
        hasher.update(item.read_bytes())
    return hasher.hexdigest()


def load_manifest(path: Path) -> dict:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeDecodeError, json.JSONDecodeError) as error:
        raise ValueError(f"cannot read manifest {path}: {error}") from error
    if data.get("schema_version") != 1 or not isinstance(data.get("resources"), dict):
        raise ValueError("unsupported or invalid manifest")
    return data


def destination(base: Path, resource: dict, scope: str) -> Path:
    destinations = resource.get("destinations", {})
    relative = destinations.get(scope)
    if not isinstance(relative, str) or Path(relative).is_absolute() or ".." in Path(relative).parts:
        raise ValueError(f"invalid {scope} destination")
    return base / relative


def source_path(resource: dict) -> Path:
    relative = resource.get("source")
    if not isinstance(relative, str) or Path(relative).is_absolute() or ".." in Path(relative).parts:
        raise ValueError("invalid source path")
    source = (ROOT / relative).resolve()
    try:
        source.relative_to(ROOT)
    except ValueError as error:
        raise ValueError("source resolves outside the toolkit") from error
    return source


def status(source: Path, target: Path) -> tuple[str, str]:
    if not source.exists():
        return "ERROR", "source is missing"
    if not target.exists():
        return "CREATE", "target does not exist"
    if source.is_dir() != target.is_dir():
        return "CONFLICT", "source and target types differ"
    if digest(source) == digest(target):
        return "UNCHANGED", "target matches source"
    return "CONFLICT", "target exists with different content"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--check", action="store_true", help="preview and fail on conflicts")
    mode.add_argument("--dry-run", action="store_true", help="preview without writing")
    parser.add_argument("--scope", choices=("project", "user"), required=True)
    parser.add_argument("--target", type=Path, help="repository root or user home; defaults to CWD or HOME")
    parser.add_argument("--resource", action="append", dest="resources", help="resource name; repeat as needed")
    parser.add_argument("--technology", action="append", dest="technologies", help="filter by technology")
    parser.add_argument("--manifest", type=Path, default=DEFAULT_MANIFEST)
    args = parser.parse_args()

    try:
        manifest = load_manifest(args.manifest.resolve())
    except ValueError as error:
        print(f"ERROR: {error}", file=sys.stderr)
        return 2

    if args.target:
        base = args.target.expanduser().resolve()
    elif args.scope == "project":
        base = Path.cwd().resolve()
    else:
        base = Path.home().resolve()

    available = manifest["resources"]
    selected = args.resources or list(available)
    unknown = sorted(set(selected).difference(available))
    if unknown:
        print(f"ERROR: unknown resources: {', '.join(unknown)}", file=sys.stderr)
        return 2

    technology_filter = set(args.technologies or [])
    conflicts = False
    print(f"Toolkit {manifest.get('toolkit_version', 'unversioned')} installation preview")
    print(f"Scope: {args.scope}; base: {base}")
    for name in selected:
        resource = available[name]
        supported = set(resource.get("technologies", []))
        if technology_filter and not technology_filter.intersection(supported):
            print(f"SKIP {name}: technology filter does not match")
            continue
        try:
            source = source_path(resource)
            target = destination(base, resource, args.scope)
        except ValueError as error:
            print(f"ERROR {name}: {error}")
            conflicts = True
            continue
        state, detail = status(source, target)
        print(f"{state} {name} {resource.get('version', 'unversioned')}: {source} -> {target} ({detail})")
        conflicts = conflicts or state in {"CONFLICT", "ERROR"}

    print("No files were modified. This preview-only version never writes to the target.")
    return 1 if args.check and conflicts else 0


if __name__ == "__main__":
    raise SystemExit(main())
