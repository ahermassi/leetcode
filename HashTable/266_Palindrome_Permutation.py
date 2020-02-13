""" Given a string, determine if a permutation of the string could form a palindrome. """

from collections import Counter, defaultdict
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


def can_permute_palindrome_v2(s):
    """ Instead of first traversing over the string s for finding the number of occurrences of each element and then
        determining the count of characters with odd number of occurrences in s, we can determine the value of count on
        the fly while traversing over s. If the value of the entry just updated in the map happens to be odd, we
        increment the value of 'odd' to indicate that one more character with odd number of occurrences has been found.
        But, if this entry happens to be even, we decrement the value of 'odd' to indicate that the number of
        characters with odd number of occurrences has reduced by one.
        But, in this case, we need to traverse till the end of the string to determine the final result, unlike the
        last approach, where we could stop the traversal over the map as soon as the count exceeded 1.
    Time complexity: O(N)
    Space complexity: O(1)
    """
    counter, odd = defaultdict(int), 0
    for c in s:
        counter[c] += 1
        if counter[c] % 2:
            odd += 1
        else:
            odd -= 1
    return odd <= 1


class Test(unittest.TestCase):
    data = [('code', False), ('aab', True), ('carerac', True)]

    def test_can_permute_palindrome(self):
        for test_s, result in self.data:
            self.assertEqual(result, can_permute_palindrome_v1(test_s))
            self.assertEqual(result, can_permute_palindrome_v2(test_s))


if __name__ == '__main__':
    unittest.main()
