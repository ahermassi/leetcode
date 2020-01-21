""" You have some sticks with positive integer lengths.
You can connect any two sticks of lengths X and Y into one stick by paying a cost of X + Y.  You perform this action
until there is one stick remaining.
Return the minimum cost of connecting all the given sticks into one stick in this way. """

import unittest2 as unittest
from heapq import heappush, heappop


def connect_sticks(sticks):
    """ Earlier sticks will be counted again. Therefore, we have to always use the current shortest two sticks till
        only one remains.
        Why does greedy guarantee the minimum?
        The earlier combined sticks are added more times, so if we want to minimize cost, we will want to combine the
        longer sticks as late as possible.
        We cannot just sort the array once and be done. At each step when we pick two sticks, we want to pick the
        lowest possible costs. So we will have to do a sort at each iteration.
        Example: sticks = [1, 8, 3, 5]
        Step 1: cost = 1 + 3 = 4, result = [4, 8, 5]
        Step 2: cost = 4 + 5 = 9, result = [9, 8]
        Step 3: cost = 9 + 8 = 17, result = [17]
        Final cost = 4 + 9 + 17 = 30
    Time complexity: O(N * logN)
    Space complexity: O(N)
    """
    heap, res = [], 0
    for stick in sticks:
        heappush(heap, stick)
    while len(heap) > 1:
        x, y = heappop(heap), heappop(heap)
        res += x + y
        heappush(heap, x + y)
    return res


class Test(unittest.TestCase):
    data = [([2, 4, 3], 14), ([1, 8, 3, 5], 30)]

    def test_connect_sticks(self):
        for test_sticks, result in self.data:
            self.assertEqual(result, connect_sticks(test_sticks))


if __name__ == '__main__':
    unittest.main()
