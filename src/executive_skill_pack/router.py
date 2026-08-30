from __future__ import annotations

import re
from dataclasses import dataclass, asdict
from typing import Any

from .catalog import load_catalog


@dataclass(frozen=True)
class Candidate:
    name: str
    score: int
    explicit: bool
    matches: tuple[str, ...]
    penalties: tuple[str, ...]

    def as_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class RouteResult:
    prompt: str
    selected: str | None
    status: str
    minimum_score: int
    candidates: tuple[Candidate, ...]

    def as_dict(self) -> dict[str, Any]:
        return {
            "prompt": self.prompt,
            "selected": self.selected,
            "status": self.status,
            "minimum_score": self.minimum_score,
            "candidates": [item.as_dict() for item in self.candidates],
        }


def _normalize(text: str) -> str:
    lowered = text.casefold().replace("_", " ").replace("-", " ")
    return re.sub(r"\s+", " ", lowered).strip()


def _explicitly_names(prompt: str, name: str) -> bool:
    raw = prompt.casefold()
    escaped = re.escape(name.casefold())
    patterns = [
        rf"(?<![\w-])\${escaped}(?![\w-])",
        rf"(?<![\w-]){escaped}(?![\w-])",
        rf"\buse\s+{escaped}\b",
        rf"\brun\s+{escaped}\b",
        rf"\binvoke\s+{escaped}\b",
    ]
    return any(re.search(pattern, raw) for pattern in patterns)


def _contains(normalized_prompt: str, term: str) -> bool:
    return _normalize(term) in normalized_prompt


def route_prompt(
    prompt: str,
    *,
    catalog: dict[str, Any] | None = None,
    minimum_score: int | None = None,
) -> RouteResult:
    """Return a deterministic reference route for evaluation and debugging.

    This function is not a claim about model routing in every Codex host. It is
    a conservative, inspectable harness for testing the pack's written
    boundaries.
    """
    data = catalog or load_catalog()
    raw_threshold = (
        minimum_score
        if minimum_score is not None
        else data.get("pack", {}).get("routing_minimum_score", 6)
    )
    if isinstance(raw_threshold, bool) or not isinstance(raw_threshold, int):
        raise ValueError("minimum score must be an integer")
    if raw_threshold < 0:
        raise ValueError("minimum score must be non-negative")
    threshold = raw_threshold

    normalized = _normalize(prompt)
    candidates: list[Candidate] = []

    for skill in data["skills"]:
        name = skill["name"]
        explicit = _explicitly_names(prompt, name)
        if skill["explicit_only"] and not explicit:
            continue

        score = 100 if explicit else 0
        matches: list[str] = []
        penalties: list[str] = []

        if explicit:
            matches.append(f"explicit:{name}")

        for phrase in skill.get("phrases", []):
            if _contains(normalized, phrase):
                score += 8
                matches.append(f"phrase:{phrase}")

        for keyword in skill.get("keywords", []):
            if _contains(normalized, keyword):
                weight = 4 if len(_normalize(keyword).split()) > 1 else 2
                score += weight
                matches.append(f"keyword:{keyword}")

        for term in skill.get("anti_keywords", []):
            if _contains(normalized, term):
                score -= 10
                penalties.append(f"anti:{term}")

        if score != 0 or explicit:
            candidates.append(
                Candidate(
                    name=name,
                    score=score,
                    explicit=explicit,
                    matches=tuple(matches),
                    penalties=tuple(penalties),
                )
            )

    candidates.sort(key=lambda item: (-item.score, item.name))
    ranked = tuple(candidates)

    if not ranked:
        return RouteResult(prompt, None, "direct", threshold, ranked)

    # Explicit activation is a user decision, not an implicit relevance score.
    top = ranked[0]
    if top.explicit:
        return RouteResult(prompt, top.name, "skill", threshold, ranked)
    if top.score < threshold:
        return RouteResult(prompt, None, "direct", threshold, ranked)

    # Avoid pretending a close implicit tie is certain.
    if len(ranked) > 1 and top.score - ranked[1].score < 2:
        return RouteResult(prompt, None, "ambiguous", threshold, ranked)

    return RouteResult(prompt, top.name, "skill", threshold, ranked)
