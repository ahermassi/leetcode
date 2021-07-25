""" Given an array nums of n integers and an integer target, find three integers in nums such that the sum is closest
to target. Return the sum of the three integers. You may assume that each input would have exactly one solution. """

import unittest2 as unittest


def three_sum_closest(nums, target):
    """ First, sort the list. Then, use 3 pointers to point to current element, next element and the last element. If the
        sum is less than target, it means we have to add a larger element so next element moves to the next. If the sum
        is greater, it means we have to add a smaller element so last element moves to the second last element. Keep
        doing this until the end. Each time compare the gap between sum and target, and if it is less than the minimum
        gap found so far, then the current sum is the best we could achieve so far.
    Time complexity: O(N^2)
    Space complexity: O(N), for sorting
    """
    nums.sort()
    n, closest_sum, = len(nums), float('inf')
    for i in range(n - 2):
        left, right = i + 1, n - 1
        while left < right:
            cur_sum = nums[i] + nums[left] + nums[right]
            if cur_sum == target:  # A gap of 0 between target and cur_sum. We can't achieve better.
                return cur_sum
            if abs(target - cur_sum) < abs(target - closest_sum):
                closest_sum = cur_sum
            if cur_sum < target:
                left += 1
            else:
                right -= 1
    return closest_sum


class Test(unittest.TestCase):
    data = [([-1, 2, 1, -4], 1, 2), ([0, 2, 1, -3], 1, 0)]

    def test_three_sum_closest(self):
        for test_array, test_target, result in self.data:
            self.assertEqual(result, three_sum_closest(test_array, test_target))


if __name__ == '__main__':
    unittest.main()
