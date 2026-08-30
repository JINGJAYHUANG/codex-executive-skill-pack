# Installation

## Recommended distribution: plugin marketplace

The repository includes:

```text
.codex-plugin/plugin.json
.agents/plugins/marketplace.json
```

Add the Git-backed marketplace:

```bash
codex plugin marketplace add JINGJAYHUANG/codex-executive-skill-pack
```

Then install the plugin from the available Plugins Directory or `/plugins` surface. Restart the host when a newly installed skill does not appear.

Availability can vary by ChatGPT or Codex surface and workspace policy. This repository does not bypass administrator controls.

## Repo-scoped direct skills

Codex discovers repository skills under `.agents/skills`.

Install the CLI from a clone:

```bash
python -m pip install --no-deps -e .
```

Preview all files:

```bash
cesp install --layout repo-skills --target .
```

Apply:

```bash
cesp install --layout repo-skills --target . --apply
```

Install selected skills:

```bash
cesp install   --layout repo-skills   --target .   --skills web-intel-harvester,change-sentinel,decision-memo-engine   --apply
```

## Standalone plugin materialization

```bash
cesp install   --layout plugin   --target ./build/codex-executive-skill-pack   --apply
```

This writes a plugin manifest and selected skill folders into the target.

## Safety behavior

The installer:

- defaults to preview;
- prints every target path and expected SHA-256;
- refuses a filesystem root;
- refuses control or cache directories such as `.git`;
- treats different existing files as conflicts;
- requires `--replace` for intentional replacement;
- writes each file through a temporary sibling and atomic replacement.

The installer does not edit Codex configuration, register a marketplace, authenticate an account, or restart a host.

## Uninstall

The CLI intentionally does not provide a broad recursive uninstall command in v0.1.0. Remove only the exact skill folders or plugin directory you reviewed and installed. This avoids a convenience command becoming a destructive filesystem primitive.
