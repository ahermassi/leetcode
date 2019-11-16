""" Given an input string, reverse the string word by word.
Input string may contain leading or trailing spaces. However, your reversed string should not contain leading or
trailing spaces.
You need to reduce multiple spaces between two words to a single space in the reversed string.
"""

import unittest2 as unittest


def reverse_words_v1(s):
    """ First reverse entire string, then iterate over reversed string and again reverse order of characters within a
        word. Append each 'word' to 'words'.
    Time complexity: O(N)
    Space complexity: O(N)
    """
    s = s[::-1]
    word, words = '', ''
    for i, c in enumerate(s):
        if not c.isspace():  # If it's a space, continue
            if not word:  # If current reversed 'word' we're building is empty
                word = c
            elif s[i-1].isspace():  # Character is not space, a current word exists, and previous character is space
                # --> We've hit a NEW word
                words += word + ' '  # Append the last reversed 'word' to 'words'
                word = c  # Start a new reversed 'word'
            else:
                word = c + word  # Building the reversed 'word'
    words += word  # Adding the last reversed 'word'. Don't forget !
    return words


def reverse_words_v2(s):
    """ Same idea but reversing the words of the reversed string itself.
    Time complexity: O(N)
    Space complexity: O(N)
    """
    s = list(' '.join(s.split()))[::-1]  # Get rid of spaces and transform the string to list as strings are immutable
    n, i = len(s), 0
    while i < n:
        left = i  # Left end of the word to reverse
        while i < n and s[i] != ' ':
            i += 1
        right = i - 1  # Right end of the word to reverse
        while left < right:  # The actual reversing
            s[left], s[right] = s[right], s[left]
            left += 1
            right -= 1
        while i < n and s[i] == ' ':  # Advance till the first non-space character
            i += 1
    return ''.join(s)


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