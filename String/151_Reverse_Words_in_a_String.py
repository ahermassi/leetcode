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
    """ The same algorithm but removes leading, trailing, and consecutive whitespaces without the use of split().

    Time complexity: O(N)
    Space complexity: O(N)
    """

    def trimSpaces():
        left, right = 0, len(s) - 1
        # Remove leading spaces
        while left <= right and s[left] == '  ':
            left += 1
            # Remove trailing spaces
        while left <= right and s[right] == '  ':
            right -= 1
        chars = []
        while left <= right:
            if s[left] != '  ':
                chars.append(s[left])
            # Reduce multiple spaces to a single one
            elif chars[-1] != '  ':
                chars.append(s[left])
            left += 1
        return chars

    def reverse(left, right):
        while left < right:
            s[left], s[right] = s[right], s[left]
            left += 1
            right -= 1

    s = trimSpaces()
    n = len(s)
    reverse(0, n - 1)
    i = 0
    while i < n:
        j = i
        while j < n and s[j] != '  ':
            j += 1
        reverse(i, j - 1)
        i = j + 1
    return ''.join(s)


def reverse_words_v3(s):
    """ Reverse the individual words in the string without reversing the string itself.

        Process the string backwards and extract the words. Each word is appended to the output. Finally, join the
        words together and return the final reversed string.

    Time complexity: O(N)
    Space complexity: O(N)
    """
    s = s.strip()
    words = []
    i = len(s) - 1
    while i >= 0:
        j = i
        while j >= 0 and s[j] != '  ':
            j -= 1
        words.append(s[j + 1:i + 1])
        while j >= 0 and s[j] == '  ':
            j -= 1
        i = j
    return ' '.join(words)


class Test(unittest.TestCase):
    data = [
        ('the sky is blue', 'blue is sky the'), ('  hello world!  ', 'world! hello'),
        ('a good   example', 'example good a')
    ]

    def test_reverse_words(self):
        for test_string, result in self.data:
            self.assertEqual(result, reverse_words_v1(test_string))
            self.assertEqual(result, reverse_words_v2(test_string))


if __name__ == '__main__':
    unittest.main()