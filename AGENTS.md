# AGENTS.md

## Purpose

This document defines mandatory workflow requirements for future coding agents working on `simuci`.

## Required Context Reading (Before Any Edit)

Every agent must read the following files before implementing changes:

1. `README.md`
2. `docs/index.md`
3. `docs/architecture.md`
4. `docs/function-profile.md` (if present)
5. `.github/copilot-instructions.md`

## Documentation Policy

- All new and updated documentation must be written in English.
- If architecture or behavior changes, documentation updates must be included in the same change set.
- Keep terminology consistent across code, tests, and docs.

## Contribution Policy Context

- Public direct commits are closed.
- Contribution appeals and access requests should be directed to: `gabrielpazruiz02@gmail.com`.

## Testing and Quality Expectations

- Run `pytest` after code or test edits.
- Keep typing strict and avoid untyped public surfaces.
- Prefer minimal, focused changes and avoid unrelated refactors.
