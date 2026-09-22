# API Practice: Status Records and Authorization Exercises

## Problem

Practice Python problems: summarize failed requests by endpoint, find the first
run of consecutive successful statuses, combine role permissions, and validate
a short name. These are ordinary synthetic learning exercises, not actual
assessment questions or a deployed API.

## Data

All data is invented and stored in the source examples or tests. There are no
customer records, credentials, external services, or network calls.

- Authorization examples use synthetic role-to-permission mappings and short
  names. They are standalone policy exercises, not a deployed access system.

- Error summaries accept `(endpoint, status)` pairs. Endpoint names are strings;
  statuses are integers. This exercise counts any status at least 400 as a failure.
- Recovery accepts integer statuses and a positive integer `needed`. Success is
  specifically `200 <= status < 300`. A 300–399 status does not count as a failure
  in the summary, but does interrupt a successful recovery run.

## What I Built

I attempted, revised, and can explain the underlying learning exercises. This
repository presents the final counting, sorting, and recovery functions. Its
packaging, documentation, and conversion of the existing cases to `unittest`
were prepared with AI assistance. It does not claim independent authorship of
every teaching prompt, comment, or supporting test.

- `count_failures`: count failures per endpoint using a dictionary.
- `api_error_summary`: return a list of pairs, highest count first, breaking ties
  alphabetically by endpoint name.
- `recovery_index`: return the zero-based ending index of the first qualifying
  success run, or `-1` when no run qualifies.

The original final function bodies are preserved, including the redundant
`current_run` variable in the recovery implementation.

The authorization exercises add `effective_permissions` and `name_error`.
Their original explanations and 48 example cases are preserved in
`src/api_practice/authorization.py`, and a unittest adapter runs the cases.

## Methods

Counting uses `dict.get(name, 0) + 1`. Sorting uses the key
`(-count, endpoint)` so that counts descend and names ascend. Recovery scans
statuses in order, decreases the remaining required count on success, and resets
it after a non-success.

For permissions, recognized grants are combined in a set, explicit denials
are applied after all grants, and the remaining permissions are sorted. Name
validation checks length, first character, and then other characters in that
order, returning the first applicable error.

With `n` records and `u` endpoints with failures, the summary takes average
`O(n + u log u)` time and `O(u)` extra space. Recovery takes worst-case `O(n)`
time and `O(1)` extra space. These bounds assume fixed-cost comparisons and
average constant-time dictionary operations; input storage is excluded.

## Validation

The test suite carries forward 16 filled exercise cases: six for summaries and
ten for recovery. It checks empty input, filtering, repeated failures, ordering,
status boundaries, interrupted runs, the first qualifying run, and output types.
The authorization adapter runs another 16 permission and 32 name examples.
Unlike the earlier print-only result helper, an assertion failure makes the test
command fail. No external API, CI service, database, or deployment is tested.

## Results

For `[("a", 200), ("b", 500), ("a", 401), ("b", 503)]`, the summary is
`[("b", 2), ("a", 1)]`. For `[500, 200, 204, 500, 200]`, recovery with two
required successes returns `2`; with three, it returns `-1`.

Local verification results are recorded in `LEARNING_LOG.md`. Passing these
cases supports only the behaviors covered; no performance benchmark is claimed.

For the authorization examples, denying `write` leaves only `read` for an
editor granted both. A valid-length name starting with a digit returns `start`.

## Repository Structure

```text
api-practice/
├── README.md
├── LEARNING_LOG.md
├── .gitignore
├── src/api_practice/
│   ├── __init__.py
│   ├── analysis.py
│   └── authorization.py
└── tests/
    ├── test_analysis.py
    └── test_authorization.py
```

## How to Reproduce

Use Python 3. No third-party packages are required. From the project directory
on macOS or Linux, run:

```sh
PYTHONPATH=src python3 -m unittest discover -s tests -v
```

To try the functions interactively, run `PYTHONPATH=src python3`, then:

```python
from api_practice.analysis import api_error_summary, recovery_index
api_error_summary([("a", 200), ("b", 500), ("a", 401), ("b", 503)])
recovery_index([500, 200, 204, 500, 200], 2)
```

## Limitations and Next Steps

This is local algorithm practice, not an HTTP client, HTTP server, monitoring
system, or production project. It assumes valid input and does not validate
malformed records or non-positive `needed` values. It does not implement retries,
authentication, persistent storage, or a database.
The authorization examples assume well-formed inputs; they do not implement
or audit a production access-control policy.

A next learning milestone is to define invalid-input behavior and add tests for
it before changing the functions. Another small refactor is to remove the
redundant recovery counter while preserving existing results. These are proposed
next steps, not completed features.
