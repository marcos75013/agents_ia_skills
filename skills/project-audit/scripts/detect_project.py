#!/usr/bin/env python3
"""Inventory project manifests without executing project code or reading secrets."""

from __future__ import annotations

import argparse
import json
import os
from pathlib import Path


IGNORED = {".git", ".dart_tool", ".gradle", ".idea", ".next", ".venv", "build", "coverage", "dist", "node_modules", "target", "vendor"}
MANIFESTS = {
    "pubspec.yaml",
    "angular.json",
    "package.json",
    "pom.xml",
    "build.gradle",
    "build.gradle.kts",
    "settings.gradle",
    "settings.gradle.kts",
}
SPRING_BOOT_MARKERS = ("org.springframework.boot", "spring-boot-")


def candidates(root: Path):
    for current, directories, filenames in os.walk(root, followlinks=False):
        directories[:] = sorted(name for name in directories if name not in IGNORED)
        for name in sorted(MANIFESTS.intersection(filenames)):
            yield Path(current) / name


def package_json_signals(path: Path) -> set[str]:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeDecodeError, json.JSONDecodeError):
        return set()
    if not isinstance(data, dict):
        return set()
    dependencies = {}
    for key in ("dependencies", "devDependencies", "peerDependencies"):
        value = data.get(key, {})
        if isinstance(value, dict):
            dependencies.update(value)
    signals = set()
    is_angular = "@angular/core" in dependencies
    if is_angular:
        signals.add("angular")
    backend_packages = {"express", "fastify", "@nestjs/core", "koa", "hapi", "@hapi/hapi"}
    if not is_angular or backend_packages.intersection(dependencies):
        signals.add("nodejs")
    return signals


def belongs_to_flutter_project(path: Path) -> bool:
    return any((parent / "pubspec.yaml").is_file() for parent in path.parents)


def detect(path: Path) -> set[str]:
    if path.name == "pubspec.yaml":
        try:
            text = path.read_text(encoding="utf-8", errors="replace")
        except OSError:
            return {"dart"}
        return {"flutter"} if "flutter:" in text else {"dart"}
    if path.name == "angular.json":
        return {"angular"}
    if path.name == "package.json":
        return package_json_signals(path)
    if path.name in {"pom.xml", "build.gradle", "build.gradle.kts"}:
        try:
            text = path.read_text(encoding="utf-8", errors="replace")
        except OSError:
            return {"java"}
        lowered = text.lower()
        if any(marker in lowered for marker in SPRING_BOOT_MARKERS):
            return {"spring-boot"}
        return set() if belongs_to_flutter_project(path) else {"java"}
    return set()


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("path", nargs="?", default=".", help="project or repository root")
    args = parser.parse_args()
    root = Path(args.path).resolve()
    if not root.is_dir():
        parser.error(f"not a directory: {root}")

    manifests = []
    technologies: set[str] = set()
    for path in sorted(candidates(root)):
        relative = path.relative_to(root).as_posix()
        detected = sorted(detect(path))
        technologies.update(detected)
        manifests.append({"path": relative, "signals": detected})

    print(json.dumps({"root": str(root), "technologies": sorted(technologies), "manifests": manifests}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
