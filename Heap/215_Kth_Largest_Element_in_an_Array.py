""" Find the kth largest element in an unsorted array. Note that it is the kth largest element in the sorted order,
not the kth distinct element. """

from heapq import heappush, heappop
from random import randint
import unittest2 as unittest


def find_kth_largest_v1(nums, k):
    """ The naive solution would be to sort the array first and then return kth element from the end.
    Time complexity: O(N logN)
    Space complexity: O(N)
    """
    return sorted(nums)[-k]


def find_kth_largest_v2(nums, k):
    """ Build a min heap and add all elements from the array into this heap one by one keeping the size
         of the heap always less than or equal to k. That would result in a heap containing the k largest elements of
         the array. The head of this heap is the answer, i.e. the kth largest element of the array.

    Time complexity: O(N logK), for heap construction
    Space complexity: O(k), to store heap elements
    """
    heap = []
    for num in nums:
        heappush(heap, num)
        if len(heap) > k:
            heappop(heap)
    return heap[0]


# Video explanation: https://youtu.be/hGK_5n81drs
# Video explanation: https://youtu.be/XEmy13g1Qxc
def find_kth_largest_v3(nums, k):
    """ QuickSelect.

        This approach is basically the same as for QuickSort. For simplicity, notice that the kth largest element is
        the same as (N - k + 1)th smallest element, i.e. the element at index (N - k), hence we could implement
        kth smallest algorithm for this problem.

        First, we choose a pivot and define its position in sorted array in a linear time. This could be done with
        the help of partitioning algorithm. As output, we have an array where the pivot is at its perfect position in
        the ascending sorted array, all elements to the left of the pivot are smaller than the pivot, and all elements
        to the right of the pivot are larger than or equal to the pivot.

        There are different partition algorithms. The most simple one is Lomuto's Partition Scheme, and so is what
        we will use. Here is how it works:

            - Swap the pivot and the rightmost element
            - Set the store pointer i and scan pointer j at the beginning of the array: i = j = left
            - Iterate over the array and move each element to less than the pivot to the left partition
            - Move i one step to the right after each swap.
            - Once the entire array scanned, move the pivot to its original place and return this index.

        If there are exactly (k - 1) elements greater than the pivot, the pivot must be the kth largest element.
        If there are more than (k- 1) elements greater than the pivot, we can discard elements less than or equal to the
        pivot; the kth largest element must be greater than the pivot.
        If there are less than (k - 1) elements greater than the pivot, we can discard elements greater than or equal to
        the pivot.

        If that would've been a QuickSort algorithm, we would have proceeded recursively to use quicksort for the
        both parts that would result in O(N logN) time complexity. Here, there is no need to deal with both parts since
        now we know in which part to search for the (N - k)th smallest element, and that reduces the average time
        complexity to O(N). Unlike QuickSort, we only need to focus on one subarray in QuickSelect.

    Time complexity: O(N), on average each partition operation splits the remaining input into two equal parts. We can
    disregard one of those parts, because we know the solution is not in that part. Since we expect to reduce the
    number of elements to process by roughly half, the average time complexity T(N) satisfies T(N) = O(N) + T(N/2).
    This solves to T(N) = O(N). The worst-case time complexity is O(N^2), which occurs when the randomly selected pivot
    is the smallest or largest element in the current subarray. The probability of the worst-case reduces exponentially
    with the length of the input array, and the worst-case is a nonissue in practice. For this reason, the randomized
    selection algorithm is sometimes said to have almost certain O(N) time complexity.
    Space complexity: O(1)
    """

    def partition(left, right):
        """ This is the same partitioning routine of QuickSort. """

        # Select a random pivot index between left and right, so that even when the worst case input would
        # be provided the algorithm wouldn't be affected
        random_index = randint(left, right)
        pivot = nums[random_index]
        nums[right], nums[random_index] = nums[random_index], nums[right]
        i = j = left
        # i will keep track of the 'tail' of the section of elements less than the pivot so that at the end we
        # can 'sandwich' the pivot between the section less than it and the section greater than it.
        # j will scan for us
        while j < right:
            if nums[j] <= pivot:
                nums[i], nums[j] = nums[j], nums[i]  # Execute the swap
                i += 1
            j += 1
        # Swap the pivot value right after the section of items less than the pivot pointed to by i
        nums[i], nums[right] = nums[right], nums[i]
        return i  # Return the pivot's final resting position

    n = len(nums)
    left, right = 0, n - 1
    # kth largest is the same as (n - k + 1)th smallest. Since indexing is 0-based, we search for the (n - k)th smallest
    k = n - k
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
