# ReproRestore v0.1 reproducible demo

This demo exercises the public pre-grant baseline. It validates the manifest, creates a deterministic recovery bundle, verifies the bundle and runs the automated tests.

## Requirements

- Python 3.11 or later; or
- Nix with flakes enabled.

## Python path

```bash
git clone https://github.com/MaxTulli70/reprorestore.git
cd reprorestore
python -m venv .venv
. .venv/bin/activate
python -m pip install -e .

reprorestore inspect examples/demo/reprorestore.toml
reprorestore capture examples/demo/reprorestore.toml \
  --source-root examples/demo \
  --output /tmp/reprorestore-demo.tar.gz
reprorestore verify /tmp/reprorestore-demo.tar.gz
python -m unittest discover -s tests -v
```

Expected baseline behaviour:

- the manifest is accepted;
- the bundle is written to `/tmp/reprorestore-demo.tar.gz`;
- verification reports valid integrity evidence;
- the unit-test suite passes;
- modifying captured content or unsafe archive paths causes verification or extraction checks to fail.

## Clean Nix path

```bash
git clone https://github.com/MaxTulli70/reprorestore.git
cd reprorestore
nix run . -- inspect examples/demo/reprorestore.toml
nix flake check
```

## What this demo proves

The v0.1 baseline already demonstrates:

- executable manifest validation;
- deterministic ordering and normalised archive metadata;
- per-file SHA-256 evidence;
- safe relative-path handling;
- integrity verification and tamper detection;
- repeatable automated tests;
- Nix packaging and test execution.

It does not yet prove production-grade restoration of PostgreSQL, MariaDB, SQLite or complete Forgejo/Nextcloud instances. Those are explicitly funded v1.0 targets and have separate acceptance criteria in `MILESTONES.md`.

## Reporting a result

When opening an issue, include:

- operating system and architecture;
- Python or Nix version;
- exact command;
- complete error output;
- whether the checkout was clean;
- the commit SHA tested.

Do not attach real recovery material containing personal data, secrets or production credentials.
