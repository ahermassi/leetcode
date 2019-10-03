""" Find the kth largest element in an unsorted array. Note that it is the kth largest element in the sorted order,
not the kth distinct element. """

from heapq import heappush, heappop, nlargest
from random import randint

import unittest2 as unittest


def find_kth_largest_v1(nums, k):
    """ The naive solution would be to sort an array first and then return kth element from the end.
    Time complexity: O(N logN)
    Space complexity: O(N)
    """
    return sorted(nums)[-k]


def find_kth_largest_v2(nums, k):
    """ Build a min heap from nums. Since kth largest element == (n - k + 1)th smallest element, pop (n - k) elements
        from the heap to get to the kth largest element.
    Time complexity: O(N) for constructing the heap, O((N- k)logN) for popping (N - k) elements, so O(N + (N - k)logN)
    Space complexity: O(N) to store heap elements
    """
    heap = []
    for num in nums:
        heappush(heap, num)
    for _ in range(len(nums) - k):
        heappop(heap)
    return heappop(heap)


def find_kth_largest_v3(nums, k):
    """ Using the built-in nlargest.
    Time complexity: The time complexity of adding an element in a heap is O(log(k)) (binary tree of k elements) and
    we do it N times, that means O(N log(k))). Hence the overall complexity of the algorithm is O(N log(k))
    Space complexity: O(k) to store the heap elements
    """
    return nlargest(k, nums)[-1]


def find_kth_largest_v4(nums, k):
    """ This approach is basically the same as for quick sort. For simplicity let's notice that kth largest element is
        the same as N - kth smallest element, hence we could implement kth smallest algorithm for this problem.
        First we choose a pivot, and define its position in a sorted array in a linear time. This could be done with
        the help of partition algorithm. As an output we have an array where pivot is on its perfect position in the
        ascending sorted array, all elements on the left of the pivot are smaller than pivot, and all elements on the
        right of the pivot are larger or equal to pivot.
        Compare pos and N - k to choose the side of array to proceed recursively
    Time complexity: O(N)
    Space complexity: O(1)
    """

    def partition(left, right):
        ri = randint(left, right)
        nums[right], nums[ri] = nums[ri], nums[right]
        for i, v in enumerate(nums[left: right + 1], left):
            if v >= nums[right]:
                nums[left], nums[i] = nums[i], nums[left]
                left += 1
        return left - 1

    left, right, k = 0, len(nums) - 1, k - 1
    while True:
        pivot = partition(left, right)
        if pivot < k:
            left = pivot + 1
        elif pivot > k:
            right = pivot - 1
        else:
            return nums[pivot]


class Test(unittest.TestCase):
    data = [([3, 2, 1, 5, 6, 4], 2, 5), ([3, 2, 3, 1, 2, 4, 5, 5, 6], 4, 4)]

    def test_top_k_frequent(self):
        for test_array, test_k, result in self.data:
            self.assertEqual(result, find_kth_largest_v1(test_array, test_k))
            self.assertEqual(result, find_kth_largest_v2(test_array, test_k))
            self.assertEqual(result, find_kth_largest_v3(test_array, test_k))
            self.assertEqual(result, find_kth_largest_v4(test_array, test_k))


if __name__ == '__main__':
    unittest.main()
