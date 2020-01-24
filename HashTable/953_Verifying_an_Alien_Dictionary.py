""" Given a sequence of words written in the alien language, and the order of the alphabet, return true if and only
if the given words are sorted lexicographically in this alien language. """

import unittest2 as unittest


def is_alien_sorted(words, order):
    """ The words are sorted lexicographically if and only if adjacent words are. This is because order is
        transitive: a <= b and b <= c implies a <= c.
    Time complexity: O(N), The outer loop runs for N times which is the length of the array. The inner loop is constant.
    Space complexity: O(1), no matter the size of the input string of words, the dictionary will always be a mapping
    of 26 characters to 26 numbers.
    """
    alphabet = {c: i for i, c in enumerate(order)}
    alphabet[''] = -1
    for i in range(len(words) - 1):
        word1 = words[i]
        word2 = words[i + 1]
        for j in range(max(len(word1), len(word2))):
            if word1[j:j+1] != word2[j:j+1]:
                if alphabet[word1[j:j+1]] > alphabet[word2[j:j+1]]:
                    return False
                break
    return True


class Test(unittest.TestCase):
    data = [(['hello', 'leetcode'], 'hlabcdefgijkmnopqrstuvwxyz', True),
            (['word', 'world', 'row'], 'worldabcefghijkmnpqstuvxyz', False),
            (['apple', 'app'], 'abcdefghijklmnopqrstuvwxyz', False)
            ]

    def test_is_alien_sorted1(self):
        for test_array, order, result in self.data:
            self.assertEqual(result, is_alien_sorted(test_array, order))


if __name__ == '__main__':
    unittest.main()
