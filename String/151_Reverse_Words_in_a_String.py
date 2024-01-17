""" Given an input string, reverse the string word by word.
Input string may contain leading or trailing spaces. However, your reversed string should not contain leading or
trailing spaces.
You need to reduce multiple spaces between two words to a single space in the reversed string.
"""

import unittest2 as unittest


def reverse_words_v1(s):
    """ First reverse the entire string, then iterate over the reversed string and reverse each group of non-whitespace
         characters to form a word.

    Time complexity: O(N)
    Space complexity: O(N)
    """
    def reverse(left, right):
        while left < right:
            s[left], s[right] = s[right], s[left]
            left += 1
            right -= 1

    # Get rid of whitespaces and transform the string into a list of characters (strings are immutable).
    # This takes care of consecutive whitespaces.
    # Example: s = 'blue      sky  ' --> s = ['b', 'l', 'u', 'e', ' ', 's' 'k', 'y']
    s = list('  '.join(s.split()))
    n = len(s)
    reverse(0, n - 1) # Reverse the entire string (or list of characters)
    i = 0
    while i < n:
        j = i
        while j < n and s[j] != '  ':
            j += 1
        reverse(i, j - 1) # Reverse the word
        i = j + 1
    return ''.join(s)


def reverse_words_v2(s):
    """ In-place transformation. Same idea but reversing the words of the reversed string itself.
    Time complexity: O(N)
    Space complexity: O(N)
    """
    s = list(' '.join(s.split()))[::-1]
    n, right = len(s), 0
    while right < n:
        left = right  # Left end of the word to reverse
        while right < n and s[right] != ' ':
            right += 1
        r = right - 1  # Right end of the word to reverse
        while left < r:  # The actual reversing
            s[left], s[r] = s[r], s[left]
            left += 1
            r -= 1
        right += 1  # Advance to the beginning of next word
    return ''.join(s)


def reverse_words_v3(s):
    """ Reversing the individual words in the string without reversing the string itself.
        Read the original string backwards and construct the reversed words. Each reversed word is appended to 'res'
        list. Finally, join the reversed words together and return the final reversed string.
    Time complexity: O(N)
    Space complexity: O(N)
    """
    s = s.strip()
    i = len(s) - 1
    res, word = [], ''
    while i >= 0:
        while i >= 0 and not s[i].isspace():
            word = s[i] + word
            i -= 1
        res.append(word)
        word = ''
        while i >= 0 and s[i].isspace():
            i -= 1
    return ' '.join(res)


class Test(unittest.TestCase):
    data = [
        ('the sky is blue', 'blue is sky the'), ('  hello world!  ', 'world! hello'),
        ('a good   example', 'example good a')
    ]

    def test_reverse_words(self):
        for test_string, result in self.data:
            self.assertEqual(result, reverse_words_v1(test_string))
            # self.assertEqual(result, reverse_words_v2(test_string))


if __name__ == '__main__':
    unittest.main()