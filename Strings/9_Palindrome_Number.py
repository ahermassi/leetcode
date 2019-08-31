""" Determine whether an integer is a palindrome. An integer is a palindrome when it reads the same backward as forward.
"""

import unittest2 as unittest


def is_palindrome_v1(x):
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


def is_palindrome_v2(x):
    """ Reverse the number and see if it is equal to the original number.
    Time complexity: O(log10 x), since we divide the input by 10 in every iteration
    Space complexity: O(1)
    """
    if x < 0:
        return False
    p, reverse = x, 0
    while p:
        reverse = reverse * 10 + p % 10
        p = p // 10
    return reverse == x


class Test(unittest.TestCase):
    data = [(121, True), (-123, False), (10, False)]

    def test_is_palindrome(self):
        for test_number, result in self.data:
            self.assertEqual(result, is_palindrome_v1(test_number))
            self.assertEqual(result, is_palindrome_v2(test_number))


if __name__ == '__main__':
    unittest.main()
