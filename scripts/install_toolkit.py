#!/usr/bin/env python3
"""Preview, install, or safely update toolkit resources."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import shutil
import sys
import tempfile
from dataclasses import dataclass
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_MANIFEST = ROOT / "toolkit-manifest.json"
STATE_RELATIVE = Path(".codex/agents-ia-toolkit-state.json")
BACKUP_RELATIVE = Path(".codex/toolkit-backups")
SEMVER = re.compile(r"^\d+\.\d+\.\d+(?:-[0-9A-Za-z.-]+)?$")


@dataclass
class PlanItem:
    name: str
    resource: dict
    source: Path
    target: Path
    target_relative: str
    state: str
    detail: str
    source_digest: str | None = None
    target_digest: str | None = None
    backup: Path | None = None


def reject_symlinks(path: Path, label: str) -> None:
    if path.is_symlink():
        raise ValueError(f"{label} must not be a symbolic link: {path}")
    if path.is_dir():
        for item in path.rglob("*"):
            if item.is_symlink():
                raise ValueError(f"{label} contains a symbolic link: {item}")


def digest(path: Path) -> str:
    reject_symlinks(path, "resource")
    hasher = hashlib.sha256()
    if path.is_file():
        hasher.update(path.name.encode())
        hasher.update(path.read_bytes())
        return hasher.hexdigest()
    if not path.is_dir():
        raise OSError(f"unsupported resource type: {path}")
    for item in sorted(candidate for candidate in path.rglob("*") if candidate.is_file()):
        hasher.update(item.relative_to(path).as_posix().encode())
        hasher.update(item.read_bytes())
    return hasher.hexdigest()


def load_manifest(path: Path) -> dict:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeDecodeError, json.JSONDecodeError) as error:
        raise ValueError(f"cannot read manifest {path}: {error}") from error
    if not isinstance(data, dict) or data.get("schema_version") != 1 or not isinstance(data.get("resources"), dict):
        raise ValueError("unsupported or invalid manifest")
    if not SEMVER.fullmatch(str(data.get("toolkit_version", ""))):
        raise ValueError("invalid toolkit version")
    if not data["resources"]:
        raise ValueError("manifest contains no resources")
    for name, resource in data["resources"].items():
        if not isinstance(name, str) or not isinstance(resource, dict):
            raise ValueError("invalid resource entry")
        if resource.get("kind") not in {"skill", "agent"} or not SEMVER.fullmatch(str(resource.get("version", ""))):
            raise ValueError(f"invalid resource metadata: {name}")
        technologies = resource.get("technologies")
        if (
            not isinstance(technologies, list)
            or not technologies
            or not all(isinstance(item, str) and item for item in technologies)
            or len(technologies) != len(set(technologies))
        ):
            raise ValueError(f"invalid technologies: {name}")
    return data


def valid_relative(value: object, label: str) -> Path:
    if not isinstance(value, str) or not value:
        raise ValueError(f"invalid {label}")
    path = Path(value)
    if path == Path(".") or path.is_absolute() or ".." in path.parts:
        raise ValueError(f"invalid {label}")
    return path


def contained_path(base: Path, relative: Path, label: str) -> Path:
    candidate = base / relative
    resolved = candidate.resolve(strict=False)
    try:
        resolved.relative_to(base)
    except ValueError as error:
        raise ValueError(f"{label} resolves outside the installation base") from error
    return candidate


def destination(base: Path, resource: dict, scope: str) -> Path:
    destinations = resource.get("destinations", {})
    if not isinstance(destinations, dict):
        raise ValueError("invalid destinations")
    relative = valid_relative(destinations.get(scope), f"{scope} destination")
    return contained_path(base, relative, f"{scope} destination")


def source_path(resource: dict) -> Path:
    relative = valid_relative(resource.get("source"), "source path")
    source = (ROOT / relative).resolve()
    try:
        source.relative_to(ROOT)
    except ValueError as error:
        raise ValueError("source resolves outside the toolkit") from error
    reject_symlinks(source, "source")
    return source


def state_path(base: Path) -> Path:
    return contained_path(base, STATE_RELATIVE, "state path")


def load_state(path: Path) -> dict:
    if not path.exists():
        return {"schema_version": 1, "resources": {}}
    if path.is_symlink() or not path.is_file():
        raise ValueError("installation state must be a regular file")
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeDecodeError, json.JSONDecodeError) as error:
        raise ValueError(f"cannot read installation state {path}: {error}") from error
    if not isinstance(data, dict) or data.get("schema_version") != 1 or not isinstance(data.get("resources"), dict):
        raise ValueError("unsupported or invalid installation state")
    for name, entry in data["resources"].items():
        if not isinstance(name, str) or not isinstance(entry, dict):
            raise ValueError("invalid installation state resource")
        for field in ("kind", "version", "target", "digest"):
            if not isinstance(entry.get(field), str) or not entry[field]:
                raise ValueError(f"invalid installation state metadata: {name}")
        if entry["kind"] not in {"skill", "agent"} or not SEMVER.fullmatch(entry["version"]):
            raise ValueError(f"invalid installation state metadata: {name}")
        if not re.fullmatch(r"[0-9a-f]{64}", entry["digest"]):
            raise ValueError(f"invalid installation state digest: {name}")
        valid_relative(entry["target"], f"state target for {name}")
    return data


def backup_path(base: Path, name: str, entry: dict, target: Path) -> Path:
    version = entry.get("version", "unknown")
    old_digest = entry.get("digest", "unknown")[:12]
    relative = BACKUP_RELATIVE / name / f"{version}-{old_digest}" / target.name
    return contained_path(base, relative, "backup path")


def inspect_resource(base: Path, name: str, resource: dict, scope: str, installed: dict) -> PlanItem:
    source = source_path(resource)
    target = destination(base, resource, scope)
    relative = target.relative_to(base).as_posix()
    if not source.exists():
        return PlanItem(name, resource, source, target, relative, "ERROR", "source is missing")
    try:
        source_digest = digest(source)
    except (OSError, ValueError) as error:
        return PlanItem(name, resource, source, target, relative, "ERROR", str(error))
    entry = installed.get(name)
    if not target.exists() and not target.is_symlink():
        return PlanItem(name, resource, source, target, relative, "CREATE", "target does not exist", source_digest)
    if target.is_symlink():
        return PlanItem(name, resource, source, target, relative, "CONFLICT", "target is a symbolic link", source_digest)
    if source.is_dir() != target.is_dir():
        return PlanItem(name, resource, source, target, relative, "CONFLICT", "source and target types differ", source_digest)
    try:
        target_digest = digest(target)
    except (OSError, ValueError) as error:
        return PlanItem(name, resource, source, target, relative, "ERROR", str(error), source_digest)
    if source_digest == target_digest:
        detail = "target matches source"
        if entry is None:
            detail += "; apply mode will adopt it into installation state"
        return PlanItem(name, resource, source, target, relative, "UNCHANGED", detail, source_digest, target_digest)
    if entry is None:
        return PlanItem(name, resource, source, target, relative, "CONFLICT", "unmanaged target has different content", source_digest, target_digest)
    if entry.get("target") != relative:
        return PlanItem(name, resource, source, target, relative, "CONFLICT", "recorded destination differs", source_digest, target_digest)
    if entry.get("digest") != target_digest:
        return PlanItem(name, resource, source, target, relative, "CONFLICT", "target was modified after installation", source_digest, target_digest)
    backup = backup_path(base, name, entry, target)
    if backup.exists() or backup.is_symlink():
        return PlanItem(name, resource, source, target, relative, "ERROR", f"backup already exists: {backup}", source_digest, target_digest)
    return PlanItem(name, resource, source, target, relative, "UPDATE", "managed target is unchanged and can be updated safely", source_digest, target_digest, backup)


def copy_to_stage(source: Path, target: Path, name: str) -> tuple[Path, Path]:
    target.parent.mkdir(parents=True, exist_ok=True)
    stage_root = Path(tempfile.mkdtemp(prefix=f".{name}-stage-", dir=target.parent))
    staged = stage_root / target.name
    if source.is_dir():
        shutil.copytree(source, staged, copy_function=shutil.copy2)
    else:
        shutil.copy2(source, staged)
    return stage_root, staged


def remove_path(path: Path) -> None:
    if path.is_dir() and not path.is_symlink():
        shutil.rmtree(path)
    elif path.exists() or path.is_symlink():
        path.unlink()


def apply_item(item: PlanItem) -> tuple[str, Path, Path | None] | None:
    if item.state == "UNCHANGED":
        return None
    stage_root, staged = copy_to_stage(item.source, item.target, item.name)
    try:
        if item.state == "CREATE":
            staged.rename(item.target)
            return "CREATE", item.target, None
        if item.state == "UPDATE" and item.backup is not None:
            item.backup.parent.mkdir(parents=True, exist_ok=False)
            item.target.rename(item.backup)
            try:
                staged.rename(item.target)
            except Exception:
                item.backup.rename(item.target)
                raise
            return "UPDATE", item.target, item.backup
        raise ValueError(f"cannot apply state {item.state}")
    finally:
        shutil.rmtree(stage_root, ignore_errors=True)


def rollback(applied: list[tuple[str, Path, Path | None]]) -> None:
    for action, target, backup in reversed(applied):
        if action == "CREATE":
            remove_path(target)
        elif action == "UPDATE" and backup is not None:
            remove_path(target)
            backup.rename(target)


def write_state(path: Path, state: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    handle = tempfile.NamedTemporaryFile("w", encoding="utf-8", dir=path.parent, prefix=".toolkit-state-", delete=False)
    temporary = Path(handle.name)
    try:
        with handle:
            json.dump(state, handle, indent=2, sort_keys=True)
            handle.write("\n")
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temporary, path)
    except Exception:
        temporary.unlink(missing_ok=True)
        raise


def state_entry(item: PlanItem) -> dict:
    if item.source_digest is None:
        raise ValueError(f"missing digest for {item.name}")
    return {
        "kind": item.resource["kind"],
        "version": item.resource["version"],
        "target": item.target_relative,
        "digest": item.source_digest,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--check", action="store_true", help="preview and fail on conflicts")
    mode.add_argument("--dry-run", action="store_true", help="preview without writing")
    mode.add_argument("--install", action="store_true", help="install missing resources and record identical targets")
    mode.add_argument("--update", action="store_true", help="install missing resources and update unmodified managed targets")
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
    applying = args.install or args.update
    if applying and (not base.exists() or not base.is_dir() or base.is_symlink()):
        print("ERROR: apply target must be an existing regular directory", file=sys.stderr)
        return 2

    try:
        current_state_path = state_path(base)
        installed_state = load_state(current_state_path)
    except ValueError as error:
        print(f"ERROR: {error}", file=sys.stderr)
        return 2

    available = manifest["resources"]
    selected = args.resources or list(available)
    if len(selected) != len(set(selected)):
        print("ERROR: duplicate resource selection", file=sys.stderr)
        return 2
    unknown = sorted(set(selected).difference(available))
    if unknown:
        print(f"ERROR: unknown resources: {', '.join(unknown)}", file=sys.stderr)
        return 2

    technology_filter = set(args.technologies or [])
    known_technologies = {technology for resource in available.values() for technology in resource.get("technologies", [])}
    unknown_technologies = sorted(technology_filter.difference(known_technologies))
    if unknown_technologies:
        print(f"ERROR: unknown technologies: {', '.join(unknown_technologies)}", file=sys.stderr)
        return 2

    items: list[PlanItem] = []
    print(f"Toolkit {manifest.get('toolkit_version', 'unversioned')} installation plan")
    print(f"Scope: {args.scope}; base: {base}")
    for name in selected:
        resource = available[name]
        supported = set(resource.get("technologies", []))
        if technology_filter and not technology_filter.intersection(supported):
            print(f"SKIP {name}: technology filter does not match")
            continue
        try:
            item = inspect_resource(base, name, resource, args.scope, installed_state["resources"])
        except ValueError as error:
            item = PlanItem(name, resource, ROOT, base, ".", "ERROR", str(error))
        items.append(item)
        print(f"{item.state} {name} {resource.get('version', 'unversioned')}: {item.source} -> {item.target} ({item.detail})")

    errors = any(item.state == "ERROR" for item in items)
    conflicts = any(item.state == "CONFLICT" for item in items)
    updates = any(item.state == "UPDATE" for item in items)
    if not applying:
        print("No files were modified.")
        if errors:
            return 2
        return 1 if args.check and conflicts else 0
    if errors:
        print("No files were modified because the plan contains errors.", file=sys.stderr)
        return 2
    if conflicts:
        print("No files were modified because the plan contains conflicts.", file=sys.stderr)
        return 1
    if args.install and updates:
        print("No files were modified because managed updates require --update.", file=sys.stderr)
        return 1
    if not items:
        print("No resources matched; no files were modified.")
        return 0

    next_state = json.loads(json.dumps(installed_state))
    next_state["toolkit_version"] = manifest["toolkit_version"]
    applied: list[tuple[str, Path, Path | None]] = []
    try:
        for item in items:
            result = apply_item(item)
            if result is not None:
                applied.append(result)
            next_state["resources"][item.name] = state_entry(item)
        if next_state != installed_state:
            write_state(current_state_path, next_state)
    except Exception as error:
        rollback(applied)
        print(f"ERROR: installation rolled back: {error}", file=sys.stderr)
        return 2

    changed = sum(item.state in {"CREATE", "UPDATE"} for item in items)
    print(f"Applied successfully: {changed} resource(s) changed; state: {current_state_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
