""" Given a string, find the first non-repeating character in it and return it's index. If it doesn't exist,
return -1.
Note: You may assume the string contain only lowercase letters. """

import string
from collections import defaultdict
import unittest2 as unittest


def first_uniq_char_v1(s):
    """ The idea is to go through the string and save in a hash map the number of times each character appears in the
    string. And then we go through the string the second time, this time we use the hash map as a reference to check
    if a character is unique or not.
    Time complexity: O(N)
    Space complexity: O(1), if English alphabet is assumed the algorithm is iterating over a constant (26) number of
    bins as keys for hash map.
    """
    counter = defaultdict(int)
    for c in s:
        counter[c] += 1
    for i, c in enumerate(s):
        if counter[c] == 1:
            return i
    return -1


def first_uniq_char_v2(s):
    """ Single pass over the string. Construct a character to index mapping, and when a character is encountered for
        a second time set its map value to 1. We end up with a hash map where all unique characters have values
        different from -1.
    Time complexity: O(N)
    Space complexity: O(1)
    """
    map = defaultdict(int)
    for i, c in enumerate(s):
        if c in map:
            map[c] = -1
        else:
            map[c] = i
    res = float('inf')
    for v in map.values():
        if v != -1:
            res = min(res, v)
    return res if res != float('inf') else -1


def first_uniq_char_v3(s):
    """ Single pass over the string. This is the fastest of all solutions.
        The idea is to iterate over the set of lowercase letters instead of the characters of s, and for each of these
        characters get its index in s if it appears only once in s and append it to 'indices' list. Finally, return
        the minimum value in 'indices' which corresponds to the smallest index of a non-repeating character in s.
    Time complexity: O(N), s.count() takes O(N) and is called |Σ| times, where |Σ| is the size of the alphabet. This
    takes O( |Σ| * n). Since the alphabet in question is just lowercase letters, |Σ| = 26 so this is O(26 * N).
    s.index() also takes O(N) and is called |Σ| times. This takes O( |Σ| * N), or O(N) since |Σ| is constant.
    min() takes O(|Σ|) -> O(1) time.
    Space complexity: O(1), since 'indices' list can hold at most |Σ| values.
    """
    characters = string.ascii_lowercase
    indices = []
    for c in characters:
        if s.count(c) == 1:
            indices.append(s.index(c))
    return min(indices) if indices else -1


class Test(unittest.TestCase):
    data = [('leetcode', 0),
            ('loveleetcode', 2)
            ]

    def test_first_uniq_char(self):
        for test_string, result in self.data:
            self.assertEqual(result, first_uniq_char_v1(test_string))
            self.assertEqual(result, first_uniq_char_v2(test_string))


if __name__ == '__main__':
    unittest.main()

