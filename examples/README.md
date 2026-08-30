# Synthetic routing examples

The examples exercise only the deterministic reference router. They do not execute any skill or call external tools.

```bash
cesp route "Collect public web evidence and build a source table from official pages."
cesp route "Reorganize these files safely with a preview and rollback plan."
cesp route "$fileops-guardian: preview a safe rename plan; do not apply."
```

Expected behavior:

- low-risk specialist matches can return `route`;
- high-impact natural-language matches return `suggest_explicit`;
- explicit invocation can select the contract but still grants no external permission;
- ordinary requests that need no specialist can return `no_route`.

All names, requests, and outputs in this directory are synthetic.
