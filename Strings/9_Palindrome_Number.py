""" Determine whether an integer is a palindrome. An integer is a palindrome when it reads the same backward as forward.
"""

import unittest2 as unittest


def is_palindrome(x):
    """ Convert x to a string and verify if it's a palindrome. Pretty straightforward.
    Time complexity: O(N)
    Space complexity: O(N)
    """
    s = str(x)
    left, right = 0, len(s) - 1
    while left < right:
        if s[left] != s[right]:
            return False
        left += 1
        right -= 1
    return True


class Test(unittest.TestCase):
    data = [(121, True), (-123, False), (10, False)]

    def test_is_palindrome(self):
        for test_number, result in self.data:
            self.assertEqual(result, is_palindrome(test_number))


if __name__ == '__main__':
    unittest.main()
