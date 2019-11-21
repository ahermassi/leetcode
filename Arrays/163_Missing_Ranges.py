""" Given a sorted integer array nums, where the range of elements are in the inclusive range [lower, upper], return
its missing ranges. """

import unittest2 as unittest


def find_missing_ranges_v1(nums, lower, upper):
    """ Just simply Add lower-1 and upper+1 into the list. The missing range should be num[i]+1 ~> num[i+1]-1
    Time complexity: O(N)
    Space complexity: O(N) for the new nums array
    """
    res = []
    nums = [lower - 1] + nums + [upper + 1]
    for i in range(len(nums) - 1):
        gap = nums[i + 1] - nums[i]
        if gap == 2:
            res.append(str(nums[i] + 1))
        elif gap > 2:
            res.append(str(nums[i] + 1) + '->' + str(nums[i + 1] - 1))
    return res


def find_missing_ranges_v2(nums, lower, upper):
    """ Same as above, but without using any extra space. The edge cases are handled manually.
    Time complexity: O(N)
    Space complexity: O(1)
    """
    if not nums:
        return [str(lower) + '->' + str(upper) if lower != upper else str(lower)]
    res = []
    if nums[0] > lower:  # First edge case of left boundary
        res.append(str(lower) + '->' + str(nums[0] - 1) if lower != nums[0] - 1 else str(lower))
    n, i = len(nums), 0
    for i in range(n - 1):
        gap = nums[i + 1] - nums[i]
        if gap == 2:
            res.append(str(nums[i] + 1))
        elif gap > 2:
            res.append(str(nums[i] + 1) + '->' + str(nums[i + 1] - 1))
    if nums[-1] < upper:  # Second edge case of right boundary
        res.append(str(nums[-1] + 1) + '->' + str(upper) if nums[-1] + 1 != upper else str(upper))
    return res


class Test(unittest.TestCase):
    data = [([0, 1, 3, 50, 75], 0, 99, ['2', '4->49', '51->74', '76->99'])]

    def test_find_missing_ranges(self):
        for test_array, test_lower, test_upper, result in self.data:
            self.assertEqual(result, find_missing_ranges_v1(test_array, test_lower, test_upper))


if __name__ == '__main__':
    unittest.main()