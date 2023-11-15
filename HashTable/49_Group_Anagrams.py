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
        Maintain a hash map where each key K is a sorted string, and each value is the list of strings from the initial
        input that when sorted are equal to K.

        We will store the key as a hashable tuple, as Python lists are mutable and can't be used as hash table keys.

    Time Complexity: O(N * (K logK)), where N is the number of strings and K is the length of the longest string
    The outer loop has complexity O(N) as we iterate through each string. Then, we sort each string in O(K logK) time.
    Space Complexity: O(N)
    """
    anagrams = defaultdict(list)
    for s in strs:
        key = tuple(sorted(s))
        # sorted('abc') == ['a', 'b', 'c']; array is not hashable, which means it is not allowed to be a key
        anagrams[key].append(s)
    return anagrams.values()


def group_anagrams_v2(strs):
    """ Two strings are anagrams if and only if their character counts (respective number of occurrences of each
        character) are the same. We can transform each string s into a character count, char_count, consisting of 26
        non-negative integers representing the number of a's, b's, c's, etc. We use these counts as the basis for our
        hash map.
    Time complexity: O(N * K), where N is the number of strings and K is the length of the longest string
    Space complexity: O(N)
    """
    anagrams = defaultdict(list)
    for s in strs:
        char_count = [0] * 26
        for c in s:
            char_count[ord(c) - ord('a')] += 1
        anagrams[tuple(char_count)].append(s)  # List is not hashable and can't serve as dict key, so we transform it
        # to tuple
    return anagrams.values()


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
            self.assertEqual(result, group_anagrams_v2(test_strings))


if __name__ == '__main__':
    unittest.main()
