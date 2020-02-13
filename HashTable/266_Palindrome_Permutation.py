""" Given a string, determine if a permutation of the string could form a palindrome. """

from collections import Counter
import unittest2 as unittest


def can_permute_palindrome_v1(s):
    """ All characters must occur in pairs for a string to be permutable into a palindrome, with one exception, if the
        string is of odd length.
        More formally, if the string is of even length, a necessary and sufficient condition for it to be a palindrome
        is that each character in the string appears an even number of times. If the length is odd, all but one
        character should appear an even number of times.
        We traverse over the frequency map created and find the number of characters with odd number of occurrences.
        If this count happens to exceed 1 at any step, we conclude that a palindromic permutation isn't possible for
        the string s.
    Time complexity: O(N)
    Space complexity: O(1), the counter can hold at most 26 characters (or 128 characters)
    """
    counter = Counter(s)
    odd = 0
    for count in counter.values():
        if count % 2 == 1:
            odd += 1
            if odd > 1:
                return False
    return True


class Test(unittest.TestCase):
    data = [('code', False), ('aab', True), ('carerac', True)]

    def test_can_permute_palindrome(self):
        for test_s, result in self.data:
            self.assertEqual(result, can_permute_palindrome_v1(test_s))


if __name__ == '__main__':
    unittest.main()
