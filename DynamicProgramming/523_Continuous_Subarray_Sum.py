""" Given a list of non-negative numbers and a target integer k, write a function to check if the array has a
continuous sub array of size at least 2 that sums up to a multiple of k, that is, sums up to n*k where n is also an
integer. """

import unittest2 as unittest


def check_subarray_sum_v1(nums, k):
    """ Brute force.
        The brute force approach is trivial. We consider every possible sub array of size greater than or equal to 2,
        find out its sum by iterating over the elements of the sub array, and then we check if the sum obtained is an
        integer multiple of the given k.
    Time complexity: O(N ** 2)
    Space complexity: O(1)
    """
    n = len(nums)
    for i in range(n):
        sum = nums[i]
        for j in range(i + 1, n):
            sum += nums[j]
            if k == 0:
                if sum == 0:
                    return True
                continue
            elif sum % k == 0:
                return True
    return False


class Test(unittest.TestCase):
    data = [([23, 2, 4, 6, 7], 6, True)]

    def test_check_subarray_sum(self):
        for test_array, test_k, result in self.data:
            self.assertEqual(result, check_subarray_sum_v1(test_array, test_k))


if __name__ == '__main__':
    unittest.main()

