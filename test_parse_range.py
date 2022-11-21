import unittest

from parse_ranges import parse_ranges


class ParseRangesTests(unittest.TestCase):
    """Tests for parse_ranges."""

    def test_three_ranges(self):
        self.assertEqual(
            list(parse_ranges("1-2,4-4,8-10")),
            [1, 2, 4, 8, 9, 10],
        )

    def test_three_ranges_2(self):
        self.assertEqual(
            list(parse_ranges("1-3,4-4,8-11")),
            [1, 2, 3, 4, 8, 9, 10, 11],
        )

    def test_with_spaces(self):
        self.assertEqual(
            list(parse_ranges("0-0, 4-8, 20-21, 43-45")),
            [0, 4, 5, 6, 7, 8, 20, 21, 43, 44, 45],
        )

    # To test bonus 1, comment out the next line
    def test_return_iterator(self):
        numbers = parse_ranges("0-0, 4-8, 20-21, 43-45")
        self.assertEqual(next(numbers), 0)
        self.assertEqual(list(numbers), [4, 5, 6, 7, 8, 20, 21, 43, 44, 45])
        self.assertEqual(list(numbers), [])
        numbers = parse_ranges("100-1000000000000")
        self.assertEqual(next(numbers), 100)

    # To test bonus 2, comment out the next line
    def test_with_individual_numbers(self):
        self.assertEqual(
            list(parse_ranges("0,4-8,20,43-45")),
            [0, 4, 5, 6, 7, 8, 20, 43, 44, 45],
        )

    # To test bonus 3, comment out the next line
    @unittest.expectedFailure
    def test_ignore_arrows(self):
        self.assertEqual(
            list(parse_ranges("0, 4-8, 20->exit, 43-45")),
            [0, 4, 5, 6, 7, 8, 20, 43, 44, 45],
        )


class AllowUnexpectedSuccessRunner(unittest.TextTestRunner):
    """Custom test runner to avoid FAILED message on unexpected successes."""

    class resultclass(unittest.TextTestResult):
        def wasSuccessful(self):
            return not (self.failures or self.errors)


if __name__ == "__main__":
    from platform import python_version
    import sys

    if sys.version_info < (3, 6):
        sys.exit("Running {}.  Python 3.6 required.".format(python_version()))
    unittest.main(verbosity=2, testRunner=AllowUnexpectedSuccessRunner)
