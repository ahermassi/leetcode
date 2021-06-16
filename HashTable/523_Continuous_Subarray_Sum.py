""" Given a list of non-negative numbers and a target integer k, write a function to check if the array has a
continuous sub array of size at least 2 that sums up to a multiple of k, that is, sums up to n*k where n is also an
integer. """

import unittest2 as unittest


def check_subarray_sum_v1(nums, k):
    """ Brute force.
        The brute force approach is trivial. We consider every possible sub array of size greater than or equal to 2,
        find out its sum by iterating over the elements of the sub array, and then we check if the sum obtained is an
        integer multiple of the given k.
    Time complexity: O(N^2)
    Space complexity: O(1)
    """
    n = len(nums)
    for i in range(n):
        cur_sum = nums[i]
        for j in range(i + 1, n):
            cur_sum += nums[j]
            if cur_sum % k == 0:
                return True
    return False


def check_subarray_sum_v2(nums, k):
    """ Similar to 560- Subarray Sum Equals K. The idea behind this approach is as follows: If the cumulative sum
        up to two indices is the same, the sum of the elements lying in between those indices is zero.
        Extending the same thought further, if the cumulative sum up to two indices, say i and j, is at a difference of
        k, i.e. if sum[i] - sum[j] = k, the sum of elements lying between indices i and j is k.
        We iterate through the input array exactly once, keeping track of the running sum mod k of the elements in the
        process. If we find that a running sum value at index j has been previously seen before in some earlier index i
        in the array, then we know that the sub-array (i,j] contains a desired sum.
        This is one of those magics of remainder theorem:
            ((a + (n*x)) % x) is same as (a % x)
            1- Running sum from first element to index i : sum_i. If we mod k, it will be: sum_i = k * x + modk_1
            2- Running sum from first element to index j : sum_j. If we mod k, it will be: sum_j = k * y + modk_2
        If they have the same mod, which is modk_1 == modk_2, subtracting these two running sums gives the difference:
            sum_i - sum_j = (x - y) * k = constant * k
        The difference is the sum of elements between indices i and j, and the value is a multiple of k.
        It is based on this elementary fact:
            For a line segment AC with a point B in it, visualized as A---B---C:
            If mod(AC, k) == mod(AB, k), then BC must be equal to n * k
        Key point: if we can find any two subarray of prefix sum have same mod value, then their difference MUST be
        divisible by k.
        For e.g. in case of the array [23, 2, 6, 4, 7] and k = 6, the running sum is [23, 25, 31, 35, 42] and the
        remainders (mod 6) are [5, 1, 1, 5, 0]. We got remainder 5 at index 0 and at index 3. That means in between
        these two indices we must have added a number which is multiple of k.
    Time complexity: O(N)
    Space complexity: O(min(N,k)), hash map can contain up to min(N,k) different pairings
    """
    sum_index = {0: -1}  # This initialization avoids the case when the first element of the array is multiple of k,
    # since 0-(-1)= 1 is not greater than 1, while we want sub arrays of size at least 2
    cur_sum = 0
    for i, num in enumerate(nums):
        cur_sum += num
        cur_sum %= k
        if cur_sum not in sum_index:
            sum_index[cur_sum] = i
        elif i - sum_index[cur_sum] > 1:  # Difference of sub array's start/end indices to ensure its size is at least 2
            return True
    return False


class Test(unittest.TestCase):
    data = [([23, 2, 4, 6, 7], 6, True)]

    def test_check_subarray_sum(self):
        for test_array, test_k, result in self.data:
            self.assertEqual(result, check_subarray_sum_v1(test_array, test_k))
            self.assertEqual(result, check_subarray_sum_v2(test_array, test_k))


if __name__ == '__main__':
    unittest.main()

