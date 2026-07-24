# Contributing to ReproRestore

ReproRestore is developed in the open. Contributions that improve deterministic recovery, verification, NixOS integration, adapters, documentation, tests, accessibility, or security are welcome.

## Development setup

```bash
python -m venv .venv
. .venv/bin/activate
python -m pip install -e .
python -m unittest discover -s tests -v
```

For a dependency-free checkout test, run:

```bash
PYTHONPATH=src python -m unittest discover -s tests -v
```

## Contribution process

1. Open an issue for substantial design changes.
2. Keep each pull request narrowly scoped.
3. Add or update tests for behavioural changes.
4. Do not commit secrets, personal data, production recovery bundles, or proprietary datasets.
5. Confirm that all contributed material can be released under Apache License 2.0.

## Security issues

Do not disclose vulnerabilities in a public issue. Follow the reporting process in `SECURITY.md`.
