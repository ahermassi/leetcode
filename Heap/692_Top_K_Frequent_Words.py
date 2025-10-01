""" Given a non-empty list of words, return the k most frequent elements.
Your answer should be sorted by frequency from highest to lowest. If two words have the same frequency, then the word
with the lower alphabetical order comes first. """

from collections import Counter
from heapq import heappush, heappop
import unittest2 as unittest


class HeapElement:
    def __init__(self, count, word):
        self.count = count
        self.word = word

    def __lt__(self, other):
        if self.count == other.count:
            return self.word > other.word
            # Pay attention to this ! Because the result will be reversed, we reverse the __lt__ logic here.
            # Example: heap = [(3, 'x'), (4, 'a')], and we want to push (4, 'b').
            # If we allow the default lexicographical order, the heap will be: [(3, 'x'), (4, 'a'), (4, 'b')].
            # After we pop the elements and reverse the result: res = ['b', 'a', 'x'], which is NOT the desired output.
            # For this reason, we reverse the lexicographical order of elements with the same count.
            # --> heap = [(3, 'x'), (4, 'b'), (4, 'a')], in which we considered (4, 'b') 'less' than (4, 'a')
            # --> res = ['a', 'b', 'x']
        return self.count < other.count

    def __eq__(self, other):
        return self.count == other.count and self.word == other.word


def top_k_frequent_v1(words, k):
    """ Count the frequency of each word, then add it to a min heap that stores the best k candidates. Each time a new
        word is added, the front element of heap (min frequency) is popped. We end up with a heap containing the k
        most frequent words.

    Time complexity: O(N + N logK) = O(N logK); O(N) to build frequency map, and O(N logK) to build the heap of size k
    Space complexity: O(N)
    """
    heap, res = [], []
    counter = Counter(words)
    for word, count in counter.items():
        heappush(heap, HeapElement(count, word))
        if len(heap) > k:
            heappop(heap)
    while heap:
        # return [e.word for e in heap] is WRONG. Successive heappop() is what gives correct results because heap
        # structure (array) is such that heap[k] <= heap[2k] and heap[k] <= heap[2k+1], not that the heap stores the
        # elements in sorted order. The only exception is heap[0] which ALWAYS contains the min value.
        res.append(heappop(heap).word)
    # Because we want the words sorted by frequency from highest to lowest, we reverse the result because the heap is
    # a min heap
    return res[::-1]


def top_k_frequent_v2(words, k):
    """ If we put all numbers into a max heap, the top element of the heap must be the max value of all numbers in the
        heap. So instead of sorting all unique words, we only need to pop the word with the max frequency from the max
        heap k times.

    Time complexity: O(k logN), we pop k elements from a heap of size N
    Space complexity: O(N)
    """
    heap, res = [], []
    counter = Counter(words)
    for key, value in counter.items():
        heappush(heap, (-value, key))
    for _ in range(k):
        res.append(heappop(heap)[1])
    return res


def top_k_frequent_v3(words, k):
    """ The good old bucket sort.
    Time complexity: O(K logK)
    Space complexity: O(N)
    """
    n = len(words)
    bucket, res = [[] for _ in range(n + 1)], []
    counter = Counter(words)
    for key, v in counter.items():
        bucket[v].append(key)
    for i in reversed(range(n + 1)):
        if bucket[i]:
            res.extend(sorted(bucket[i]))  # Sort the elements alphabetically
        if len(res) >= k:
            return res[:k]


class Test(unittest.TestCase):
    data = [(['i', 'love', 'leetcode', 'i', 'love', 'coding'], 2, ['i', 'love']),
            (['the', 'day', 'is', 'sunny', 'the', 'the', 'the', 'sunny', 'is', 'is'], 4, ['the', 'is', 'sunny', 'day'])]

    def test_top_k_frequent(self):
        for test_words, test_k, result in self.data:
            self.assertEqual(result, top_k_frequent_v1(test_words, test_k))
            self.assertEqual(result, top_k_frequent_v2(test_words, test_k))
            self.assertEqual(result, top_k_frequent_v3(test_words, test_k))


if __name__ == '__main__':
    unittest.main()