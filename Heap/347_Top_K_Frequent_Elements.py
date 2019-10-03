""" Given a non-empty array of integers, return the k most frequent elements.
Your algorithm's time complexity must be better than O(n log n), where n is the array's size.
"""
from collections import defaultdict
from heapq import nlargest
import unittest2 as unittest


def top_k_frequent_v1(nums, k):
    """ Build a frequency hash map. The next step is to build a heap.
    Time complexity: The complexity of building the hash map is O(N). The time complexity of adding an element in a
    heap is O(log(k)) (binary tree of k elements) and we do it N times, that means O(N log(k))). Hence the overall
    complexity of the algorithm is O(N + N log(k)) = O(N log(k)).
    Space complexity: O(N) to store the hash map
    """
    d, res = defaultdict(int), []
    for num in nums:
        d[num] += 1
    return nlargest(k, d.keys(), d.get)


class Test(unittest.TestCase):
    data = [([1, 1, 1, 2, 2, 3], 2, [1, 2]), ([1], 1, [1])]

    def test_top_k_frequent(self):
        for test_array, test_k, result in self.data:
            self.assertEqual(result, top_k_frequent_v1(test_array, test_k))


if __name__ == '__main__':
    unittest.main()
