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
        empty string. So, for example, if the first (in the alphabetical order) string is 'aaa' and last string comes
        out to be 'baa', then there is no common prefix.
        The first string stands as a BASE LINE for the longest possible common prefix, while the last string acts as a
        verifier that all strings BEFORE the last have this common prefix. Otherwise, it wouldn't have been the last
        string in sorted order.
        For example, ['flood', 'flower', 'flowers']. The max is 'flowers', and the min is 'flood'. We can only compare
        them to get common prefix 'flo'.
        Another example, ['flood', 'flower', 'flowers', 'food']. The max is 'food', and the min is 'flood'. We can only
        compare them to get common prefix 'f'
        The reason is that the max string has the longest or shortest common prefix with words that are not min or max.
        So, we can get accurate results through comparing min and max.
    Time complexity: O(S), where S is the length of the shortest string in the array
    Space complexity: O(L), where L is the length of the longest string
    """
    if not strings:
        return ''
    first, last = min(strings), max(strings)  # These are the first and last in the alphabetical order, NOT length
    i, n = 0, len(first)
    while i < n and first[i] == last[i]:
        i += 1
    return first[:i]


def longest_common_prefix_v2(strings):
    """ Now we use the fact that the longest common prefix can only be as long as the shortest string in the list.
        For each character in the shortest string, we check if the other strings have the same character at the
        corresponding index. Return the string up to the valid index.
    Time complexity: O(S * L), where S is the length of the shortest string and L is the length of the longest string
    Space complexity: O(S), where S is the length of the shortest string in the array
    """
    if not strings:
        return ''
    shortest = min(strings, key=len)
    for i, c in enumerate(shortest):
        for other in strings:
            if other[i] != c:
                return shortest[:i]
    return shortest


def longest_common_prefix_v3(strings):
    """ This solution uses zip() in a rather elegant way. Use zip() to look at respective characters in order.
    Time complexity: O(S * N), where S is the length of the shortest string in the array and N is the number of strings
    Space complexity: O(L), where L is the length of the longest string
    """
    prefix = []
    for letters in zip(*strings):
        if len(set(letters)) > 1:  # If not all respective characters are the same
            break
        prefix.append(letters[0])  # If all characters are the same, append that character
    return ''.join(prefix)


class Test(unittest.TestCase):
    data = [(['flower', 'flow', 'flight'], 'fl'),
            (['dog', 'racecar', 'car'], '')
            ]

    def test_longest_common_prefix(self):
        for test_array, result in self.data:
            self.assertEqual(result, longest_common_prefix_v1(test_array))
            self.assertEqual(result, longest_common_prefix_v2(test_array))
            self.assertEqual(result, longest_common_prefix_v3(test_array))


if __name__ == '__main__':
    unittest.main()
