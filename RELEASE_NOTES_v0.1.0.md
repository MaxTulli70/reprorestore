# ReproRestore v0.1.0

Initial public pre-grant baseline for verifiable, reproducible recovery of stateful NixOS services.

## Included

- TOML Recovery Manifest validation;
- deterministic filesystem capture with normalised archive metadata;
- SHA-256 evidence for captured files;
- safe relative-path handling and archive extraction checks;
- integrity verification and tamper detection;
- installable Python CLI;
- automated unit tests and GitHub Actions CI;
- Nix flake packaging and `nix flake check`;
- reproducible demonstration fixture;
- public RFC, threat-aware design notes, milestones and acceptance criteria.

## Scope

This release proves the pre-existing technical baseline. It does not yet include the production disposable NixOS restore runner, database adapters, Forgejo and Nextcloud profiles, semantic probes or independent security review proposed for the funded v1.0 work.

## Verification

```bash
python -m pip install -e .
reprorestore inspect examples/demo/reprorestore.toml
reprorestore capture examples/demo/reprorestore.toml --source-root examples/demo --output /tmp/reprorestore-demo.tar.gz
reprorestore verify /tmp/reprorestore-demo.tar.gz
python -m unittest discover -s tests -v
nix flake check
```

## Licence

Apache License 2.0.
