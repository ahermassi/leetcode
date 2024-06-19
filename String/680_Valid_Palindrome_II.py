""" Given a non-empty string s, you may delete at most one character. Judge whether you can make it a palindrome. """

import unittest2 as unittest


def valid_palindrome(s):
    """ An important thing to notice is that once we verify two characters match at positions i and j, we only care
        about the indices between i and j.

        For example, with s = 'racecar', after verifying that s[0] and s[6] are the same character, we only care about
        indices 1 through 5, which represent the substring 'aceca'. If 'aceca' is a palindrome, then 'racecar' is a
        palindrome as well.

        For our purposes, we can basically pretend that matched characters no longer exist. For example, after verifying
        that the first and last characters of 'racecar' match, we can reframe the problem as checking if 'aceca' can be
        a palindrome with at most one deletion.

        If s can be a palindrome after one deletion, the deletion must be of one of the mismatched characters.
        This leaves us two scenarios:

            1- s is a palindrome - great, we can just return true.

            2- Somewhere in s, there will be a pair of mismatched characters. We must use the allowed deletion on one of
                 these characters. Try both options - if neither results in a palindrome, then return false. Otherwise,
                 return true. We can "delete" the character at i by moving the bounds to (i + 1, j). Likewise, we can
                 "delete" the character at j by moving the bounds to (i, j - 1).

    Time complexity: O(N), each character is visited at most once
    Space complexity: O(1)
    """

    def is_palindrome(left, right):
        while left < right:
            if s[left] != s[right]:
                return False
            left += 1
            right -= 1
        return True

    left, right = 0, len(s) - 1
    while left < right:
        if s[left] != s[right]:
            # Found a mismatched pair - try both deletions
            return is_palindrome(left + 1, right) or is_palindrome(left, right - 1)
        left += 1
        right -= 1
    return True


class Test(unittest.TestCase):
    data = [('abca', True), ('ecced', True), ('notaplindrome', False)]

    def test_valid_palindrome(self):
        for test_string, result in self.data:
            self.assertEqual(result, valid_palindrome(test_string))


if __name__ == '__main__':
    unittest.main()