""" Given an input string , reverse the string word by word. """

import unittest2 as unittest


def reverse_words(s):
    """ The idea is simple: reverse the whole string and then reverse each word.
    Time complexity: O(N)
    Space complexity: O(1)
    """

    def reverse(left, right):
        while left < right:
            s[left], s[right] = s[right], s[left]
            left += 1
            right -= 1

    n = len(s)
    reverse(0, n - 1)
    start = 0
    while start < n:
        end = start
        while end < n and s[end] != ' ':
            end += 1
        reverse(start, end - 1)
        start = end + 1
    return s


class Test(unittest.TestCase):
    data = [(['t', 'h', 'e', ' ', 's', 'k', 'y', ' ', 'i', 's', ' ', 'b', 'l', 'u', 'e'],
             ['b', 'l', 'u', 'e', ' ', 'i', 's', ' ', 's', 'k', 'y', ' ', 't', 'h', 'e'])]

    def test_reverse_words(self):
        for test_s, result in self.data:
            self.assertEqual(result, reverse_words(test_s))


if __name__ == '__main__':
    unittest.main()
