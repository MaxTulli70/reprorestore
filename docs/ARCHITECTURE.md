# Architecture baseline

## Recovery Manifest

A service profile declares the Nix configuration reference, mutable state resources, quiescence/capture hooks, restore order, compatibility constraints and validation probes. Secrets are references by default, not embedded data.

## Recovery Bundle

The v0.1 starter creates a normalised archive and a machine-readable evidence file. The funded version will move to a content-addressed bundle layout, optional age encryption and detached signatures while retaining a simple offline verification path.

## Disposable restore runner

The funded implementation will build a clean NixOS VM from the declared configuration, inject the recovery bundle, execute ordered restore adapters, start the service and run semantic probes. The VM is destroyed after evidence is produced.

## Evidence

Results are emitted as JSON: configuration identity, bundle identity, adapter versions, probe outcomes, timings and failure reasons. Evidence is suitable for local audit and CI use.
