""" Given an array nums of n integers and an integer target, find three integers in nums such that the sum is closest
to target. Return the sum of the three integers. You may assume that each input would have exactly one solution. """

import unittest2 as unittest


def three_sum_closest(nums, target):
    """ First, sort the list. Then, use 3 pointers to point current element, next element and the last element. If the
        sum is less than target, it means we have to add a larger element so next element move to the next. If the sum
        is greater, it means we have to add a smaller element so last element move to the second last element. Keep
        doing this until the end. Each time compare the difference between sum and target, if it is less than minimum
        difference so far, then replace result with it, otherwise keep iterating.
    Time complexity: O(N ** 2)
    Space complexity: O(1)
    """
    nums.sort()
    min_sum = float('inf')
    for i in range(len(nums) - 2):
        left, right = i + 1, len(nums) - 1
        while left < right:
            s = nums[i] + nums[left] + nums[right]
            if s == target:
                return s
            if abs(target - s) < abs(target - min_sum):
                min_sum = s
            if s < target:
                left += 1
            elif s > target:
                right -= 1
    return min_sum


class Test(unittest.TestCase):
    data = [([-1, 2, 1, -4], 1, 2), ([0, 2, 1, -3], 1, 0)]

    def test_three_sum_closest(self):
        for test_array, test_target, result in self.data:
            self.assertEqual(result, three_sum_closest(test_array, test_target))


if __name__ == '__main__':
    unittest.main()
