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
    """ In-place transformation. Same idea but reversing the words of the reversed string itself.
    Time complexity: O(N)
    Space complexity: O(N)
    """
    s = list(' '.join(s.split()))[::-1]  # Get rid of spaces and transform the string to list as strings are immutable
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
        while right < n and s[right] == ' ':  # Advance till the first non-space character
            right += 1
    return ''.join(s)


def reverse_words_v3(s):
    """ Reversing the individual words in the string without reversing the string itself.
        Read the original string backwards and construct the reversed words. Each reversed word is appended ot 'res'
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
            self.assertEqual(result, reverse_words_v2(test_string))


if __name__ == '__main__':
    unittest.main()