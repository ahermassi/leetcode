""" Given a string, find the length of the longest substring without repeating characters. """

import unittest2 as unittest


def length_of_longest_substring(s):
    """ Reuse previous computation as we iterate through the string. Suppose we know the longest duplicate-free
        substring ending at a given index. The longest duplicate-free substring ending at the next index is either:
            1- The previous substring appended with the element at the next index, if that element does not appear in
               the longest duplicate-free substring at the current index
            2- The substring beginning at the most recent occurrence of the element at the next index + 1
        To perform this case analysis as we iterate, all we need is a hash table storing the most recent occurrence of
        each element, and the longest duplicate-free substring ending at the current element.
        The basic idea is to keep a hash map which stores the characters in string as keys and their indices as values,
        and use two pointers which define the max substring. Move the right pointer 'i' to scan the string, and in the
        meanwhile update the hash map. If the character is already in the hash map, then move the left pointer 'start'
        to the right of the same character last found. The reason is that if s[i] has a duplicate in the range
        [start, i) at index j, we can skip all the elements in the range [start, j] and let 'start' be equal to
        (j + 1) directly.
        Note that 'start' and i represent the left and right ends of the sliding window, respectively.
        Example: s = 'fsfetwenwe'. When we process the element at index 2, the longest duplicate-free substring ending
        at index 1 is from 0 to 1. The hash table tells us that the element at index 2, namely f, appears in that
        substring, so we update the longest substring ending at index 2 to being from index 1 to 2.
        Indices 3-5 introduce fresh elements. Index 6 holds a repeated value, e, which appears within the longest
        substring ending at index 5; specifically, it appears at index 3. Therefore, the longest substring ending at
        index 6 starts at index 4.
    Time complexity : O(N)
    Space complexity: O(N), or O(1) if the set of characters considered is the English alphabet O(26)
    """
    prev_occ_index, res, start = {}, 0, 0  # 'start' denotes the left end of the longest substring with no
    # repeating characters seen so far
    for i, c in enumerate(s):  # i is the right end of that string, or the right end of our sliding window
        if c in prev_occ_index:
            start = max(start, prev_occ_index[c] + 1)  # The variable 'start' is used to indicate the index of first
            # character of this substring. If the repeated character's index is less than 'start' itself, this means
            # the repeated character in the hash map is no longer available at this time and is already outside the
            # window.
            # Consider the input: s = 'tmsmfdut'
            # When i = s.length()-1 = 7, start = 2 after we've encountered the first repeated 'm', so the current
            # window is defined by start=2, i=7, substring='smfdut'
            # If we update start = prev_occ_index['t'] + 1, then 'start' will be equal to 1 because the previous
            # occurrence of 't' is at index 0, and this will give a wrong answer.
            # For this reason, 'start' should not be set to (prev_occ_index[c] + 1) as this value is less than current
            # value of start = 2, or in simple words (last_occurrence_index[c] + 1) is outside the window defined by
            # start=2 and i=7.
        res = max(res, i - start + 1)
        prev_occ_index[c] = i
    return res


class Test(unittest.TestCase):
    data = [('abcabcbb', 3), ('bbbbb', 1), ('pwwkew', 3)]

    def test_length_of_longest_substring(self):
        for test_string, result in self.data:
            self.assertEqual(result, length_of_longest_substring(test_string))


if __name__ == '__main__':
    unittest.main()
