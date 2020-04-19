""" Design a class to find the kth largest element in a stream. Note that it is the kth largest element in the sorted
order, not the kth distinct element.
Your KthLargest class will have a constructor which accepts an integer k and an integer array nums, which contains
initial elements from the stream. For each call to the method KthLargest.add, return the element representing the kth
largest element in the stream. """

import unittest2 as unittest
from heapq import heappush, heappop


class KthLargest(object):

    """ Create a min heap (priority queue), keep it only having the k largest elements by popping off small elements.
        With only k elements, the smallest item (heap[0]) will always be the kth largest.
        If a new value is bigger than the smallest, it should be added into the heap.
        If it's bigger than the smallest (that is already the kth largest), it will certainly be within the k largest
        of the stream.
    """

    def __init__(self, k, nums):
        """ We can build a min heap that contains only k largest elements.
        Time complexity: O(N logK), where N is the length of nums, we push N items into a heap of size k
        Space complexity: O(k)
        """
        self.k = k
        self.heap = []
        for num in nums:
            heappush(self.heap, num)
            if len(self.heap) > k:
                heappop(self.heap)

    def add(self, val):
        """ Compare the new element val with min to decide if we should pop min and insert val.
        Time complexity: O(logK)
        Space complexity: O(1)
        """
        heap, k = self.heap, self.k
        if len(heap) < k:
            heappush(heap, val)
        elif val > heap[0]:  # Pop smallest element (kth largest) and replace it with val, making val kth largest
            heappop(heap)
            heappush(heap, val)
        return heap[0]  # Because the heap contains the k largest elements, the one at index 0 is the kth largest
        # Similarly:
        # heappush(heap, val)
        # if len(heap) > k:
        #     heappop(heap)
        # return heap[0]


class Test(unittest.TestCase):
    kth_largest = KthLargest(3, [4, 5, 8, 2])
    a = kth_largest.add(3)
    b = kth_largest.add(5)
    c = kth_largest.add(10)
    d = kth_largest.add(9)
    e = kth_largest.add(4)

    def test_kth_largest(self):
        self.assertEqual(4, self.a)
        self.assertEqual(5, self.b)
        self.assertEqual(5, self.c)
        self.assertEqual(8, self.d)
        self.assertEqual(8, self.e)


if __name__ == '__main__':
    unittest.main()
