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
        if c != ' ':  # If it's a space, continue
            if not word:  # If current reversed 'word' we're building ia empty
                word = c
            elif word and s[i - 1] and s[i - 1] == ' ':  # If a previous reversed 'word' exists and we hit a new word
                # (because the previous character is space)
                words += word + ' '  # Append the last reversed 'word' to 'words'
                word = c  # Start a new reversed 'word'
            else:
                word = c + word  # Building the reversed 'word'
    words += word  # Adding the last reversed 'word'. Don't forget !
    return words


class Test(unittest.TestCase):
    data = [
        ('the sky is blue', 'blue is sky the'), ('  hello world!  ', 'world! hello'),
        ('a good   example', 'example good a')
    ]

    def test_reverse_words(self):
        for test_string, result in self.data:
            self.assertEqual(result, reverse_words_v1(test_string))


if __name__ == '__main__':
    unittest.main()