""" Design a class to find the kth largest element in a stream. Note that it is the kth largest element in the sorted
order, not the kth distinct element.
Your KthLargest class will have a constructor which accepts an integer k and an integer array nums, which contains
initial elements from the stream. For each call to the method KthLargest.add, return the element representing the kth
largest element in the stream. """

import unittest2 as unittest
from heapq import heappush, heappop

# Video explanation: https://www.youtube.com/watch?v=hOjcdrqMoQ8


class KthLargest(object):

    """ Create a min heap (priority queue), keep it only having the k largest elements by popping off small elements.
        With only k largest elements, the smallest item (heap[0]) will always be the kth largest.
    """

    def __init__(self, k, nums):
        """ Build a min heap from the initial stream.
        Time complexity: O(N logN), where N is the length of nums
        Space complexity: O(N)
        """
        self.heap = []
        self.k = k
        for num in nums:
            heappush(self.heap, num)

    def add(self, val):
        """ Push the new value into the heap and make sure the heap's size doesn't exceed k.
        Time complexity: O(logK)
        Space complexity: O(1)
        """
        heappush(self.heap, val)
        while len(self.heap) > self.k:
            heappop(self.heap)
        return self.heap[0]  # Because the heap contains the k largest elements, the one at index 0 is the kth largest


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
