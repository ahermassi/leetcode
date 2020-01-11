""" Given a sorted integer array nums, where the range of elements are in the inclusive range [lower, upper], return
its missing ranges. """

import unittest2 as unittest


def find_missing_ranges_v1(nums, lower, upper):
    """ Just simply add lower-1 and upper+1 to the list. The missing range should be num[i-1]+1 ~> num[i]-1
    Time complexity: O(N)
    Space complexity: O(N) for the new nums array
    """
    nums = [lower - 1] + nums + [upper + 1]
    n, res = len(nums), []
    for i in range(1, n):
        gap = nums[i] - nums[i - 1]
        if gap == 2:
            res.append(str(nums[i - 1] + 1))
        elif gap > 2:
            res.append(str(nums[i - 1] + 1) + '->' + str(nums[i] - 1))
    return res


def find_missing_ranges_v2(nums, lower, upper):
    """ Same as above, but using constant space.
    Time complexity: O(N)
    Space complexity: O(1)
    """
    n, res = len(nums), []
    pre = lower - 1
    for i in range(n + 1):
        curr = upper + 1 if i == n else nums[i]  # If we go out of bound, assign upper+1 to curr
        gap = curr - pre
        if gap == 2:
            res.append(str(pre + 1))
        elif gap > 2:
            res.append(str(pre + 1) + '->' + str(curr - 1))
        pre = curr
    return res


class Test(unittest.TestCase):
    data = [([0, 1, 3, 50, 75], 0, 99, ['2', '4->49', '51->74', '76->99'])]

    def test_find_missing_ranges(self):
        for test_array, test_lower, test_upper, result in self.data:
            self.assertEqual(result, find_missing_ranges_v1(test_array, test_lower, test_upper))


if __name__ == '__main__':
    unittest.main()
