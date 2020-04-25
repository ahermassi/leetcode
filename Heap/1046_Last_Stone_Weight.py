""" We have a collection of stones, each stone has a positive integer weight.
Each turn, we choose the two heaviest stones and smash them together.  Suppose the stones have weights x and y with
x <= y.  The result of this smash is:
If x == y, both stones are totally destroyed;
If x != y, the stone of weight x is totally destroyed, and the stone of weight y has new weight y-x.
At the end, there is at most 1 stone left.  Return the weight of this stone (or 0 if there are no stones left.) """

from bisect import insort
import unittest2 as unittest


def last_stone_weight_v1(stones):
    """ Conceptually, the simplest way we could solve this problem is to repeatedly search for the 2 largest stones in
        the array, delete them, and then if they are not the same size, add the new stone size back in. We can repeat
        this process until there is only one stone left.
        To simplify the search-for-maximum process, we could maintain a sorted array. We'd need to sort the array at
        the start, and then ensure that each time we need to add a stone back, that we're maintaining the sorted order.
    Time complexity: O(N logN + N^2) = O(N^2), sorting and maintaining sorted order by shuffling existing stones
    Space complexity: O(N), for the sort
    """
    stones.sort()
    while len(stones) > 1:
        a, b = stones.pop(), stones.pop()  # a >= b
        if a != b:
            insort(stones, a - b)
    return stones[0] if stones else 0


class Test(unittest.TestCase):
    data = [([2, 7, 4, 1, 8, 1], 1)]

    def test_last_stone_weight(self):
        for test_stones, result in self.data:
            self.assertEqual(result, last_stone_weight_v1(test_stones))


if __name__ == '__main__':
    unittest.main()
