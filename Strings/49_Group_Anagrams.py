""" Given an array of strings, group anagrams together.

Example:

Input: ["eat", "tea", "tan", "ate", "nat", "bat"],
Output:
[
  ["ate","eat","tea"],
  ["nat","tan"],
  ["bat"]
] """

from collections import defaultdict
import unittest2 as unittest


def group_anagrams_v1(strs):
    """ Two strings are anagrams if and only if their sorted strings are equal.
        Maintain a map d where each key K is a sorted string, and each value is the list of strings from the initial
        input that when sorted, are equal to K.
    Time Complexity: O(N * KlogK), where N is the length of strs, and K is the maximum length of a string in strs.
    The outer loop has complexity O(N) as we iterate through each string. Then, we sort each string in O(KlogK) time.
    Space Complexity: O(N)
    """
    d = defaultdict(list)
    for s in strs:
        d[''.join(sorted(s))].append(s)  # sorted('abc') == ['a', 'b', 'c'], array is not hashable, which means it is
        # not allowed to be a key
    return d.values()


class Test(unittest.TestCase):
    data = [(['eat', 'tea', 'tan', 'ate', 'nat', 'bat'], [
        ['ate', 'eat', 'tea'],
        ['nat', 'tan'],
        ['bat']
    ])
            ]

    def test_group_anagrams(self):
        for test_strings, result in self.data:
            self.assertEqual(result, group_anagrams_v1(test_strings))


if __name__ == '__main__':
    unittest.main()
