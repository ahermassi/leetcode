""" Given a non-empty array of integers, return the k most frequent elements.
Your algorithm's time complexity must be better than O(n log n), where n is the array's size.
"""
from collections import defaultdict, Counter
from heapq import heappush, heappop
from random import randint

import unittest2 as unittest


def top_k_frequent_v1(nums, k):
    """ Build a frequency hash map. The next step is to build a min heap and maintain its size at k.

    Time complexity: O(N logK), the complexity of building the hash map is O(N); the time complexity of pushing an
    element into a heap is O(logK) (binary tree of K elements) and we do it N times, that means O(N logK). Hence, the
    overall complexity of the algorithm is O(N + N logK) = O(N logK)
    Space complexity: O(N), to store the hash map and heap
    """
    counter = defaultdict(int)
    for num in nums:
        counter[num] += 1
    heap = []
    for num, count in counter.items():
        heappush(heap, (count, num))
        if len(heap) > k:
            # Popping from the heap discards the smallest element. Doing so (N-k) times leaves us with
            # the k largest elements
            heappop(heap)
    return [val[1] for val in heap]


def top_k_frequent_v2(nums, k):
    """ Build a frequency hash map, 'counter'. Then build another hash map that maps frequencies to the elements that
         appear with that frequency, 'freq'.

         Then, in a reversed range [len(nums) + 1 .. 0], if any index in that range is in 'freq' map, append the
         corresponding elements to the final output list. Return when the list has already k elements.

        Note: we use a reversed range because we want the top k or most frequent k, so it makes sense to start with
        the max frequency.

    Time complexity: O(N)
    Space complexity: O(N), for the hash maps
    """
    n, topk = len(nums), []
    counter = defaultdict(int)
    for num in nums:
        counter[num] += 1
    freq = defaultdict(list)
    for num, count in counter.items():
        freq[count].append(num)
    for i in reversed(range(n+1)):
        for num in freq[i]:
            topk.append(num)
            if len(topk) == k:
                return topk


# Video explanation: https://youtu.be/YPTqKIgVk-k
def top_k_frequent_v3(nums, k):
    """ Same idea as previous solution but using bucket sort, where 'bucket' array replaces 'frequencies' hash map.
         Note that we don't need to loop starting at (n + 1). We could instead start at max(counter.values()) + 1.

    Time complexity: O(N), as we traverse through the bucket array, we aren't doing an operation N times at each
    iteration; we are doing N total operations throughout the entire array. So even though the for loops are nested, we
    are processing at most N elements, each only once.
    Space complexity: O(N)
    """
    n, topk = len(nums), []
    counter = defaultdict(int)
    for num in nums:
        counter[num] += 1
    bucket = [[] for _ in range(n+1)]
    for num, count in counter.items():
        bucket[count].append(num)
    # max_count = max(counter.values())
    # for i in reversed(range(max_count + 1)):
    for i in reversed(range(n+1)):  # Traverse the bucket right-to-left to get the largest counts first
        for num in bucket[i]:
            topk.append(num)
            if len(topk) == k:
                return topk


def top_k_frequent_v4(nums, k):
    """ Quick Select. Similar to 215- Kth Largest Element in an Array and 973- K Closest Points to Origin.

        Quickselect is a textbook algorithm typically used to solve the problems "find kth something": kth smallest,
        kth largest, kth most frequent, kth less frequent, etc. Like quicksort, quickselect was developed by Tony Hoare
        and is also known as Hoare's selection algorithm.

        The approach is the same as for quicksort:

                    Choose a pivot and define its position in a sorted array in a linear time using the so-called
                                                            partition algorithm


        Build a hash map element -> its frequency and convert its keys into the array 'unique_nums' of unique elements.
        Note that elements are unique, but their frequencies are not. If by chance our pivot element took (N - k)th
        final position, then k elements on the right are these top k frequent we're looking for. If not, we can choose
        one more pivot and place it in its perfect position.

        Work with 'unique_nums' array. Use a partition scheme to place the pivot into its perfect position 'pivot_index'
        in the sorted array. As an output, we have an array where the pivot is on its perfect position in the ascending
        sorted array, sorted by the frequency. All elements on the left of the pivot are less frequent than the pivot,
        and all elements on the right are more frequent or have the same frequency.

        Hence, the array is now split into two parts. If by chance our pivot element took (N - k)th final position, then
        k elements on the right are these top k frequent we're looking for. If not, we can choose one more pivot and
        place it in its perfect position.

        There are different partition algorithms. The most simple one is Lomuto's Partition Scheme, and so is what
        we will use. Here is how it works:

            - Move pivot at the end of the array using swap.
            - Set the store pointer i and scan pointer j at the beginning of the array: i = j = left.
            - Iterate over the array and move all less frequent elements to the left: swap(i, j).
            - Move i one step to the right after each swap.
            - Once the entire array scanned, move the pivot to its original place and return this index.

        Compare 'pivot_index' and (N - k):
            - If pivot_index == N - k, the pivot is (N - k)th most frequent element, and all elements on the right are
              more frequent or of the same frequency. Return these top k frequent elements: unique_nums[N - k:]
            - Otherwise, choose the side of the array to proceed accordingly.

    Time complexity: O(N) in the average case, O(N^2) in the worst case. In the worst-case of constantly bad chosen
    pivots, the problem is not divided by half at each step, it becomes just one element less, which leads to O(N^2)
    time complexity. It happens, for example, if at each step we choose the pivot not randomly, but take the rightmost
    element. For the random pivot choice the probability of having this worst-case is negligibly small.
    Space complexity: O(N)
    """

    def partition(left, right):
        pivot_index = randint(left, right)
        pivot = unique_nums[pivot_index]
        unique_nums[pivot_index], unique_nums[right] = unique_nums[right], unique_nums[pivot_index]
        i = j = left
        # i will keep track of the 'tail' of the section of items less than the pivot so that at the end we can
        # 'sandwich' the pivot between the section less than it and the section equal to or greater than it.
        # j will  scan for us. All the elements before i (excluding i) are less than the pivot.
        while j < right:
            if counter[unique_nums[j]] < counter[pivot]:
                unique_nums[i], unique_nums[j] = unique_nums[j], unique_nums[i]
                i += 1
            j += 1
        # Bring the pivot back after the section of items less than the pivot. i keeps the tail of this section
        unique_nums[i], unique_nums[right] = unique_nums[right], unique_nums[i]
        return i  # Return the pivot's final resting position

    counter = Counter(nums)
    unique_nums = list(counter.keys())
    n = len(unique_nums)
    # kth largest element in an array of n elements is (n - k + 1)th smallest (think 1st largest is nth smallest).
    # Similarly, kth most frequent element is (n - k + 1)th less frequent.
    # Since indexing is 0-based, kth most frequent is at index (n - k) in the frequency-sorted array.
    k = n - k
    left, right = 0, n - 1
    while True:
        index = partition(left, right)
        if index == k:
            return unique_nums[k:]
        if index < k:
            left = index + 1
        else:
            right = index - 1


class Test(unittest.TestCase):
    data = [([1, 1, 1, 2, 2, 3], 2, [1, 2]), ([1], 1, [1])]

    def test_top_k_frequent(self):
        for test_array, test_k, result in self.data:
            # self.assertEqual(result, top_k_frequent_v1(test_array, test_k))
            # self.assertEqual(result, top_k_frequent_v2(test_array, test_k))
            # self.assertEqual(result, top_k_frequent_v3(test_array, test_k))
            self.assertEqual(result, top_k_frequent_v4(test_array, test_k))


if __name__ == '__main__':
    unittest.main()
