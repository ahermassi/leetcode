""" Given a non-empty array of integers, return the k most frequent elements.
Your algorithm's time complexity must be better than O(n log n), where n is the array's size.
"""
from collections import defaultdict, Counter
from heapq import heappush, heappop
import unittest2 as unittest


def top_k_frequent_v1(nums, k):
    """ Build a frequency hash map. The next step is to build a heap and maintain a size of k.
    Time complexity: The complexity of building the hash map is O(N). The time complexity of adding an element in a
    heap is O(logK) (binary tree of k elements) and we do it N times, that means O(N logK). Hence the overall
    complexity of the algorithm is O(N + N logK) = O(N logK).
    Space complexity: O(N) to store the hash map
    """
    counter = Counter(nums)
    heap, res = [], []
    for key, value in counter.items():
        heappush(heap, (value, key))
        if len(heap) > k:
            heappop(heap)
    while heap:
        res.append(heappop(heap)[1])
    return res


def top_k_frequent_v2(nums, k):
    """ Build a frequency hash map, 'counter'. Then build another hash map that maps frequencies to the elements that
        appear with that frequency, 'freq'. Now, in a reversed range [len(nums) + 1 .. 0], if any index in that range
        is in 'freq' map, append the corresponding elements in final output list 'res'. Return when 'res' has
        already k elements.
        Note: we use a reversed range because we want the top k or most frequent k, so it makes sense to start with
        the max index.
    Time complexity: O(N)
    Space complexity: O(N) for the hash maps
    """
    n, counter, freq, res = len(nums), defaultdict(int), defaultdict(list), []
    for num in nums:
        counter[num] += 1
    for key, v in counter.items():
        freq[v].append(key)
    for i in reversed(range(n+1)):
        if i in freq:
            res.extend(freq[i])
            if len(res) >= k:
                return res[:k]


def top_k_frequent_v3(nums, k):
    """ Same idea as previous solution but using bucket sort. In this version, 'bucket' array replaces 'frequencies'
        hash map.
    Time complexity: O(N)
    Space complexity: O(N) for 'counter' hash map
    """
    n = len(nums)
    bucket = [[] for _ in range(n+1)]
    counter, res = defaultdict(int), []
    for num in nums:
        counter[num] += 1
    for key, value in counter.items():
        bucket[value].append(key)
    for i in reversed(range(n+1)):  # Traverse the bucket right-to-left to get the greatest counts first
        if bucket[i]:
            res.extend(bucket[i])
            if len(res) >= k:
                return res[:k]


class Test(unittest.TestCase):
    data = [([1, 1, 1, 2, 2, 3], 2, [1, 2]), ([1], 1, [1])]

    def test_top_k_frequent(self):
        for test_array, test_k, result in self.data:
            self.assertEqual(result, top_k_frequent_v1(test_array, test_k))
            self.assertEqual(result, top_k_frequent_v2(test_array, test_k))
            self.assertEqual(result, top_k_frequent_v3(test_array, test_k))


if __name__ == '__main__':
    unittest.main()
