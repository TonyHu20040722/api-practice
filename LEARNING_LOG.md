# Learning Log

Entries are append-only. Add a new dated entry for later work or corrections;
do not rewrite earlier results. Week 4 identifies the Sep 13–19 study-material
calendar grouping; it does not mean four API project stages were completed.

## 2026-09-19 — Week 4 (Sep 13–19): package completed local exercises

### Learned

The exercises cover dictionary accumulation, sorting by two criteria, return
types, status boundaries, and consecutive runs. I confirmed that I personally
attempted and revised the exercises and can explain them. This entry records
their current state; it does not claim all learning happened on this date.

### Built

Packaged the completed counting, error-summary, and recovery implementations
into an importable source module. The final function bodies were preserved.
AI assisted with repository preparation, documentation, and moving the existing
16 exercise cases into a standard `unittest` suite. Original learning files were
left unchanged outside this project. Earlier teaching examples and incomplete
starter scaffolding are not included in this public candidate.

### Verified

On 2026-09-19, the local suite ran with Python 3.9.6: **16 tests passed, zero
failures or errors**. The six summary tests and ten recovery tests use the
completed exercises' input and expected-output cases. The new harness raises
assertion failures instead of merely printing a failure message.

### Evidence

- Implementation: `src/api_practice/analysis.py`.
- Reproducible checks: `tests/test_analysis.py`.
- Command: `PYTHONPATH=src python3 -m unittest discover -s tests -v`.
- Observed result: `Ran 16 tests` followed by `OK`.
- Examples: the summary returns `[("b", 2), ("a", 1)]` for the README input;
  the recovery example returns `2` for a required run of two and `-1` for three.

This is local verification. No HTTP integration, deployment, CI run, or
performance measurement is claimed.

### What I Can Explain Now

- Why a dictionary can count repeated failures while a set of names cannot.
- Why the sorting key uses both the negative count and the endpoint name.
- Why recovery accepts only 200–299, although summary failures start at 400.
- Why a non-success resets the recovery run and why the returned index is the
  ending index of the first qualifying run.
- Why `needed_run` determines the result and `current_run` is redundant.
- Why passing a finite set of tests is not proof of production readiness.

### Next Milestone

Define behavior for invalid inputs, add focused tests for that contract, and
then implement validation. Separately, simplify the redundant recovery state
while keeping the current tests passing. Neither change has been made yet.

## 2026-09-22 — Week 5 (Sep 20–26): permission and name exercises

### Learned

Role grants can be merged with a set, and explicit denials applied after all
grants. A validator can return one error according to a stated rule order:
length, starting character, then first invalid character.

### Built

Added the personally completed practice in `src/api_practice/authorization.py`.
The existing functions, reasoning and example cases were moved here with Codex
help. Earlier intermediate versions remain outside the public project.

### Verified

The standard-library adapter in `tests/test_authorization.py` ran 16 permission
and 32 name examples successfully on 2026-09-22. The 16 existing analysis tests
also passed. The adapter exposes two test methods that execute the 48 examples;
it does not claim 48 independent unittest methods.

### Evidence

- `src/api_practice/authorization.py`
- `tests/test_authorization.py`
- `PYTHONPATH=src python3 -B -m unittest discover -s tests -v`

### What I Can Explain Now

Why unknown roles grant nothing, why denials win over grants, why a set removes
duplicates, and why length is tested before indexing the first character.
Tony confirmed personal participation and ability to explain these exercises.

### Next Milestone

Define and test malformed-input behavior before using the functions as a
reusable application component. No production security integration is claimed.
