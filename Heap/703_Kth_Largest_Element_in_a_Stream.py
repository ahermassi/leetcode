""" Design a class to find the kth largest element in a stream. Note that it is the kth largest element in the sorted
order, not the kth distinct element.
Your KthLargest class will have a constructor which accepts an integer k and an integer array nums, which contains
initial elements from the stream. For each call to the method KthLargest.add, return the element representing the kth
largest element in the stream. """

import unittest2 as unittest
from heapq import heapify, heappush, heappop, heapreplace


class KthLargest(object):

    """ Create a min heap (priority queue) - keep it only having the k-largest elements by popping off small elements.
        With only k elements, the smallest item (self.heap[0]) will always be the kth largest.

        If a new value is bigger than the smallest, it should be added into the heap.
        If it's bigger than the smallest (that is already the kth largest), it will certainly be within the kth largest
        of the stream. """

    def __init__(self, k, nums):
        """
        :type k: int
        :type nums: List[int]
        """
        self.k = k
        self.heap = nums
        heapify(self.heap)
        while len(self.heap) > self.k:  # Keep only k largest elements
            heappop(self.heap)  # Take off smallest elements (popping returns the min element because it's min heap)

    def add(self, val):
        """
        :type val: int
        :rtype: int
        """
        if len(self.heap) < self.k:
            heappush(self.heap, val)
        elif val > self.heap[0]:
            heapreplace(self.heap, val)  # Pop smallest element and replace it with val, making val the smallest
        return self.heap[0]  # Because the heap contains the k largest elements, the one at index 0 is the kth largest


class Test(unittest.TestCase):
    kth_largest = KthLargest(3, [4, 5, 8, 2])
    a = kth_largest.add(3)
    b = kth_largest.add(5)
    c = kth_largest.add(10)
    d = kth_largest.add(9)
    e = kth_largest.add(4)

    def test_roman_to_int(self):
        self.assertEqual(4, self.a)
        self.assertEqual(5, self.b)
        self.assertEqual(5, self.c)
        self.assertEqual(8, self.d)
        self.assertEqual(8, self.e)


if __name__ == '__main__':
    unittest.main()
