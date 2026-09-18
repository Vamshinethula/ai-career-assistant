# Project checks

The workflow in `workflows/ci.yml` runs on pushes, pull requests and manual
dispatch. It does not deploy the app. It has read-only repository permissions
and does not require application secrets.

| Job | Checks |
| --- | --- |
| Backend (Windows and Ubuntu) | Python 3.12, pinned dependency install, pip check, all unittest tests, fresh migrations, Alembic model comparison |
| Frontend (Ubuntu) | Node 24, npm ci, lint, comparison-export unit tests, production build |

Tests generate their own signing keys and synthetic data. Migration commands
use the disposable runner checkout. No databases, uploaded resumes or secrets
are uploaded as artifacts. Dependency caches are keyed from dependency files.

The local clean Windows environment passed all 58 backend tests and frontend
install/build/lint before this workflow was added. The first [GitHub run](https://github.com/Vamshinethula/ai-career-assistant/actions/runs/35131859172)
passed all three jobs for commit `1c468db`, including the Linux checks.
The Windows Chrome smoke test remains a separate local check.

After committing and pushing the complete checkpoint, open the repository's
Actions tab and choose **Project checks**. Success means all three job results
are green. If a job fails, open the first failed step and read its error; a
dependency-install failure differs from a test assertion failure. Fix and rerun
rather than hiding a failed check. Manual dispatch becomes available when the
workflow is on the default branch.

These checks do not make deployment automatic or enforce branch protection.
Requiring checks before merges is a separate repository-settings decision.

Reference: GitHub's [Python CI guide](https://docs.github.com/en/actions/tutorials/build-and-test-code/python)
and [Node CI guide](https://docs.github.com/en/actions/tutorials/build-and-test-code/nodejs).

Latest verified feature run: [35356842127](https://github.com/Vamshinethula/ai-career-assistant/actions/runs/35356842127), commit e933920, passed on 2026-09-18: 74 backend tests on each OS and 3 frontend export tests plus lint/build. Browser checks remain local.
