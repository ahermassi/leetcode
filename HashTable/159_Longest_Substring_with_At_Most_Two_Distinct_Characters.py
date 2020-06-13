""" Given a string s , find the length of the longest substring t that contains at most 2 distinct characters. """

import unittest2 as unittest


def length_of_longest_substring_two_distinct(s):
    """ To solve the problem in one pass, let's use sliding window approach with two set pointers left and right
        serving as the window boundaries.
        The idea is to set both pointers in the position 0 and then move right pointer to the right while the window
        contains not more than two distinct characters. If at some point we've got 3 distinct characters, let's move
        left pointer to keep not more than 2 distinct characters in the window.
        Basically that's the algorithm : to move sliding window along the string, to keep not more than 2 distinct
        characters in the window, and to update max substring length at each step.
        Let's use for this purpose a hash map containing all characters in the sliding window as keys and their
        rightmost positions as values. At each moment, this hash map could contain not more than 3 elements.
        The key is to store the last occurrence of each character as the value in the hash map. This way, whenever the
        size of the hash map exceeds 2, we can traverse through the map to find the character with the smallest
        rightmost index and remove that character from our map. Since the range of characters is constrained, we should
        be able to find this character in constant time.
    Time complexity: O(N)
    Space complexity: O(1), additional space is used only for a hash map with at most 2 elements
    """
    last_occ_index, start, res = {}, 0, 0
    for i, c in enumerate(s):
        if c not in last_occ_index and len(last_occ_index) == 2:
            index_to_remove = min(last_occ_index.values())
            del last_occ_index[s[index_to_remove]]
            start = index_to_remove + 1
        last_occ_index[c] = i
        res = max(res, i - start + 1)
    return res


class Test(unittest.TestCase):
    data = [('eceba', 3), ('ccaabbb', 5)]

    def test_length_of_longest_substring_two_distinct(self):
        for test_s, result in self.data:
            self.assertEqual(result, length_of_longest_substring_two_distinct(test_s))


if __name__ == '__main__':
    unittest.main()
