"""Synthetic status-record exercises; these functions make no HTTP requests.

Function bodies are preserved from the completed learning exercises.
Inputs must follow the contracts described in README.md.
"""


def count_failures(records):
    counts = {}

    for endpoint, status in records:
        if status >= 400:
            counts[endpoint] = counts.get(endpoint, 0) + 1

    return counts


def api_error_summary(records):
    counts = count_failures(records)
    return sorted(counts.items(), key=lambda item: (-item[1], item[0]))


def recovery_index(statuses, needed):
    current_run = 0
    needed_run = needed
    for index, status in enumerate(statuses):
        if 200 <= status < 300:
            current_run += 1
            needed_run -= 1
            if needed_run == 0:
                break
        else:
            current_run = 0
            needed_run = needed
    if needed_run == 0:
        return index
    else:
        return -1
