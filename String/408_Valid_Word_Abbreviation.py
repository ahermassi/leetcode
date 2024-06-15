""" A string can be abbreviated by replacing any number of non-adjacent, non-empty substrings with their lengths. The
lengths should not have leading zeros.

For example, a string such as "substitution" could be abbreviated as (but not limited to):

"s10n" ("s ubstitutio n")
"sub4u4" ("sub stit u tion")
"12" ("substitution")
"su3i1u2on" ("su bst i t u ti on")
"substitution" (no substrings replaced)

The following are not valid abbreviations:

"s55n" ("s ubsti tutio n", the replaced substrings are adjacent)
"s010n" (has leading zeros)
"s0ubstitution" (replaces an empty substring)

Given a string word and an abbreviation abbr, return whether the string matches the given abbreviation.

A substring is a contiguous non-empty sequence of characters within a string. """

import unittest2 as unittest


def valid_word_abbreviation(word, abbr):
    """ We maintain two pointers, i pointing at the abbreviation and j pointing at the word.
         There are only two scenarios:

         - i points to a letter. We compare the values i and j point to. If equal, we increment them. Otherwise,
            return False.

         - i points to a digit. We need to find out the complete number that i is pointing to, e.g. 12. Then we would
            increment j by 12. We know that next we will either break out of the while loop if i or j is too large, or
            return to scenario 1.

    Time complexity: O(max(N, M), where N is the length of the abbreviation and M is the length of the word.
    Space complexity: O(1)
    """
    n, m = len(abbr), len(word)
    i = j = 0
    while i < n and j < m:
        if abbr[i].isalpha():
            if abbr[i] != word[j]:
                return False
            i += 1
            j += 1
        else:
            if abbr[i] == '0':
                # Handle edge cases such as "01", which are invalid
                return False
            k, length = i, 0
            while k < n and abbr[k].isdigit():
                length = length * 10 + ord(abbr[k]) - ord('0')
                k += 1
            i = k
            j += length
    return i == n and j == m


class Test(unittest.TestCase):
    data = [('internationalization', 'i12iz4n', True), ('apple', 'a2e', False)]

    def test_valid_word_abbreviation(self):
        for word, abbr, result in self.data:
            self.assertEqual(result, valid_word_abbreviation(word, abbr))


if __name__ == '__main__':
    unittest.main()