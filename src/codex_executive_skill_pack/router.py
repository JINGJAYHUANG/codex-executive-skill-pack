from __future__ import annotations

import re
from dataclasses import dataclass, asdict
from typing import Any, Iterable

from .catalog import load_skills

TOKEN_RE = re.compile(r"[a-z0-9]+")


@dataclass(frozen=True)
class RouteCandidate:
    name: str
    score: float
    invocation: str
    explicit: bool
    reasons: tuple[str, ...]

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class RouteDecision:
    request: str
    disposition: str
    selected: str | None
    requires_explicit_invocation: bool
    candidates: tuple[RouteCandidate, ...]
    rationale: str

    def to_dict(self) -> dict[str, Any]:
        payload = asdict(self)
        payload["candidates"] = [candidate.to_dict() for candidate in self.candidates]
        return payload


def _tokens(text: str) -> set[str]:
    return set(TOKEN_RE.findall(text.lower()))


def _explicit_names(request: str, names: Iterable[str]) -> set[str]:
    lower = request.lower()
    found: set[str] = set()
    for name in names:
        if f"${name}" in lower:
            found.add(name)
            continue
        pattern = rf"(?<![a-z0-9-]){re.escape(name)}(?![a-z0-9-])"
        if re.search(pattern, lower):
            found.add(name)
    return found


def _score_skill(request: str, skill: dict[str, Any], explicit: bool) -> RouteCandidate:
    lower = request.lower()
    request_tokens = _tokens(request)
    score = 100.0 if explicit else 0.0
    reasons: list[str] = ["explicit invocation"] if explicit else []

    name_words = set(skill["name"].split("-"))
    overlap = request_tokens & name_words
    if overlap:
        score += 0.75 * len(overlap)
        reasons.append(f"name-token overlap: {', '.join(sorted(overlap))}")

    for trigger in skill["triggers"]:
        trigger_lower = trigger.lower()
        trigger_tokens = _tokens(trigger)
        if trigger_lower in lower:
            score += 12.0
            reasons.append(f"exact trigger: {trigger}")
        elif trigger_tokens:
            ratio = len(request_tokens & trigger_tokens) / len(trigger_tokens)
            if ratio >= 0.67:
                score += 4.0 * ratio
                reasons.append(f"trigger-token match: {trigger}")

    for phrase in skill["avoid_when"]:
        phrase_tokens = _tokens(phrase)
        if phrase.lower() in lower:
            score -= 12.0
            reasons.append(f"avoid phrase: {phrase}")
        elif phrase_tokens and len(request_tokens & phrase_tokens) / len(phrase_tokens) >= 0.8:
            score -= 4.0
            reasons.append(f"avoid-token match: {phrase}")

    return RouteCandidate(
        name=skill["name"],
        score=round(score, 3),
        invocation=skill["invocation"],
        explicit=explicit,
        reasons=tuple(reasons),
    )


def route(request: str, *, root: str | None = None, limit: int = 3) -> RouteDecision:
    text = request.strip()
    if not text:
        return RouteDecision(text, "no_route", None, False, (), "The request is empty.")

    skills = load_skills(root)
    names = [skill["name"] for skill in skills]
    explicit = _explicit_names(text, names)
    candidates = sorted(
        (_score_skill(text, skill, skill["name"] in explicit) for skill in skills),
        key=lambda item: (-item.score, item.name),
    )
    positive = [candidate for candidate in candidates if candidate.score >= 3.0]
    top = positive[0] if positive else None
    shown = tuple(positive[: max(1, limit)])

    if top is None:
        return RouteDecision(text, "no_route", None, False, shown, "No skill crossed the routing threshold.")
    if top.invocation == "explicit_first" and not top.explicit:
        return RouteDecision(
            text,
            "suggest_explicit",
            top.name,
            True,
            shown,
            f"{top.name} is relevant but high-impact and must be explicitly invoked before execution.",
        )
    return RouteDecision(
        text,
        "route",
        top.name,
        False,
        shown,
        f"{top.name} is the smallest sufficient routed skill for this request.",
    )
