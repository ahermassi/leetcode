""" Design a class which receives a list of words in the constructor, and implements a method that takes two words
word1 and word2 and return the shortest distance between these two words in the list. Your method will be called
* repeatedly * many times with different parameters. """

from collections import defaultdict
import unittest2 as unittest


class WordDistance(object):
    """ A given word can occur multiple times in the original word list. The main idea for this approach is that if the
        list of these indices is in sorted order, we can find such a pair in linear time.
        The idea is to use a two pointer approach. Let's say we have a pointer i for the sorted list of indices of word1
        and j for the sorted list of indices of word2. At every iteration, we record the difference of indices i.e.
        abs(word1[i] - word2[j]). Once we've done that, we have two possible choices for progressing the two pointers:
        word1[i] < word2[j]: If this is the case, that means there is no point in moving the j pointer forward. So, if
        we move j forward, then the difference abs(word1[i] - word2[j + 1]) would be even greater than
        abs(word1[i] - word2[j]).
        So, if we have (word1[i] < word2[j]), we move the pointer 'i' one step forward i.e. (i + 1) in the hopes that
        abs(word1[i + 1] - word2[j]) would give us a lower distance than abs(word1[i] - word2[j]).
        Same logic if word1[i] > word2[j].
    Time complexity: the time complexity of the constructor of our class is O(N)O(N) considering there were NN words in
    the original list. We iterate over them and prepare a mapping from key to list of indices as described before.
    Then, for the function that finds the minimum distance between the two words, the complexity would be O(max(K, L))
    where K and L represent the number of occurrences of the two words. However, K = O(N) and also L = O(N). Therefore,
    the overall time complexity would also be O(N).
    Space complexity: O(N)
    """

    def __init__(self, words):
        """
        :type words: List[str]
        """
        self.words = words
        self.distances = {}
        self.indices = defaultdict(list)
        for i, word in enumerate(self.words):
            self.indices[word].append(i)

    def shortest(self, word1, word2):
        """
        :type word1: str
        :type word2: str
        :rtype: int
        """
        indices1, indices2 = self.indices[word1], self.indices[word2]
        i, j, n, m = 0, 0, len(indices1), len(indices2)
        shortest_distance = float('inf')
        while i < n and j < m:
            shortest_distance = min(shortest_distance, abs(indices1[i] - indices2[j]))
            if indices1[i] < indices2[j]:
                i += 1
            else:
                j += 1
        return shortest_distance


class Test(unittest.TestCase):
    word_distance = WordDistance(["practice", "makes", "perfect", "coding", "makes"])
    words = [('coding', 'practice'), ('makes', 'coding')]
    result = [3, 1]

    def test_has_cycle(self):
        for test_words, result in zip(self.words, self.result):
            self.assertEqual(result, self.word_distance.shortest(test_words[0], test_words[1]))


if __name__ == '__main__':
    unittest.main()
