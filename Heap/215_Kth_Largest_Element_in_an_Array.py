""" Find the kth largest element in an unsorted array. Note that it is the kth largest element in the sorted order,
not the kth distinct element. """

from heapq import heappush, heappop
from random import randint
import unittest2 as unittest


def find_kth_largest_v1(nums, k):
    """ The naive solution would be to sort an array first and then return kth element from the end.
    Time complexity: O(N logN)
    Space complexity: O(N)
    """
    return sorted(nums)[-k]


def find_kth_largest_v2(nums, k):
    """ Build a min heap that stores the K largest values. The algorithm iterates over the whole input and maintains
        the size of the heap as k.
    Time complexity: O(N logK) for heap construction
    Space complexity: O(k) to store heap elements
    """
    heap = []
    for num in nums:
        heappush(heap, num)
        if len(heap) > k:
            heappop(heap)
    return heap[0]


def find_kth_largest_v3(nums, k):
    """ Quick select.
        This approach is basically the same as for quick sort. For simplicity, notice that kth largest element is
        the same as (N - k)th smallest element (when indexing is 0-based), hence we could implement kth smallest
        algorithm for this problem.
        First we choose a pivot, and define its position in a sorted array in a linear time. This could be done with
        the help of partition algorithm. As an output we have an array where pivot is on its perfect position in the
        ascending sorted array, all elements on the left of the pivot are smaller than pivot, and all elements on the
        right of the pivot are larger than or equal to pivot.
        If the pivot's rank is smaller than the rank we want to find, we are sure all elements before pivot actually
        have even smaller rank, we search the target at the part after pivot.
        If the pivot's rank is larger than the rank we want to find, we search the target at the left part before pivot.
        The idea is so powerful and beautiful.
    Time complexity: O(N)
    Space complexity: O(1)
    """

    def partition(left, right):
        """ This is the same partitioning routine of quicksort. """
        random_index = randint(left, right)  # Select a random pivot index between left and right, so that even when
        # the worst case input would be provided the algorithm wouldn't be affected
        pivot = nums[random_index]
        nums[right], nums[random_index] = nums[random_index], nums[right]
        i, j = left - 1, left  # i will keep track of the 'tail' of the section of items less than the pivot so that
        # at the end we can 'sandwich' the pivot between the section less than it and the section greater than it.
        # j will scan for us
        while j < right:
            if nums[j] <= pivot:  # If this item is less than the pivot, it needs to be moved to the section of items
                # less than the pivot
                i += 1  # Move i forward so that we can swap the value at j into the tail of the items less than the
                # pivot
                nums[i], nums[j] = nums[j], nums[i]  # Execute the swap
            j += 1
        i += 1
        nums[i], nums[right] = nums[right], nums[i]  # Swap the pivot value right after the section of items less
        # than the pivot. i keeps the tail of this section
        return i  # Return the pivot's final resting position

    n = len(nums)
    left, right = 0, n - 1
    k = n - k  # In reality, kth largest is same as (n-k+1)th smallest. Since indexing is 0-base, k is set to (n - k)
    while True:
        pivot = partition(left, right)
        if pivot == k:
            return nums[pivot]
        if pivot < k:
            left = pivot + 1
        else:
            right = pivot - 1


class Test(unittest.TestCase):
    data = [([3, 2, 1, 5, 6, 4], 2, 5), ([3, 2, 3, 1, 2, 4, 5, 5, 6], 4, 4)]

    def test_find_kth_largest(self):
        for test_array, test_k, result in self.data:
            self.assertEqual(result, find_kth_largest_v1(test_array, test_k))
            self.assertEqual(result, find_kth_largest_v2(test_array, test_k))
            self.assertEqual(result, find_kth_largest_v3(test_array, test_k))


if __name__ == '__main__':
    unittest.main()
