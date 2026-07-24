# RFC-0001: Recovery Manifest and Verifiable Restore Evidence

Status: public review draft  
Date: 24 July 2026  
Project: ReproRestore  
Licence: Apache-2.0

## Summary

ReproRestore proposes a small, machine-readable Recovery Manifest for declaring the mutable state and ordered recovery operations required to reconstruct a stateful internet service in a clean NixOS environment.

The manifest is not a backup format and does not prescribe a storage provider. It links recovery material, service configuration, adapters, restore order, validation probes and evidence requirements so that a clean runner can answer one bounded question:

> Can this declared service be reconstructed from this recovery material, and what evidence supports the result?

## Problem

Reproducible system configuration does not contain mutable service state. A NixOS configuration may recreate packages, units and settings while leaving databases, uploaded files, keys and application-specific restore order undefined. Archive integrity alone does not prove application-level recoverability.

Current recovery procedures are commonly expressed as operator notes, scripts or implementation-specific backup commands. These are difficult to validate before an incident and difficult for independent tools to inspect.

## Proposed core model

A Recovery Manifest should identify:

- manifest and schema version;
- service identity and intended NixOS configuration reference;
- recovery inputs and integrity expectations;
- ordered adapters and restore dependencies;
- destination paths or logical state targets;
- safety and isolation requirements;
- semantic probes required after restoration;
- evidence and report output requirements;
- declared limitations and unsupported state.

The current v0.1 repository uses TOML and already validates a narrow manifest, captures deterministic filesystem state and verifies integrity evidence. The funded target will refine the model through implementation and public review rather than treating the schema as complete in advance.

## Result model

A production report should distinguish at least:

- `recovered`: all required restore stages and semantic probes passed;
- `recovered_with_warnings`: required checks passed but non-critical limitations remain;
- `failed`: a required restore stage or semantic probe failed;
- `unknown`: the runner could not establish a required fact from available material or evidence.

Each result must identify the failing stage, adapter, probe, evidence reference and reproducible invocation context.

## Security properties

The restore runner must assume that recovery material may be malformed or hostile. Required controls include:

- clean disposable execution environments;
- safe archive extraction and path validation;
- bounded adapter execution;
- explicit secret-handling rules;
- no implicit network access unless declared;
- resource limits and timeouts;
- immutable evidence output outside the restored guest;
- no new cryptographic primitives.

## Interoperability boundaries

ReproRestore does not replace backup tools, object storage, migration platforms or NixOS deployment systems. Existing tools may produce recovery material; ReproRestore verifies whether declared material can reconstruct a working service.

The project is intentionally separate from HostCaps. HostCaps evaluates whether an environment declares the capabilities required by a service. ReproRestore executes a clean recovery and validates the resulting application state.

## Initial reference scope

The proposed v1.0 implementation scope is:

- filesystem state;
- PostgreSQL;
- SQLite;
- MariaDB;
- Forgejo reference profile;
- Nextcloud reference profile;
- HTTP/API, database and file-level semantic probes;
- machine-readable evidence reports;
- NixOS disposable-VM execution.

## Questions for reviewers

1. Which manifest fields are essential for operators but currently missing?
2. Should restore ordering use an explicit DAG, a linear phase model or both?
3. How should secret references be represented without embedding secret values?
4. Which evidence should be mandatory for a result to be called `recovered`?
5. Which application-level probes are most useful for Forgejo and Nextcloud?
6. Which existing NixOS, backup or recovery formats should have documented mappings?
7. Are the four result states sufficiently precise for CI and operator use?

## Review process

Feedback is requested through the repository RFC issue. Proposed changes should identify the affected field, expected interoperability benefit, security implications and a concrete example or test fixture where possible.
