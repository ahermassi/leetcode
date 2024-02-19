""" We have a collection of stones, each stone has a positive integer weight.
Each turn, we choose the two heaviest stones and smash them together.  Suppose the stones have weights x and y with
x <= y.  The result of this smash is:
If x == y, both stones are totally destroyed;
If x != y, the stone of weight x is totally destroyed, and the stone of weight y has new weight y-x.
At the end, there is at most 1 stone left. Return the weight of this stone (or 0 if there are no stones left.) """

from bisect import insort
from heapq import heappush, heappop
import unittest2 as unittest


def last_stone_weight_v1(stones):
    """ Conceptually, the simplest way we could solve this problem is to repeatedly search for the 2 largest stones in
         the array, delete them, and then if they are not the same size, add the new stone size back in. We can repeat
         this process until there is only one stone left.

         To simplify the search-for-maximum process, we could maintain a sorted array. We'd need to sort the array at
         the start, and then ensure that each time we need to add a stone back, that we're maintaining the sorted order.

         Unfortunately, inserting a stone into a sorted array is an O(N) operation. While we can use binary search to
         determine where we should put it, inserting it still ultimately requires shifting all the stones after it down
         by one place.

    Time complexity: O(N logN + N^2) = O(N^2), sorting and maintaining sorted order by shuffling existing stones
    Space complexity: O(N), for the sort
    """
    stones.sort()
    while len(stones) > 1:
        a, b = stones.pop(), stones.pop()  # a >= b
        if a != b:
            insort(stones, a - b)
    return stones[0] if stones else 0


def last_stone_weight_v2(stones):
    """ For this kind of maximum-maintenance, we use a max heap.

         Multiply all numbers going into the heap by -1, and then multiply them by -1 to restore them when they come
         out. While there is more than one stone left, remove the two largest, smash them together, and insert the
         result back into the heap if it is non-zero.

    Time complexity: O(N logN), converting an array into a heap takes O(N) time (it isn't actually sorting; it's putting
    them into an order that allows us to get the maximums, each in O(logN) time). The main loop iterates up to
    (N - 1) times, and is doing up to three O(logN) operation each time; two removes, and an optional add. This means
    that we're doing N * O(logN)=O(N logN) operations.
    Space complexity: O(N)
    """
    heap = []
    for stone in stones:
        heappush(heap, -stone)
    while len(heap) >= 2:
        a, b = -heappop(heap), -heappop(heap)  # a >= b
        if a != b:
            heappush(heap, b - a)  # b - a = - (a - b)
    return -heappop(heap) if heap else 0


class Test(unittest.TestCase):
    data = [([2, 7, 4, 1, 8, 1], 1)]

    def test_last_stone_weight(self):
        for test_stones, result in self.data:
            self.assertEqual(result, last_stone_weight_v1(test_stones))
            self.assertEqual(result, last_stone_weight_v2(test_stones))


if __name__ == '__main__':
    unittest.main()
