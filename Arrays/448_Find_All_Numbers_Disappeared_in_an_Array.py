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


def find_disappeared_numbers_v2(nums):
    """ We definitely need to keep track of all the unique numbers that appear in the array. However, we don't want to
        use any extra space for it. This solution that we will look at in just a moment springs from the fact that:
            All the elements are in the range [1, N]
        We can make use of the input array itself to somehow mark visited numbers and then find our missing numbers.
        Since all the numbers are positive integers, for every number 'num' visited we mark the presence of that number
        by negating the number at the index equal to 'num'. Since Python follows 0-indexing, the index we mark is
        actually (num - 1). If the number at that index is already negated, we do nothing.
        In the second iteration, if a value is not marked as negative, it implies we have never seen that index before,
        so just add it to the return list.
        Let nums = [4, 3, 2, 7, 8, 2, 3, 1]. Now let's iterate through the array nums.
        At iteration 0: current number = |4|, number at index 3 (current number - 1) = 7.
            After negation: nums = [4, 3, 2, -7, 8, 2, 3, 1]
        At iteration 1: current number = |3|, number at index 2 = 2
            After negation: nums = [4, 3, -2, -7, 8, 2, 3, 1]
        At iteration 2: current number = |-2| = 2, number at index 1 = 3
            After negation: nums = [4, -3, -2, -7, 8, 2, 3, 1]
        At iteration 3: current number = |-7| = 7, number at index 6 = 3
            After negation: nums = [4, -3, -2, -7, 8, 2, -3, 1]
        At iteration 4: current number = |8| = 8, number at index 7 = 1
            After negation: nums = [4, -3, -2, -7, 8, 2, -3, -1]
        At iteration 5: current number = |2| = 2, number at index 1 = -3
            Array stays unchanged: nums = [4, -3, -2, -7, 8, 2, -3, -1]
        At iteration 6: current number = |-3| = 3, number at index 2 = -2
            Array stays unchanged: nums = [4, -3, -2, -7, 8, 2, -3, -1]
        At iteration 7: current number = |-1| = 1, number at index 0 = 4
            After negation: nums = [-4, -3, -2, -7, 8, 2, -3, -1]
        Now the indices at which there are still positive numbers are the numbers (index + 1) that weren't present in
        the array.
    Time complexity: O(N)
    Space complexity: O(1)
    """
    for num in nums:
        index = abs(num) - 1
        if nums[index] > 0:
            nums[index] *= -1
    n = len(nums)
    return [i + 1 for i in range(n) if nums[i] > 0]


class Test(unittest.TestCase):
    data = [([4, 3, 2, 7, 8, 2, 3, 1], [5, 6])]

    def test_find_disappeared_numbers(self):
        for test_nums, result in self.data:
            self.assertEqual(result, find_disappeared_numbers_v1(test_nums))
            self.assertEqual(result, find_disappeared_numbers_v2(test_nums))


if __name__ == '__main__':
    unittest.main()
