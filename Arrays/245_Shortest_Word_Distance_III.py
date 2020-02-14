""" Given a list of words and two words word1 and word2, return the shortest distance between these two words in the
list.
word1 and word2 may be the same and they represent two individual words in the list. """

import unittest2 as unittest


def shortest_word_distance_v1(words, word1, word2):
    """ Self-explanatory.
    Time complexity: O(N)
    Space complexity: O(1)
    """
    last_seen, res = -1, float('inf')
    i1 = i2 = -1
    for i, word in enumerate(words):
        if word == word1 == word2:
            if last_seen != -1:
                res = min(res, i - last_seen)
            last_seen = i
        else:
            if word == word1:
                i1 = i
            elif word == word2:
                i2 = i
            if i1 != -1 and i2 != -1:
                res = min(res, abs(i1 - i2))
    return res


def shortest_word_distance_v2(words, word1, word2):
    """ Self-explanatory.
    Time complexity: O(N)
    Space complexity: O(1)
    """
    index1 = index2 = -1
    res, same = float('inf'), word1 == word2
    for i, word in enumerate(words):
        if word == word1:
            if same:
                index2 = index1
            index1 = i
        elif word == word2:
            index2 = i
        if index1 != -1 and index2 != -1:
            res = min(res, abs(index1 - index2))
    return res


class Test(unittest.TestCase):
    data = [(['practice', 'makes', 'perfect', 'coding', 'makes'], 'makes', 'coding', 1),
            (['practice', 'makes', 'perfect', 'coding', 'makes'], 'makes', 'makes', 3)
            ]

    def test_shortest_word_distance(self):
        for test_words, test_word1, test_word2, result in self.data:
            self.assertEqual(result, shortest_word_distance_v1(test_words, test_word1, test_word2))
            self.assertEqual(result, shortest_word_distance_v2(test_words, test_word1, test_word2))


if __name__ == '__main__':
    unittest.main()