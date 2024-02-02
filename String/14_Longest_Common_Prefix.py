""" Write a function to find the longest common prefix string amongst an array of strings.
If there is no common prefix, return an empty string "". """

import unittest2 as unittest


def longest_common_prefix_v1(strings):
    """ This implementation is based on the idea that the longest common prefix is included in or equal to the first
         string in the alphabetical order of the list of strings.

         The first thing to realize is that the longest common prefix can only be as long as the shortest string with a
         common prefix in the array. So, when we sort, the shortest string with a common prefix will be the first string
         (assuming ascending order).

         Then, we have to understand that the longest common prefix must apply for ALL list elements. If there's a
         string that does not have the longest common prefix we've found so far, then there is no common prefix.
         For example, if the first string in the alphabetical order is 'aaa' and the last string is 'baa', then there is
         no common prefix.

         The first string stands as a BASELINE for the longest possible common prefix, while the last string acts as a
         verifier that all strings BEFORE the last one have this common prefix. Otherwise, it wouldn't have been the
         last string in sorted alphabetical order.

         The big brained concept here is this:

                    If the list is sorted alphabetically, then we can assume that the first string in the list and
                    the last string of the list will have most different prefixes of all comparisons that could
                    be made between all the other strings. The first and last strings are the elements that are
                    going to be the least similar.

        Say we sort an array of words. The first word starts with a 'b' and the last word also starts with a 'b'. What
        does that tell us about all the words in between them? They also all start with 'b'. We know this because the
        words are sorted in alphabetical order and the only way the first and last word can both start with the same
        letter AND have the array be in order is if all the words in between start with the same letter. Using this
        logic, if we sort the array of words we only ever have to look at the first and last one. We can ignore all the
        middle words entirely since we know if the prefix matches for the first and last, it matches for the middle ones
        as well.



        For example, ['flood', 'flower', 'flowers']. The min is 'flood' and the max is 'flowers'. We can compare just
        these two them to get the longest common prefix 'flo'.

    Time complexity: O(N logN + M), where N is the number of strings in the list and M is the length of the shortest
    string in the array
    Space complexity: O(N)
    """
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
