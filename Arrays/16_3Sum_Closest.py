""" Given an array nums of n integers and an integer target, find three integers in nums such that the sum is closest
to target. Return the sum of the three integers. You may assume that each input would have exactly one solution. """

import unittest2 as unittest


def three_sum_closest(nums, target):
    """ First, sort the list. Then, use 3 pointers to point current element, next element and the last element. If the
        sum is less than target, it means we have to add a larger element so next element moves to the next. If the sum
        is greater, it means we have to add a smaller element so last element moves to the second last element. Keep
        doing this until the end. Each time compare the gap between sum and target, and if it is less than the minimum
        gap found so far, then the current sum is the best we could achieve so far.
    Time complexity: O(N^2)
    Space complexity: O(1)
    """
    nums.sort()
    n, res, = len(nums), nums[0] + nums[1] + nums[2]  # Initial result could be any 3 elements. This could be the sum
    # of any 3 elements but not a random number
    for i in range(n - 2):
        left, right = i + 1, n - 1
        while left < right:
            s = nums[i] + nums[left] + nums[right]
            if s == target:  # A gap of 0 between target and s. We can't achieve better.
                return s
            if abs(target - s) < abs(target - res):
                res = s
            if s < target:
                left += 1
            else:
                right -= 1
    return res


class Test(unittest.TestCase):
    data = [([-1, 2, 1, -4], 1, 2), ([0, 2, 1, -3], 1, 0)]

    def test_three_sum_closest(self):
        for test_array, test_target, result in self.data:
            self.assertEqual(result, three_sum_closest(test_array, test_target))


if __name__ == '__main__':
    unittest.main()
