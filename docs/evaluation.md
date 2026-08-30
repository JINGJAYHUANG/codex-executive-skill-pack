# Evaluation methodology

## What is evaluated

The committed suite contains 74 deterministic cases:

- 20 explicit-invocation cases;
- 20 natural-language trigger cases;
- 20 negative-boundary cases;
- 14 cross-domain and safety cases.

Each case records an ID, a request, a kind, and one or more assertions:

- `expected`: the selected candidate;
- `disposition`: `route`, `suggest_explicit`, or `no_route`;
- `must_not_select`: a skill that must not be selected for the boundary request.

## Why negative cases matter

Positive examples alone encourage over-routing. Each skill therefore carries a boundary request designed to ensure that adjacent but unsafe or unnecessary work does not trigger the contract.

Examples include:

- no unbounded screen recording;
- no blind payment submission;
- no secret embedding;
- no unlicensed data redistribution;
- no destructive file deletion without inventory;
- no invented meeting owners;
- no automatic commercial acceptance;
- no confident incident reconstruction without evidence.

## Reference router

The deterministic router exists to make the public contracts testable. It is deliberately simple and transparent. Passing the suite means the committed trigger language and safety dispositions are internally consistent; it does not establish semantic parity with every model or runtime.

## Reproducing the suite

```bash
python scripts/generate_skill_files.py --check
cesp validate
cesp eval
```

The CI matrix runs these checks on Python 3.11, 3.12, and 3.13.

## Adding or changing a contract

A catalog edit must update the generated files and routing cases. Reviewers should inspect:

1. whether the trigger is distinct;
2. whether the non-trigger prevents adjacent overreach;
3. whether explicit-first status matches the action risk;
4. whether downstream routes are necessary rather than decorative;
5. whether the maturity label is supported by evidence.

## Known limitations

Keyword and phrase evaluations do not measure broad language robustness, multilingual routing, adversarial prompt resistance, or actual tool safety. Those require separate runtime-specific evaluations.
