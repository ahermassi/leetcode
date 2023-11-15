""" Given a string, determine if it is a palindrome, considering only alphanumeric characters and ignoring cases.
Note: For the purpose of this problem, we define empty string as valid palindrome. """

import unittest2 as unittest


def is_palindrome(s):
    """ Good ol' two pointers technique.

        If we take any ordinary string and concatenate its reverse to it, we'll get a palindrome. This leads to an
        interesting insight about the converse: every palindrome half is reverse of the other half.

        Simply speaking, if we were to start in the middle of a palindrome and traverse outwards, we'd encounter the
        same characters, in the exact same order, in both halves!

        Since the input string contains characters that we need to ignore in our palindromic check, it becomes tedious
        to figure out the real middle point of our palindromic input.

        Instead of going outwards from the middle, we could just go inwards towards the middle!
        So, if we start traversing inwards, from both ends of the input string, we can expect to see the same
        characters, in the same order.

        We use two indices to traverse the string, one forwards, the other backwards, skipping non-alphanumeric
        characters, performing case-insensitive comparison on the alphanumeric characters. We return False as soon as
        there is a mismatch. If the indices cross, we have verified that the string is a palindrome.

    Time complexity: O(N), where N is the length of s, in the worst case all characters in the string need to be
    checked exactly once
    Space complexity: O(1)
    """
    left, right = 0, len(s) - 1
    while left < right:
        while left < right and not s[left].isalnum():  # 'left' skips non-alphanumeric characters
            left += 1
        # We can also replace the while loop with the following:
        # if not s[left].isalnum():
        #     left += 1
        #     continue
        while left < right and not s[right].isalnum():  # 'right' skips non-alphanumeric characters
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