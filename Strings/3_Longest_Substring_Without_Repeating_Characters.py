""" Given a string, find the length of the longest substring without repeating characters. """

import unittest2 as unittest


def length_of_longest_substring(s):
    """ The basic idea is to keep a hash map which stores the characters in string as keys and their indices as values,
        and use two pointers which define the max substring. Move the right pointer i to scan the string , and
        meanwhile update the hash map. If the character is already in the hash map, then move the left pointer 'start'
        to the right of the same character last found. The reason is that if s[i] has a duplicate in the range
        [start, i) with index i', we can skip all the elements in the range [start, i'] and let 'start' to be i'+1
        directly.
        Note that 'start' and i represent the left and right ends of the sliding window, respectively.
    Time complexity : O(N)
    Space complexity: O(N)
    """
    chars, res, start = {}, 0, 0  # 'start' denotes the left end of the longest substring with no repeating
    # characters we've seen so far
    for i, c in enumerate(s):  # i is the right end of that string, or the right end of our sliding window
        if c in chars:
            start = max(start, chars[c] + 1)  # The variable 'start' is used to indicate the index of first character of
            # this substring. If the repeated character's index is less than 'start' itself, this means the repeated
            # character in the hash map is no longer available at this time and is already outside the window.
            # Consider the input: 'tmsmfdut'
            # When i = s.length()-1, then start = 2 after we've encountered the first repeated 'm', so the current
            # window is start=2, i=7, substring='smfdut'
            # If we just do start = chars[c] + 1, then start will be set to 1 because the first occurrence of 't' was
            # at index 0, and this will give a wrong answer.
            # For this reason, 'start' should not be set to (chars[c] + 1) as this value is less than current value of
            # start = 2, or in simple words (chars[c] + 1) is outside the window start=2 and i=7.
        res = max(res, i - start + 1)
        chars[c] = i
    return res


class Test(unittest.TestCase):
    data = [('abcabcbb', 3), ('bbbbb', 1), ('pwwkew', 3)]

    def test_length_of_longest_substring(self):
        for test_string, result in self.data:
            self.assertEqual(result, length_of_longest_substring(test_string))


if __name__ == '__main__':
    unittest.main()