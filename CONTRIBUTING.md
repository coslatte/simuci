# Contributing to simuci

Thank you for your interest in contributing to simuci. Public direct commits to the main repository are closed; the preferred route for contributions is via issue requests and coordinated work with the maintainers.

If you believe you need contribution access or want to appeal the contribution policy, contact:

```email
gabrielpazruiz02@gmail.com
```

## How to propose changes

- Open an issue describing the problem or feature request. Include:
  - A short summary of the change.
  - Motivation and rationale.
  - A suggested validation plan (tests or data-driven checks).
- Maintainters will review and, if appropriate, invite a PR or collaborate on a branch.

## Pull request guidelines (when invited)

- Keep changes small and focused; one logical change per PR.
- Include tests for new behavior or bug fixes. Tests must use `pytest` and be placed under `tests/`.
- Run the full test suite locally before opening a PR:

```bash
uv run pytest -q
```

- Ensure typing is complete for any new public functions or classes and follow existing code style (see `.github/copilot-instructions.md`).
- Update documentation in English as part of the same change set if behavior or API changes.

## Documentation policy

- All documentation and inline comments must be written in English.
- Before editing code or docs, read these files as context:
  - `README.md`
  - `docs/index.md`
  - `docs/architecture.md`
  - `docs/function-profile.md` (if present)
  - `.github/copilot-instructions.md`

## Tests and quality

- New code must include tests that verify correctness.
- Use project fixtures in `tests/conftest.py` where appropriate.
- Keep the public API stable; add deprecation notes in docs when changing existing behavior.

## Agent and automation note

Automated agents or bots must follow the workflow specified in `AGENTS.md` and `.github/copilot-instructions.md` prior to making edits.

## Contact

For access requests or appeals: gabrielpazruiz02@gmail.com
