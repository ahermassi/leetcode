""" Given a string, determine if it is a palindrome, considering only alphanumeric characters and ignoring cases.
Note: For the purpose of this problem, we define empty string as valid palindrome. """

import unittest2 as unittest


def is_palindrome(s):
    """ Good old two pointers technique. Attention should be paid to the non alphanumeric characters, though.
    Time complexity: O(N) where N is the length of s
    Space complexity: O(1)
    """
    left, right = 0, len(s) - 1
    while left < right:
        while left < right and not s[left].isalnum():
            left += 1  # Move on to next character as long as current one is not alphanumeric
        while left < right and not s[right].isalnum():
            right -= 1
        if s[left].lower() != s[right].lower():
            return False
        left += 1
        right -= 1
    return True


class Test(unittest.TestCase):
    data = [('A man, a plan, a canal: Panama', True),
            ('race a car', False),
            ]

    def test_is_palindrome(self):
        for test_string, result in self.data:
            self.assertEqual(result, is_palindrome(test_string))


if __name__ == '__main__':
    unittest.main()