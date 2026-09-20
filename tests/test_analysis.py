"""The 16 completed exercise cases, using assertions that fail the test run."""

import unittest

from api_practice.analysis import api_error_summary, recovery_index


class ErrorSummaryTests(unittest.TestCase):
    def check_summary(self, records, expected):
        actual = api_error_summary(records)
        self.assertIs(type(actual), list)
        self.assertTrue(all(type(item) is tuple for item in actual))
        self.assertEqual(actual, expected)

    def test_given_example(self):
        self.check_summary(
            [("a", 200), ("b", 500), ("a", 401), ("b", 503)],
            [("b", 2), ("a", 1)],
        )

    def test_empty_input(self):
        self.check_summary([], [])

    def test_all_successes(self):
        self.check_summary([("a", 200), ("b", 204), ("a", 299)], [])

    def test_alphabetical_ties(self):
        self.check_summary([("b", 500), ("a", 500)], [("a", 1), ("b", 1)])

    def test_failure_boundary(self):
        self.check_summary([("a", 399), ("b", 400)], [("b", 1)])

    def test_accumulation_ignores_successes(self):
        self.check_summary(
            [("a", 500), ("a", 200), ("a", 503), ("b", 200)], [("a", 2)]
        )


class RecoveryTests(unittest.TestCase):
    def check_recovery(self, statuses, needed, expected):
        actual = recovery_index(statuses, needed)
        self.assertIs(type(actual), int)
        self.assertEqual(actual, expected)

    def test_given_example_two(self):
        self.check_recovery([500, 200, 204, 500, 200], 2, 2)

    def test_given_example_three(self):
        self.check_recovery([500, 200, 204, 500, 200], 3, -1)

    def test_empty_input(self):
        self.check_recovery([], 2, -1)

    def test_needed_one(self):
        self.check_recovery([500, 204, 200], 1, 1)

    def test_interrupted_run(self):
        self.check_recovery([200, 500, 204], 2, -1)

    def test_run_ends_at_last_item(self):
        self.check_recovery([500, 200, 204], 2, 2)

    def test_success_boundaries(self):
        self.check_recovery([199, 200, 299, 300], 2, 2)

    def test_300_interrupts_run(self):
        self.check_recovery([200, 300, 204], 2, -1)

    def test_first_qualifying_run(self):
        self.check_recovery([200, 204, 500, 200, 204], 2, 1)

    def test_no_successful_statuses(self):
        self.check_recovery([199, 300, 404, 500], 1, -1)


if __name__ == "__main__":
    unittest.main()
