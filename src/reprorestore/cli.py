from __future__ import annotations

import argparse
import hashlib
import json
import os
import sys
import tarfile
import tempfile
import tomllib
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path, PurePosixPath
from typing import Any, Iterable

FORMAT_VERSION = "reprorestore.bundle.v0.1"


class ReproRestoreError(RuntimeError):
    pass


@dataclass(frozen=True)
class Resource:
    name: str
    path: str
    required: bool = True


def _load_manifest(path: Path) -> dict[str, Any]:
    try:
        with path.open("rb") as handle:
            manifest = tomllib.load(handle)
    except (OSError, tomllib.TOMLDecodeError) as exc:
        raise ReproRestoreError(f"cannot read manifest: {exc}") from exc

    project = manifest.get("project")
    resources = manifest.get("resources")
    if not isinstance(project, dict) or not project.get("name"):
        raise ReproRestoreError("manifest requires [project] with a non-empty name")
    if not isinstance(resources, list) or not resources:
        raise ReproRestoreError("manifest requires at least one [[resources]] entry")

    seen: set[str] = set()
    for item in resources:
        if not isinstance(item, dict):
            raise ReproRestoreError("each resources entry must be a table")
        name = item.get("name")
        rel_path = item.get("path")
        if not isinstance(name, str) or not name.strip():
            raise ReproRestoreError("resource name must be a non-empty string")
        if name in seen:
            raise ReproRestoreError(f"duplicate resource name: {name}")
        seen.add(name)
        _safe_relative_path(rel_path)
    return manifest


def _safe_relative_path(value: Any) -> PurePosixPath:
    if not isinstance(value, str) or not value:
        raise ReproRestoreError("resource path must be a non-empty string")
    posix = PurePosixPath(value)
    if posix.is_absolute() or ".." in posix.parts:
        raise ReproRestoreError(f"unsafe resource path: {value}")
    return posix


def _resources(manifest: dict[str, Any]) -> list[Resource]:
    return [
        Resource(
            name=str(item["name"]),
            path=str(item["path"]),
            required=bool(item.get("required", True)),
        )
        for item in manifest["resources"]
    ]


def _iter_files(root: Path) -> Iterable[Path]:
    if root.is_file():
        yield root
        return
    for current, dirs, files in os.walk(root):
        dirs.sort()
        files.sort()
        current_path = Path(current)
        for filename in files:
            path = current_path / filename
            if path.is_symlink():
                raise ReproRestoreError(f"symbolic links are not accepted in v0.1: {path}")
            yield path


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _normalised_tarinfo(tar: tarfile.TarFile, path: Path, arcname: str) -> tarfile.TarInfo:
    info = tar.gettarinfo(str(path), arcname=arcname)
    info.uid = 0
    info.gid = 0
    info.uname = "root"
    info.gname = "root"
    info.mtime = 0
    info.mode = 0o644 if info.isfile() else 0o755
    return info


def cmd_inspect(args: argparse.Namespace) -> int:
    manifest_path = Path(args.manifest).resolve()
    manifest = _load_manifest(manifest_path)
    result = {
        "valid": True,
        "project": manifest["project"],
        "resources": [resource.__dict__ for resource in _resources(manifest)],
    }
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0


def cmd_capture(args: argparse.Namespace) -> int:
    manifest_path = Path(args.manifest).resolve()
    source_root = Path(args.source_root).resolve()
    output = Path(args.output).resolve()
    manifest = _load_manifest(manifest_path)

    entries: list[dict[str, Any]] = []
    selected: list[tuple[Path, str]] = []
    for resource in _resources(manifest):
        rel = _safe_relative_path(resource.path)
        source = source_root.joinpath(*rel.parts)
        if not source.exists():
            if resource.required:
                raise ReproRestoreError(f"required resource is missing: {resource.path}")
            continue
        for file_path in _iter_files(source):
            rel_file = file_path.relative_to(source_root).as_posix()
            entries.append(
                {
                    "resource": resource.name,
                    "path": rel_file,
                    "size": file_path.stat().st_size,
                    "sha256": _sha256(file_path),
                }
            )
            selected.append((file_path, f"payload/{rel_file}"))

    entries.sort(key=lambda item: item["path"])
    evidence = {
        "format": FORMAT_VERSION,
        "project": manifest["project"],
        "created_at": datetime.now(timezone.utc).isoformat(),
        "source_manifest": manifest_path.name,
        "entries": entries,
    }
    canonical_evidence = json.dumps(evidence, sort_keys=True, separators=(",", ":")).encode()
    evidence["evidence_sha256"] = hashlib.sha256(canonical_evidence).hexdigest()

    output.parent.mkdir(parents=True, exist_ok=True)
    with tarfile.open(output, "w:gz", format=tarfile.PAX_FORMAT) as archive:
        with tempfile.NamedTemporaryFile("wb", delete=False) as handle:
            evidence_tmp = Path(handle.name)
            handle.write(json.dumps(evidence, indent=2, sort_keys=True).encode())
        try:
            info = _normalised_tarinfo(archive, evidence_tmp, "evidence.json")
            with evidence_tmp.open("rb") as data:
                archive.addfile(info, data)
            for file_path, arcname in sorted(selected, key=lambda item: item[1]):
                info = _normalised_tarinfo(archive, file_path, arcname)
                with file_path.open("rb") as data:
                    archive.addfile(info, data)
        finally:
            evidence_tmp.unlink(missing_ok=True)

    print(json.dumps({"bundle": str(output), "files": len(entries)}, indent=2))
    return 0


def _safe_extract(archive: tarfile.TarFile, destination: Path) -> None:
    destination = destination.resolve()
    for member in archive.getmembers():
        member_path = destination / member.name
        if not member_path.resolve().is_relative_to(destination):
            raise ReproRestoreError(f"unsafe archive member: {member.name}")
    archive.extractall(destination, filter="data")


def cmd_verify(args: argparse.Namespace) -> int:
    bundle = Path(args.bundle).resolve()
    if not bundle.exists():
        raise ReproRestoreError(f"bundle not found: {bundle}")

    failures: list[str] = []
    with tempfile.TemporaryDirectory(prefix="reprorestore-") as tmp:
        root = Path(tmp)
        with tarfile.open(bundle, "r:gz") as archive:
            _safe_extract(archive, root)
        evidence_path = root / "evidence.json"
        if not evidence_path.exists():
            raise ReproRestoreError("bundle has no evidence.json")
        evidence = json.loads(evidence_path.read_text(encoding="utf-8"))
        if evidence.get("format") != FORMAT_VERSION:
            failures.append("unsupported bundle format")
        for entry in evidence.get("entries", []):
            rel = _safe_relative_path(entry.get("path"))
            payload = root / "payload" / Path(*rel.parts)
            if not payload.exists():
                failures.append(f"missing: {rel.as_posix()}")
                continue
            actual_size = payload.stat().st_size
            actual_hash = _sha256(payload)
            if actual_size != entry.get("size"):
                failures.append(f"size mismatch: {rel.as_posix()}")
            if actual_hash != entry.get("sha256"):
                failures.append(f"hash mismatch: {rel.as_posix()}")

    report = {
        "bundle": str(bundle),
        "status": "PASS" if not failures else "FAIL",
        "failures": failures,
    }
    print(json.dumps(report, indent=2, sort_keys=True))
    return 0 if not failures else 2


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="reprorestore",
        description="Deterministic capture and verification baseline for stateful services.",
    )
    sub = parser.add_subparsers(dest="command", required=True)

    inspect_parser = sub.add_parser("inspect", help="validate and display a manifest")
    inspect_parser.add_argument("manifest")
    inspect_parser.set_defaults(func=cmd_inspect)

    capture_parser = sub.add_parser("capture", help="capture declared state into a deterministic bundle")
    capture_parser.add_argument("manifest")
    capture_parser.add_argument("--source-root", required=True)
    capture_parser.add_argument("--output", required=True)
    capture_parser.set_defaults(func=cmd_capture)

    verify_parser = sub.add_parser("verify", help="verify bundle integrity")
    verify_parser.add_argument("bundle")
    verify_parser.set_defaults(func=cmd_verify)
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    try:
        return int(args.func(args))
    except ReproRestoreError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
