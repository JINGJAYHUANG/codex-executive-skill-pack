# Security Policy

## Supported version

Security fixes are currently applied to the latest `0.1.x` release line.

## Scope

This repository is a skill-only plugin. It intentionally ships no MCP server, account connector, authentication material, desktop driver, or hidden background service.

Report problems involving:

- unsafe activation or permission escalation;
- an instruction that could expose secrets or private data;
- path traversal or destructive behavior in the installer;
- a public-tree secret or personal-information leak;
- supply-chain risks in workflows or release artifacts.

Do not include real credentials, private message content, or sensitive production data in an issue. Use a minimal synthetic reproduction.

## Execution boundary

Skill text cannot grant capabilities. The host's sandbox, tool permissions, account authorization, and approval controls remain authoritative.
