""" Given an integer array nums, find the contiguous subarray within an array (containing at least one number) which
has the largest product. """

import unittest2 as unittest


def max_product_v1(nums):
    """ This is very similar to the 53- Maximum Sub array problem. Here we keep 2 values: the max cumulative
        product UP TO current element starting from SOMEWHERE in the past, and the minimum cumulative product UP TO
        current element. At each new element, we could either add the new element to the existing product, or start
        fresh the product from current index (wipe out previous results), hence the 2 max() lines.
        The max result from A[0] to A[i] can only come from:
            Decision 1: discard previous result, restart at A[i]
            Decision 2: take A[i], MAX[i] = MAX[i-1] * A[i]
            Decision 3: this is the trickiest part: A[i] can be negative, then MAX[i-1] * A[i] can be smaller than
            MAX[i-1]
    Time complexity: O(N)
    Space complexity: O(1)
    """
    max_so_far = min_so_far = global_max = nums[0]  # max_so_far / min_so_far store the max/min product of sub-array
    # that ends with the current element nums[i]
    for i in range(1, len(nums)):
        candidates = (nums[i], max_so_far * nums[i], min_so_far * nums[i])  # These values are the candidates of
        # maximum product and minimum product up to ith index: start a new product with nums[i], multiply the previous
        # num product with nums[i], or multiply the previous max product with nums[i]
        max_so_far = max(candidates)
        min_so_far = min(candidates)
        global_max = max(global_max, max_so_far)
    return global_max


def max_product_v2(nums):
    """ Same logic but in a different manner.
        What do we need to know to calculate maximum product at i? Recall what we did in Maximum Sub-array Sum
        (Kadane's algorithm), only known maximum ending at i-1 is not enough for this one.
        Due to negative numbers, we need max and min ending at i-1. In case of a negative number at i, we then swap
        min an max. Therefore, we maintain two local optimal variables, update them in each iteration and the global
        maximum as well.
    Time complexity: O(N)
    Space complexity: O(1)
    """
    n = len(nums)
    max_so_far = min_so_far = global_max = nums[0]
    for i in range(1, n):
        if nums[i] < 0:  # Multiplying by a negative makes big number smaller and small number bigger, so we redefine
            # min and max by swapping them
            max_so_far, min_so_far = min_so_far, max_so_far
        # max/min product for the current index is either the current number itself or the max/min of the previous
        # index times the current number
        max_so_far = max(nums[i], max_so_far * nums[i])
        min_so_far = min(nums[i], min_so_far * nums[i])
        global_max = max(global_max, max_so_far)
    return global_max


def max_product_v3(A):
    """ Calculate prefix product in A. Calculate suffix product in A. Return the max.
        It turns out that the only reason you'd ever need to use a sub-array is if there was an odd number of negative
        numbers in the array or a 0.
        If the number of negative values is even, the result is the total product, can be reached from start and end
        of array.
        If the number of negative values is odd, the result can be reached from either start or end of array, split by
        that negative value.
        This approach handles the first case by multiplying from both ends of array. It handles the second with the
        'or 1' clause that resets the product to 1 any time A[i - 1] or B[i - 1] are 0.
    Time complexity: O(N)
    Space complexity: O(N)
    """
    B = A[::-1]
    for i in range(1, len(A)):
        A[i] *= A[i - 1] or 1
        B[i] *= B[i - 1] or 1
    return max(A + B)


class Test(unittest.TestCase):
    data = [([2, 3, -2, 4], 6), ([-2, 0, -1], 0)]

    def test_max_product(self):
        for test_array, result in self.data:
            self.assertEqual(result, max_product_v1(test_array))
            self.assertEqual(result, max_product_v2(test_array))


if __name__ == '__main__':
    unittest.main()
