# ReproRestore delivery milestones and acceptance criteria

This document separates the public v0.1 baseline from the proposed funded v1.0 work. Pre-existing code and proposal preparation are not charged to the grant.

## Baseline B0 — public pre-grant evidence

Status: implemented.

Acceptance evidence:

- public repository and Apache-2.0 licence;
- installable Python CLI;
- TOML manifest validation;
- deterministic filesystem capture;
- per-file SHA-256 evidence;
- safe archive handling and tamper detection;
- automated tests;
- Nix flake and CI workflow;
- reproducible demo instructions.

## M1 — Recovery Manifest review draft

Target: month 1.

Outputs:

- Recovery Manifest specification draft;
- JSON Schema or equivalent machine-readable validation artefact;
- versioning and extension rules;
- threat-model update;
- public RFC review round.

Acceptance criteria:

- every normative field has semantics, type, required/optional status and example;
- invalid fixtures cover missing, conflicting and unsafe declarations;
- specification and implementation validation agree on the conformance corpus;
- review issues and dispositions are public.

## M2 — Disposable NixOS restore runner

Target: months 2–3.

Outputs:

- clean NixOS VM runner;
- bounded execution, resource limits and timeouts;
- deterministic input mounting and evidence export;
- network-isolation policy.

Acceptance criteria:

- a restore run starts from a clean image with no state inherited from the host;
- undeclared host paths and network access are unavailable;
- timeout, resource-limit and guest-failure cases generate machine-readable failures;
- the evidence report records Nix configuration reference, runner version and input fingerprints.

## M3 — State adapters

Target: months 3–5.

Outputs:

- filesystem adapter;
- PostgreSQL adapter;
- SQLite adapter;
- MariaDB adapter;
- adapter conformance fixtures.

Acceptance criteria:

- each adapter completes at least one successful clean restore fixture;
- corrupt, incomplete and version-incompatible fixtures fail explicitly;
- adapters declare supported versions and required external tools;
- repeated execution from identical inputs produces equivalent evidence;
- unsafe paths, embedded credentials and undeclared side effects are rejected or flagged.

## M4 — Semantic probes and application profiles

Target: months 5–6.

Outputs:

- probe interface;
- HTTP/API, database and filesystem probes;
- Forgejo profile;
- Nextcloud profile.

Acceptance criteria:

- Forgejo recovery verifies service reachability, expected repository visibility and database state;
- Nextcloud recovery verifies service reachability, expected account/file state and database consistency;
- a service that starts but lacks required application state is not reported as recovered;
- failed probes include reproducible evidence and diagnostic context.

## M5 — Evidence format and integration surface

Target: month 7.

Outputs:

- stable machine-readable report format;
- CLI and library interfaces;
- CI integration example;
- provenance and fingerprint documentation.

Acceptance criteria:

- reports distinguish `recovered`, `recovered_with_warnings`, `failed` and `unknown`;
- every required stage and probe has a rule-level result;
- equivalent runs are diffable without volatile noise;
- a clean external consumer can parse reports without importing private ONMAKE code.

## M6 — Security review, documentation and v1.0 release

Target: month 8.

Outputs:

- independent security review;
- remediation log;
- installation and operator documentation;
- accessibility-reviewed HTML documentation;
- tagged v1.0 release and public roadmap.

Acceptance criteria:

- no unresolved critical or high-severity review finding at release;
- medium findings have remediation or documented disposition;
- all release tests pass in CI and through `nix flake check`;
- documentation enables a new contributor to run both reference profiles from a clean checkout;
- release artefacts contain no production data, secrets or proprietary dependencies.

## Cross-project independence

ReproRestore does not depend on HostCaps, LINKALL, xTdC or other proprietary ONMAKE systems. No funded hour or output may be charged to another proposal. Optional future integrations must preserve independent operation and the Apache-2.0 licence.
