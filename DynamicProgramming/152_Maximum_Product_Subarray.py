""" Given an integer array nums, find the contiguous subarray within an array (containing at least one number) which
has the largest product. """

import unittest2 as unittest


def max_product_v1(nums):
    """ This is very similar to the 53- Maximum Sub array problem. Here we keep 2 values: the max cumulative
        product UP TO current element starting from SOMEWHERE in the past, and the minimum cumulative product UP TO
        current element. At each new element, we could either add the new element to the existing product, or start
        fresh the product from current index (wipe out previous results), hence the 2 max() lines.
        The max result from A[0] to A[i] can only come from:
            Decision 1. discard previous result, restart at A[i]
            Decision 2. take A[i], MAX[i] = MAX[i-1] * A[i]
            Decision 3. this is the most tricky part: A[i] can be negative, then MAX[i-1] * A[i] is negative (suppose
            MAX[i-1] is positive).
    Time complexity: O(N)
    Space complexity: O(1)
    """
    max_so_far = min_so_far = global_max = nums[0]
    for i in range(1, len(nums)):
        candidates = (nums[i], max_so_far * nums[i], min_so_far * nums[i])  # These values are the candidates of
        # maximum product and minimum product up to ith index
        max_so_far = max(candidates)
        min_so_far = min(candidates)
        global_max = max(global_max, max_so_far)
    return global_max


class Test(unittest.TestCase):
    data = [([2, 3, -2, 4], 6), ([-2, 0, -1], 0)]

    def test_max_product(self):
        for test_array, result in self.data:
            self.assertEqual(result, max_product_v1(test_array))


if __name__ == '__main__':
    unittest.main()
