""" Given a non-empty list of words, return the k most frequent elements.
Your answer should be sorted by frequency from highest to lowest. If two words have the same frequency, then the word
with the lower alphabetical order comes first. """

from collections import Counter
from heapq import heappush, heappop
import unittest2 as unittest


class Element:
    def __init__(self, count, word):
        self.count = count
        self.word = word

    def __lt__(self, other):
        if self.count == other.count:
            return self.word > other.word  # Pay attention to this ! Because the result will be reversed, we reverse
            # the __lt__ logic here
        return self.count < other.count

    def __eq__(self, other):
        return self.count == other.count and self.word == other.word


def top_k_frequent_v1(words, k):
    """ Count the frequency of each word, then add it to heap that stores the best k candidates. Each time a new word
        is encountered, the front element of heap (min frequency) is popped. We end up with a heap containing the k
        most frequent words.
    Time complexity: O(N + N logk) = O(N logk); O(N) to build frequency map, and O(N logk) to build the heap of size k
    Space complexity: O(N)
    """
    heap, res = [], []
    counter = Counter(words)
    for key, value in counter.items():
        heappush(heap, Element(value, key))
        if len(heap) > k:
            heappop(heap)
    for _ in range(k):  # return [e.word for e in heap] is WRONG. Successive heappop() is what gives correct results
        # because heap structure (array) is such that heap[k] <= heap[2k] and heap[k] <= heap[2k+1], not that the heap
        # stores its elements in sorted order. The only exception is heap[0] which ALWAYS contains the min value.
        res.append(heappop(heap).word)
    return res[::-1]  # Because we want the words sorted by frequency from highest to lowest, we reverse the result
    # as the heap is a min heap


def top_k_frequent_v2(words, k):
    """ Count the frequency of each word, and sort the words with a custom ordering relation that uses these
    frequencies. Then take the best k of them.
    Time complexity: O(N logN), where N is the length of words. We count the frequency of each word in O(N) time, then
    we sort the given words in O(N logN) time
    Space complexity: O(N)
    """
    counter = Counter(words)
    keys = counter.keys()
    keys = sorted(keys, key=lambda word: (-counter[word], word))
    return keys[:k]


class Test(unittest.TestCase):
    data = [(['i', 'love', 'leetcode', 'i', 'love', 'coding'], 2, ['i', 'love']),
            (['the', 'day', 'is', 'sunny', 'the', 'the', 'the', 'sunny', 'is', 'is'], 4, ['the', 'is', 'sunny', 'day'])]

    def test_remove_stones(self):
        for test_words, test_k, result in self.data:
            self.assertEqual(result, top_k_frequent_v1(test_words, test_k))
            self.assertEqual(result, top_k_frequent_v2(test_words, test_k))


if __name__ == '__main__':
    unittest.main()