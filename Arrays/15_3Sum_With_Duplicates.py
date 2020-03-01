""" Design an algorithm that takes as input an array and a number, and determines if there are three entries in the
array (not necessarily distinct) which add up to the specified number. """

import unittest2 as unittest


def has_three_sum(nums, t):
    """ How would we check if a given array entry can be added to two more entries to get the specified number?
        First, sort the input. For each index i, start with nums[i] + nums[n-1]. If this equals (t - nums[i]), we're
        done. Otherwise, if nums[i] + nums[n-1] < t - nums[i], we move to nums[i+1] + nums[n-1]; there is no chance of
        nums[i] pairing with any other entry to get (t - nums[i]) (since nums[n-1] is the largest value in nums).
        Similarly, if nums[i] + nums[n-1] > t - nums[i], we move to nums[i] + nums[n-2].
    Time complexity: O(N logN + N^2) = O(N^2)
    Space complexity: O(N), for Timsort
    """
    nums.sort()
    n, res = len(nums), []
    for i in range(n):
        j, k = i, n - 1  # j starts from i instead of (i+1) because duplicates are allowed
        while j <= k:
            s = nums[i] + nums[j] + nums[k]
            if s == t:
                return True
            if s < t:
                j += 1
            else:
                k -= 1
    return False


class Test(unittest.TestCase):
    data = [([11, 2, 5, 7, 3], 21, True), ([1], 3, True), ([1], 2, False)]

    def test_has_three_sum(self):
        for test_array, test_target, result in self.data:
            self.assertEqual(result, has_three_sum(test_array, test_target))


if __name__ == '__main__':
    unittest.main()
