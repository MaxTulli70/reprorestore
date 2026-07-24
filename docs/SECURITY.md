# Security baseline

- No network upload is required for capture or verification.
- Paths must be relative and traversal is rejected.
- Symbolic links are rejected in v0.1 to avoid ambiguous capture semantics.
- Archive extraction verifies destination containment.
- Every payload file is hashed.
- Secrets are excluded unless an explicit future encrypted-secret adapter is selected.
- Restore hooks will execute only inside an isolated NixOS test VM in the funded version.
- The project will commission an independent security review before v1.0.
