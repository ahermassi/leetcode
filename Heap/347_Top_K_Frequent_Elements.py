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


def top_k_frequent_v2(nums, k):
    """ Build a frequency hash map, 'counter'. Then build another hash map that maps frequencies to the elements that
        appear with that frequency, 'freq'. Now, in a reversed range [len(nums) + 1 .. 0], if any index in that range
        is in 'frequency' map, append the corresponding elements in final output list 'res'. Return when 'res' has
        already k elements.
        Note: we use a reversed range because we want the top k or most frequent k, so it makes sense to start with
        the max index.
    Time complexity: O(N)
    Space complexity: O(N) for the hash maps
    """
    counter, freq, res = defaultdict(int), defaultdict(list), []
    for num in nums:
        counter[num] += 1
    for key, v in counter.items():
        freq[v].append(key)
    for i in reversed(range(len(nums) + 1)):
        if i in freq:
            res.extend(freq[i])
            if len(res) >= k:
                return res[:k]


class Test(unittest.TestCase):
    data = [([1, 1, 1, 2, 2, 3], 2, [1, 2]), ([1], 1, [1])]

    def test_top_k_frequent(self):
        for test_array, test_k, result in self.data:
            self.assertEqual(result, top_k_frequent_v1(test_array, test_k))
            self.assertEqual(result, top_k_frequent_v2(test_array, test_k))


if __name__ == '__main__':
    unittest.main()
