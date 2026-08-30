from __future__ import annotations

import argparse
import json
import shutil
import sys
from pathlib import Path
from typing import Any

from . import __version__
from .catalog import catalog_sha256, load_skills, skill_map
from .router import route
from .validation import summary


def _json_dump(payload: Any) -> None:
    print(json.dumps(payload, indent=2, sort_keys=True, ensure_ascii=False))


def _repo_root(value: str | None) -> Path:
    return Path(value or ".").resolve()


def _load_cases(root: Path) -> list[dict[str, Any]]:
    path = root / "evals" / "routing_cases.jsonl"
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def run_evals(root: Path) -> dict[str, Any]:
    cases = _load_cases(root)
    failures: list[dict[str, Any]] = []
    for case in cases:
        decision = route(case["request"], root=str(root))
        expected = case.get("expected")
        expected_disposition = case.get("disposition")
        must_not = case.get("must_not_select")
        passed = True
        if expected is not None and decision.selected != expected:
            passed = False
        if expected_disposition is not None and decision.disposition != expected_disposition:
            passed = False
        if must_not is not None and decision.selected == must_not:
            passed = False
        if not passed:
            failures.append({"case": case, "actual": decision.to_dict()})
    return {
        "status": "pass" if not failures else "fail",
        "cases": len(cases),
        "passed": len(cases) - len(failures),
        "failed": len(failures),
        "failures": failures,
    }


def install_pack(root: Path, target: Path, *, apply: bool, force: bool) -> dict[str, Any]:
    destination = target.resolve() / "codex-executive-skill-pack"
    planned = [".codex-plugin", "skills"]
    result = {"mode": "apply" if apply else "preview", "destination": str(destination), "items": planned}
    if not apply:
        return result
    if destination.exists() and not force:
        raise FileExistsError(f"destination exists: {destination}; use --force to replace it")
    if destination.exists():
        shutil.rmtree(destination)
    destination.mkdir(parents=True)
    for item in planned:
        source = root / item
        if not source.exists():
            raise FileNotFoundError(source)
        shutil.copytree(source, destination / item)
    result["catalog_sha256"] = catalog_sha256(root)
    return result


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="cesp", description="Inspect, validate, route, and install the Codex Executive Skill Pack.")
    parser.add_argument("--version", action="version", version=f"%(prog)s {__version__}")
    sub = parser.add_subparsers(dest="command", required=True)

    validate = sub.add_parser("validate", help="Validate catalog, generated skills, plugin metadata, and evaluations.")
    validate.add_argument("--root", default=".")
    validate.add_argument("--no-generated", action="store_true")

    listing = sub.add_parser("list", help="List the twenty skill contracts.")
    listing.add_argument("--root", default=".")
    listing.add_argument("--json", action="store_true")

    show = sub.add_parser("show", help="Show one skill contract.")
    show.add_argument("name")
    show.add_argument("--root", default=".")

    routing = sub.add_parser("route", help="Route a request without executing any skill.")
    routing.add_argument("request")
    routing.add_argument("--root", default=".")

    evaluate = sub.add_parser("eval", help="Run the committed deterministic routing cases.")
    evaluate.add_argument("--root", default=".")

    install = sub.add_parser("install", help="Preview or copy the skill-only plugin into a chosen directory.")
    install.add_argument("--root", default=".")
    install.add_argument("--target", required=True)
    install.add_argument("--apply", action="store_true", help="Apply the copy; preview is the default.")
    install.add_argument("--force", action="store_true", help="Replace an existing destination when applying.")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    root = _repo_root(getattr(args, "root", "."))
    try:
        if args.command == "validate":
            payload = summary(root, check_generated=not args.no_generated)
            _json_dump(payload)
            return 0 if payload["status"] == "pass" else 1
        if args.command == "list":
            skills = load_skills(root)
            if args.json:
                _json_dump(skills)
            else:
                for skill in skills:
                    print(f"{skill['name']:<32} {skill['invocation']:<14} {skill['status']}")
            return 0
        if args.command == "show":
            skill = skill_map(root).get(args.name)
            if skill is None:
                print(f"unknown skill: {args.name}", file=sys.stderr)
                return 2
            _json_dump(skill)
            return 0
        if args.command == "route":
            _json_dump(route(args.request, root=str(root)).to_dict())
            return 0
        if args.command == "eval":
            payload = run_evals(root)
            _json_dump(payload)
            return 0 if payload["status"] == "pass" else 1
        if args.command == "install":
            _json_dump(install_pack(root, Path(args.target), apply=args.apply, force=args.force))
            return 0
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2
    return 2


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())
