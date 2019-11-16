""" Given a list of words and two words word1 and word2, return the shortest distance between these two words in the
list. """

import unittest2 as unittest


def shortest_distance_v1(words, word1, word2):
    """ Keep two indices index1 and index2 where we store the most recent locations of word1 and word2. Each time we
        find a new occurrence of one of the words, we do not need to search the entire array for the other word,
        since we already have the index of its most recent occurrence.
    Time complexity: O(N) where N is the length of words list
    Space complexity: O(1)
    """
    index1 = index2 = -1
    min_distance = len(words)
    for i, w in enumerate(words):
        if w == word1:
            index1 = i
        elif w == word2:
            index2 = i
        if index1 != -1 and index2 != -1:
            min_distance = min(min_distance, abs(index1 - index2))
    return min_distance


def shortest_distance_v2(words, word1, word2):
    """ Create two lists storing indices of each occurrence of the word1 and word2 accordingly. After that, find the
        minimum difference between two elements from these two lists.
        Notice that finding the minimum distance between the two lists is done in linear time O(n+m) instead of
        quadratic O(n^2) since the two lists are sorted (increasing indices)
    Time complexity: O(N)
    Space complexity: O(N)
    """
    indices1, indices2 = [], []
    for i, w in enumerate(words):
        if w == word1:
            indices1.append(i)
        elif w == word2:
            indices2.append(i)
    n, m, res = len(indices1), len(indices2), float('inf')
    i = j = 0
    while i < n and j < m:
        res = min(res, abs(indices1[i] - indices2[j]))
        if indices1[i] < indices2[j]:  # Advance the smallest in hopes of making the gap smaller
            i += 1
        else:
            j += 1
    return res


class Test(unittest.TestCase):
    data = [(['practice', 'makes', 'perfect', 'coding', 'makes'], 'coding', 'practice', 3),
            (['practice', 'makes', 'perfect', 'coding', 'makes'], 'makes', 'coding', 1)
            ]

    def test_shortest_distance(self):
        for test_words, test_word1, test_word2, result in self.data:
            self.assertEqual(result, shortest_distance_v1(test_words, test_word1, test_word2))
            self.assertEqual(result, shortest_distance_v2(test_words, test_word1, test_word2))


if __name__ == '__main__':
    unittest.main()

