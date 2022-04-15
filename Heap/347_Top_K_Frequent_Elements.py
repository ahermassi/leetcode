""" Given a non-empty array of integers, return the k most frequent elements.
Your algorithm's time complexity must be better than O(n log n), where n is the array's size.
"""
from collections import defaultdict, Counter
from heapq import heappush, heappop
from random import randint

import unittest2 as unittest


def top_k_frequent_v1(nums, k):
    """ Build a frequency hash map. The next step is to build a min heap and maintain a size of k.
    Time complexity: The complexity of building the hash map is O(N). The time complexity of adding an element in a
    heap is O(logK) (binary tree of K elements) and we do it N times, that means O(N logK). Hence the overall
    complexity of the algorithm is O(N + N logK) = O(N logK).
    Space complexity: O(N), to store the hash map
    """
    counter, heap, res = Counter(nums), [], []
    for num, count in counter.items():
        heappush(heap, (count, num))
        if len(heap) > k:
            # Popping from the heap discards the smallest element. Done (N-k) times leaves us with
            # the k largest elements
            heappop(heap)
    return [val[1] for val in heap]


def top_k_frequent_v2(nums, k):
    """ Build a frequency hash map, 'counter'. Then build another hash map that maps frequencies to the elements that
        appear with that frequency, 'freq'. Now, in a reversed range [len(nums) + 1 .. 0], if any index in that range
        is in 'freq' map, append the corresponding elements to the final output list 'res'. Return when 'res' has
        already k elements.
        Note: we use a reversed range because we want the top k or most frequent k, so it makes sense to start with
        the max index.
    Time complexity: O(N)
    Space complexity: O(N) for the hash maps
    """
    n, res = len(nums), []
    counter = Counter(nums)
    freq = defaultdict(list)
    for num, count in counter.items():
        freq[count].append(num)
    for i in reversed(range(n+1)):
        for num in freq[i]:
            res.append(num)
            if len(res) == k:
                return res


def top_k_frequent_v3(nums, k):
    """ Same idea as previous solution but using bucket sort. In this version, 'bucket' array replaces 'frequencies'
        hash map.
    Time complexity: O(N)
    Space complexity: O(N)
    """
    n = len(nums)
    bucket = [[] for _ in range(n+1)]
    counter, res = Counter(nums), []
    for num, count in counter.items():
        bucket[count].append(num)
    for i in reversed(range(n+1)):  # Traverse the bucket right-to-left to get the largest counts first
        for num in bucket[i]:
            res.append(num)
            if len(res) == k:
                return res


def top_k_frequent_v4(nums, k):
    """ Quick Select. Similar to 215- Kth Largest Element in an Array and 973- K Closest Points to Origin.
        Build a hash map element -> its frequency and convert its keys into the array 'unique_nums' of unique elements.
        Note that elements are unique, but their frequencies are not. If by chance our pivot element took (N - k)th
        final position, then k elements on the right are these top k frequent we're looking for. If not, we can choose
        one more pivot and place it in its perfect position.
        Work with 'unique_nums' array. Use a partition scheme to place the pivot into its perfect position 'pivot_index'
        in the sorted array, move less frequent elements to the left of pivot, and more frequent or of the same
        frequency to the right.
        Compare 'pivot_index' and (N - k).
            - If pivot_index == N - k, the pivot is (N - k)th most frequent element, and all elements on the right are
              more frequent or of the same frequency. Return these top k frequent elements: unique_nums[N - k:]
            - Otherwise, choose the side of the array to proceed accordingly.
    Time complexity: O(N) in the average case, O(N^2) in the worst case. In the worst-case of constantly bad chosen
    pivots, the problem is not divided by half at each step, it becomes just one element less, that leads to O(N^2)
    time complexity. It happens, for example, if at each step we choose the pivot not randomly, but take the rightmost
    element. For the random pivot choice the probability of having such a worst-case is negligibly small.
    Space complexity: O(N)
    """

    def partition(left, right):
        pivot_index = randint(left, right)
        pivot = unique_nums[left]
        unique_nums[pivot_index], unique_nums[right] = unique_nums[right], unique_nums[pivot_index]
        i = j = left  # i will keep track of the 'tail' of the section of items less than the pivot so that
        # at the end we can 'sandwich' the pivot between the section less than it and the section equal to or greater
        # than it. j will scan for us. All the elements before i (excluding i) are less than the pivot
        while j < right:
            if counter[unique_nums[j]] < counter[pivot]:
                unique_nums[i], unique_nums[j] = unique_nums[j], unique_nums[i]
                i += 1
            j += 1
        unique_nums[i], unique_nums[right] = unique_nums[right], unique_nums[i]  # Bring the pivot back after the
        # section of items less than the pivot. i keeps the tail of this section
        return i  # Return the pivot's final resting position

    counter = Counter(nums)
    unique_nums = list(counter.keys())
    n = len(unique_nums)
    k = n - k  # kth top frequent element is (n - k)th less frequent.
    left, right = 0, len(unique_nums) - 1
    while True:
        pivot_index = partition(left, right)
        if pivot_index == k:
            return unique_nums[k:]
        if pivot_index < k:
            left = pivot_index + 1
        else:
            right = pivot_index - 1


class Test(unittest.TestCase):
    data = [([1, 1, 1, 2, 2, 3], 2, [1, 2]), ([1], 1, [1])]

    def test_top_k_frequent(self):
        for test_array, test_k, result in self.data:
            self.assertEqual(result, top_k_frequent_v1(test_array, test_k))
            self.assertEqual(result, top_k_frequent_v2(test_array, test_k))
            self.assertEqual(result, top_k_frequent_v3(test_array, test_k))


if __name__ == '__main__':
    unittest.main()
