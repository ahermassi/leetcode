""" Given an array of integers where 1 ≤ a[i] ≤ n (n = size of array), some elements appear twice and others appear
once.
Find all the elements of [1, n] inclusive that do not appear in this array. """

from collections import defaultdict
import unittest2 as unittest


def find_disappeared_numbers_v1(nums):
    """ The intuition behind using a hash map is pretty clear in this case. All we have to do is keep track of which
        numbers we encounter in the array and then iterate from 1⋯N and check which numbers did not appear in the hash
        table. Those will be our missing numbers. Note that we can use a set data structure as well in this case since
        we are not concerned about the frequency counts of elements.
    Time complexity: O(N)
    Space complexity: O(N)
    """
    n, values = len(nums), defaultdict(int)
    for num in nums:
        values[num] = 1
    return [i for i in range(1, n + 1) if i not in values]


class Test(unittest.TestCase):
    data = [([4, 3, 2, 7, 8, 2, 3, 1], [5, 6])]

    def test_find_disappeared_numbers(self):
        for test_nums, result in self.data:
            self.assertEqual(result, find_disappeared_numbers_v1(test_nums))


if __name__ == '__main__':
    unittest.main()
