""" Reorder the logs so that all of the letter-logs come before any digit-log. The letter-logs are ordered
lexicographically ignoring identifier, with the identifier used in case of ties. The digit-logs should be put in
their original order. """

import unittest2 as unittest


def reorder_log_files(logs):
    """ Pretty straightforward.
    Time complexity: O(N)
    Space complexity: O(N)
    """
    letter_logs = [log for log in logs if log.split()[1].isalpha()]
    digit_logs = [log for log in logs if log.split()[1].isdigit()]
    # The trick here is to sort according to 2 criteria, and that's what the lambda does: returns a tuple. In case of
    # ties with the first criteria, the second one is used
    letter_logs.sort(key=lambda s: (s.split()[1:], s.split()[0]))

    return letter_logs + digit_logs


class Test(unittest.TestCase):
    data = [(["a1 9 2 3 1", "g1 act car", "zo4 4 7", "ab1 off key dog", "a8 act zoo"],
             ["g1 act car", "a8 act zoo", "ab1 off key dog", "a1 9 2 3 1", "zo4 4 7"])]

    def test_next_greater_element(self):
        for test_logs, result in self.data:
            self.assertEqual(result, reorder_log_files(test_logs))


if __name__ == '__main__':
    unittest.main()
