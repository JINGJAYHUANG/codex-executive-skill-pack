# Skills

This directory contains the 20 host-facing Agent Skills.

Each folder must contain:

```text
SKILL.md
agents/openai.yaml
examples.md
```

Do not edit a skill in isolation. Update the canonical record in `../catalog/skills.json`, regenerate the public files, add routing cases, and run the release gate.

The exact folder names are a compatibility contract for the `0.x` series.
