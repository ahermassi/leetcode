""" Given a sequence of words written in the alien language, and the order of the alphabet, return true if and only
if the given words are sorted lexicographically in this alien language. """

import unittest2 as unittest


def is_alien_sorted_v1(words, order):
    """ The words are sorted lexicographically if and only if adjacent words are. This is because order is
        transitive: a <= b and b <= c implies a <= c.
    Time complexity: O(N * M), where N is the number of words and M is the length of longest word
    Space complexity: O(1), no matter the size of the input string of words, the dictionary will always be a mapping
    of 26 characters to 26 numbers.
    """
    alphabet = {c: i for i, c in enumerate(order)}
    alphabet[''] = -1
    n = len(words)
    for i in range(n - 1):
        word1, word2 = words[i], words[i + 1]
        for j in range(max(len(word1), len(word2))):  # Loop until the longest word is exhausted
            c1, c2 = word1[j:j+1], word2[j:j+1]  # Slicing on the shortest word after exhaustion returns ''
            if c1 != c2:
                if alphabet[c1] > alphabet[c2]:
                    return False
                break  # Ignore the rest of the words if order is correct at the first differing character
    return True


def is_alien_sorted_v2(words, order):
    """ A variation of the previous algorithm.
        Compare every two adjacent words.
        If any letter of former word is in higher order, return False.
        If current letter of former word is in lower order, forget the rest of word
        If length of former word is longer and latter word is substring of former, return False ('apple' & 'app' etc.)
    Time complexity: O(N * M)
    Space complexity: O(1)
    """

    def is_bigger(word1, word2):
        for i in range(min(len(word1), len(word2))):  # Key difference here: loop until the shortest word is exhausted
            c1, c2 = word1[i], word2[i]
            if c1 != c2:
                return alphabet[c1] > alphabet[c2]
        return len(word1) > len(word2)  # If we reach here, one of the words is substring of the other

    alphabet = {c: i for i, c in enumerate(order)}
    n = len(words)
    for i in range(n - 1):
        word1, word2 = words[i], words[i + 1]
        if is_bigger(word1, word2):
            return False
    return True


class Test(unittest.TestCase):
    data = [(['hello', 'leetcode'], 'hlabcdefgijkmnopqrstuvwxyz', True),
            (['word', 'world', 'row'], 'worldabcefghijkmnpqstuvxyz', False),
            (['apple', 'app'], 'abcdefghijklmnopqrstuvwxyz', False)
            ]

    def test_is_alien_sorted(self):
        for test_array, order, result in self.data:
            self.assertEqual(result, is_alien_sorted_v1(test_array, order))
            self.assertEqual(result, is_alien_sorted_v2(test_array, order))


if __name__ == '__main__':
    unittest.main()
