# ReproRestore

[![CI](https://github.com/MaxTulli70/reprorestore/actions/workflows/ci.yml/badge.svg)](https://github.com/MaxTulli70/reprorestore/actions/workflows/ci.yml)

ReproRestore is an implementation-ready baseline for **verifiable, reproducible recovery of stateful internet services**. It complements NixOS's reproducible system configuration by describing, capturing and checking the mutable state that configuration management does not contain.

This starter repository is intentionally narrow. It proves that ONMAKE is not submitting a concept-only proposal: a working command-line baseline, manifest format, integrity evidence and automated tests already exist before grant start. Pre-existing work is not included in the requested budget.

## Current v0.1 baseline

- TOML recovery manifest validation
- deterministic ordering and normalised archive metadata
- SHA-256 evidence for every captured file
- safe relative-path handling and archive extraction checks
- integrity verification and tamper detection
- Python unit tests
- Nix flake for packaging and test execution

## Quick start

```bash
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

The same tests can be run directly from a clean checkout without installing the package:

```bash
PYTHONPATH=src python -m unittest discover -s tests -v
```

With Nix:

```bash
nix run . -- inspect examples/demo/reprorestore.toml
nix flake check
```

## Funded implementation target

The NGI Fediversity project will turn this baseline into a production-grade, reusable recovery verification toolchain:

1. normative Recovery Manifest v1.0;
2. NixOS disposable-VM restore runner;
3. adapters for filesystem, PostgreSQL, SQLite and MariaDB state;
4. Forgejo and Nextcloud reference service profiles;
5. semantic probes and signed machine-readable evidence;
6. documentation, accessibility, security review and upstream engagement.

## Public review and delivery evidence

- [RFC-0001: Recovery Manifest and Verifiable Restore Evidence](docs/RFC-0001-RECOVERY-MANIFEST.md)
- [Reproducible v0.1 demo](docs/DEMO.md)
- [Milestones and acceptance criteria](MILESTONES.md)

Technical feedback is requested on manifest semantics, restore ordering, secret references, evidence requirements, application probes and mappings to existing NixOS or recovery formats. Use the public RFC issue so that proposals and dispositions remain inspectable.

## Non-goals

ReproRestore is not a hosting control panel, cloud scheduler, backup storage service or complete provider-migration platform. It answers one bounded question: **can the declared service actually be reconstructed from this recovery material in a clean, reproducible environment?**

## License

Apache License 2.0. The project is independent of ONMAKE's patent-pending systems; no ONMAKE patent rights are required to implement, use, modify or redistribute ReproRestore.

## Project status and funding scope

Version 0.1 is pre-existing implementation work by ONMAKE S.r.l. It demonstrates the core manifest, deterministic capture, integrity evidence, verification and test approach. The proposed NGI Fediversity work starts from this public baseline and funds only the defined production-grade extensions, independent review, documentation and upstream integration.

## Maintainer

Massimiliano Tulli — CEO & Technical Director, ONMAKE S.r.l.

Website: https://www.onmake.it  
Project contact: maxtulli@onmake.it
