"""Run the submitted permission and name-validation example cases."""

import unittest

from api_practice.authorization import test_effective_permissions, test_name_error


class AuthorizationPracticeTests(unittest.TestCase):
    def test_effective_permissions_cases(self):
        self.assertEqual(test_effective_permissions(), 16)

    def test_name_error_cases(self):
        self.assertEqual(test_name_error(), 32)


if __name__ == "__main__":
    unittest.main()
