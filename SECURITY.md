# Security policy

## Scope

This repository contains instruction contracts, deterministic routing utilities, and local validation tools. It does not contain credentials or grant access to external systems.

## Permission boundary

A routing result is not authorization. Skills that describe desktop, file, API, workflow, or email capabilities remain subject to the host platform's permissions and user-confirmation requirements.

## Public-data boundary

Do not submit:

- API keys, tokens, cookies, webhooks, or private keys;
- private account exports or correspondence;
- personal memory or user profiles;
- real production logs, internal endpoints, or machine-specific paths;
- proprietary prompts, policies, or client data without permission.

Use synthetic fixtures for issues and pull requests.

## Reporting

Report suspected vulnerabilities through GitHub's private security-advisory channel. Do not include live secrets in an issue. Revoke exposed credentials before reporting them.

## Supported version

Security fixes target the latest tagged release and `main`.
