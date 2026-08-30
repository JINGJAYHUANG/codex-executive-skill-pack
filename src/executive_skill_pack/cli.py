from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

from . import __version__
from .catalog import load_catalog, load_routes, skill_map
from .evaluator import evaluate_routing
from .installer import InstallError, plan_install
from .router import route_prompt
from .validator import validate_repository


def _dump(value: Any) -> None:
    print(json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True))


def _root(value: str) -> Path:
    return Path(value).expanduser().resolve()


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="cesp",
        description="Validate, inspect, evaluate, route, and install the Codex Executive Skill Pack.",
    )
    parser.add_argument("--version", action="version", version=f"%(prog)s {__version__}")
    sub = parser.add_subparsers(dest="command", required=True)

    validate = sub.add_parser("validate", help="Validate the repository and all 20 skill contracts.")
    validate.add_argument("--root", default=".")
    validate.add_argument("--strict", action="store_true")
    validate.add_argument("--json", action="store_true")

    listing = sub.add_parser("list", help="List skills in canonical order.")
    listing.add_argument("--json", action="store_true")
    listing.add_argument("--layer", choices=[
        "intelligence",
        "engineering-execution",
        "decision-learning",
        "orchestration-operations",
    ])

    show = sub.add_parser("show", help="Show one machine-readable skill contract.")
    show.add_argument("name")
    show.add_argument("--json", action="store_true")

    route = sub.add_parser("route", help="Run the deterministic reference router.")
    route.add_argument("prompt", nargs="+")
    route.add_argument("--minimum-score", type=int)
    route.add_argument("--json", action="store_true")
    route.add_argument("--explain", action="store_true")

    evaluate = sub.add_parser("eval", help="Run routing and policy evaluation fixtures.")
    evaluate.add_argument("--root", default=".")
    evaluate.add_argument("--json", action="store_true")
    evaluate.add_argument("--show-passes", action="store_true")

    catalog = sub.add_parser("catalog", help="Print canonical catalog or route graph JSON.")
    catalog.add_argument("kind", choices=["skills", "routes"])

    install = sub.add_parser("install", help="Preview or apply a bounded local installation.")
    install.add_argument("--target", required=True)
    install.add_argument("--layout", choices=["repo-skills", "plugin"], required=True)
    install.add_argument(
        "--skills",
        help="Comma-separated skill names; omit to install all 20.",
    )
    install.add_argument("--apply", action="store_true")
    install.add_argument("--replace", action="store_true")
    install.add_argument("--json", action="store_true")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)

    if args.command == "validate":
        report = validate_repository(_root(args.root), strict=args.strict)
        if args.json:
            _dump(report.as_dict())
        else:
            print(
                f"validation: {'PASS' if report.ok else 'FAIL'} | "
                f"errors={report.errors} warnings={report.warnings}"
            )
            for issue in report.issues:
                print(f"{issue.severity.upper()} {issue.code} {issue.path}: {issue.message}")
        return 0 if report.ok else 1

    if args.command == "list":
        rows = load_catalog()["skills"]
        if args.layer:
            rows = [row for row in rows if row["layer"] == args.layer]
        if args.json:
            _dump(rows)
        else:
            for row in rows:
                activation = "explicit-only" if row["explicit_only"] else "contextual"
                print(
                    f"{row['id']:02d}  {row['name']:<32} "
                    f"{row['layer']:<26} {activation}"
                )
        return 0

    if args.command == "show":
        item = skill_map().get(args.name)
        if item is None:
            print(f"unknown skill: {args.name}", file=sys.stderr)
            return 2
        if args.json:
            _dump(item)
        else:
            print(f"{item['display_name']} ({item['name']})")
            print(f"Layer: {item['layer']}")
            print(f"Activation: {'explicit-only' if item['explicit_only'] else 'contextual'}")
            print(f"Risk: {item['risk']}")
            print(f"Purpose: {item['purpose']}")
            print("Permissions: " + ", ".join(item["permissions"]))
        return 0

    if args.command == "route":
        prompt = " ".join(args.prompt)
        result = route_prompt(prompt, minimum_score=args.minimum_score)
        if args.json:
            _dump(result.as_dict())
        else:
            print(f"status: {result.status}")
            print(f"selected: {result.selected or 'DIRECT / NO SKILL'}")
            if args.explain:
                for candidate in result.candidates[:5]:
                    print(
                        f"- {candidate.name}: score={candidate.score} "
                        f"explicit={candidate.explicit} "
                        f"matches={list(candidate.matches)} "
                        f"penalties={list(candidate.penalties)}"
                    )
        return 0

    if args.command == "eval":
        report = evaluate_routing(_root(args.root))
        if args.json:
            _dump(report.as_dict())
        else:
            print(
                f"routing eval: {'PASS' if report.ok else 'FAIL'} | "
                f"passed={report.passed}/{report.total}"
            )
            for result in report.results:
                if args.show_passes or not result.passed:
                    marker = "PASS" if result.passed else "FAIL"
                    print(
                        f"{marker} {result.case_id}: selected={result.selected!r} "
                        f"status={result.status} {result.note}"
                    )
        return 0 if report.ok else 1

    if args.command == "catalog":
        _dump(load_catalog() if args.kind == "skills" else load_routes())
        return 0

    if args.command == "install":
        names = None
        if args.skills:
            names = [item.strip() for item in args.skills.split(",")]
        try:
            plan = plan_install(
                Path(args.target),
                layout=args.layout,
                names=names,
                apply=args.apply,
                replace=args.replace,
            )
        except InstallError as exc:
            print(f"install error: {exc}", file=sys.stderr)
            return 2
        if args.json:
            _dump(plan.as_dict())
        else:
            mode = "APPLY" if args.apply else "PREVIEW"
            print(
                f"{mode}: {plan.layout} -> {plan.target} | "
                f"skills={len(plan.skills)} changes={plan.changes} conflicts={plan.conflicts}"
            )
            for item in plan.files:
                print(f"{item.action.upper():9} {item.path}")
        return 0

    raise AssertionError(f"unhandled command: {args.command}")
