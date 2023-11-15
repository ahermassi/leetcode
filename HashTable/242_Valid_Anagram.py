""" Given two strings s and t , write a function to determine if t is an anagram of s. """

from collections import defaultdict
import unittest2 as unittest


def is_anagram(s, t):
    """ To examine if t is a rearrangement of s, we can count occurrences of each letter in the two strings and
         compare them. First increment the counter for s, then decrement the counter for t. If at any point the counter
         drops below zero, we know that t contains an extra letter not in s and return false immediately. If the strings
         are anagrams, the frequency of each character will cancel out.

         Follow up: What if the inputs contain unicode characters? How would you adapt your solution to such case?
         A hash table is a more generic solution and could adapt to any range of characters (which is what we did).

    Time complexity: O(N), where N is the length of s (or t)
    Space complexity: O(1), the table's size stays constant no matter how large N is
    """
    if len(s) != len(t):
        return False
    counter = defaultdict(int)
    for c in s:
        counter[c] += 1
    for c in t:
        counter[c] -= 1
        if counter[c] < 0:
            return False
    return True


class Test(unittest.TestCase):
    data = [('anagram', 'nagaram', True),
            ('rat', 'car', False)
            ]

    def test_is_anagram(self):
        for test_string1, test_string2, result in self.data:
            self.assertEqual(result, is_anagram(test_string1, test_string2))


if __name__ == '__main__':
    unittest.main()
