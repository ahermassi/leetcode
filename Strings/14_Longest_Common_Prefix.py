""" Write a function to find the longest common prefix string amongst an array of strings.
If there is no common prefix, return an empty string "". """

import unittest2 as unittest


def longest_common_prefix_v1(strings):
    """ This solution is based on the idea that the longest common prefix is included in or equal to the first string
        in the alphabetical order of the strings list.
        The first thing to understand is that the longest common prefix can only be as long as the shortest string with
        a common prefix in the array. So, when we sort, the shortest string with a common prefix will be the first
        string (assuming ascending order).
        Then, we have to understand that the longest common prefix must apply for ALL array elements. If there's an
        array element that does not have the longest common prefix we've found so far, then there is no prefix, it's
        empty string. So, for example, if the first (in the alphabetical order) string is "aaa" and last string comes
        out to be "baa", then there is no common prefix.
        The first string stands as a BASE LINE for the longest possible common prefix, while the last string acts as a
        verifier that all strings BEFORE the last have this common prefix. Otherwise, it wouldn't have been the last
        string in sorted order.
    Time complexity: O(S) where S is the length of the shortest string in the array
    Space complexity: O(1)
    """
    if not strings:
        return ''
    shortest, longest = min(strings), max(strings)
    i = 0
    while i < len(shortest) and shortest[i] == longest[i]:
        i += 1
    return shortest[:i]


def longest_common_prefix_v2(strings):
    """ This one uses zip() in a rather elegant way. Use zip() to look at respective characters in order.
    Time complexity: O(N)
    Space complexity: O(N)
    """
    prefix = ''
    zipped_chars = zip(*strings)
    for zipped in zipped_chars:
        if len(set(zipped)) > 1:  # If not all respective characters are the same
            return prefix
        prefix += zipped[0]  # If all characters are equal (equal to same character), append that character
    return prefix


class Test(unittest.TestCase):
    data = [(['flower', 'flow', 'flight'], 'fl'),
            (['dog', 'racecar', 'car'], '')
            ]

    def test_longest_common_prefix(self):
        for test_array, result in self.data:
            self.assertEqual(result, longest_common_prefix_v1(test_array))
            self.assertEqual(result, longest_common_prefix_v2(test_array))


if __name__ == '__main__':
    unittest.main()
