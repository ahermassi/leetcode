""" Given a non-empty string s, you may delete at most one character. Judge whether you can make it a palindrome. """

import unittest2 as unittest


def valid_palindrome(s):
    """ We can use the standard two-pointer approach that starts at the left and right of the string and move
        inwards. Whenever there is a mismatch, we can either exclude the character at the left or the right pointer. We
        then check if either substring is a palindrome.
        In other words: check from left and right at the same time until the first different pair. Now we have
        something like a****b, where a and b are different. We need to delete either a or b to make it a palindrome.
    Time complexity: O(N)
    Space complexity: O(N) for the creation of reversed strings using [::-1] notation
    """
    left, right = 0, len(s) - 1
    while left < right and s[left] == s[right]:
        left += 1
        right -= 1
    left_subs, right_subs = s[left:right], s[left + 1:right + 1]  # Deleting right and left characters respectively
    return left_subs == left_subs[::-1] or right_subs == right_subs[::-1]


class Test(unittest.TestCase):
    data = [('abca', True), ('ecced', True), ('notaplindrome', False)]

    def test_valid_palindrome(self):
        for test_string, result in self.data:
            self.assertEqual(result, valid_palindrome(test_string))


if __name__ == '__main__':
    unittest.main()