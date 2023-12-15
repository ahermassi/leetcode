""" Given an integer array nums, find the contiguous subarray within an array (containing at least one number) which
has the largest product. """

import unittest2 as unittest


# Video explanation: https://youtu.be/lXVy6YWFcRM
def max_product_v1(nums):
    """ This problem can be seen as a problem of getting the highest combo chain. The way combo chains work is that
         they build on top of the previous combo chains that we have acquired.

         The simplest case is when the numbers in nums are all positive numbers. In that case, we would only need to
         keep on multiplying the accumulated result to get a bigger and bigger combo chain as we progress.

         However, two things can disrupt the combo chain: zeroes and negative numbers.
         Let's have a 'result' placeholder that records the highest score we have achieved.

         Zeroes will reset the combo chain. We will have to restart the combo chain after zero. If we encounter another
         combo chain which is higher than the recorded high score in 'result', we just need to update 'result'.

         Negative numbers are a bit tricky. A single negative number can flip the largest combo chain to a very small
         number. This may sound like the combo chain has been completely disrupted but if we encounter another
         negative number, the combo chain can be saved. Unlike zero, we still have a hope of saving the combo chain
         as long as we have another negative number lying ahead (think of this second negative number as an antidote
         for the poison that we just consumed).

         For these reasons, while going through the numbers in nums, we will have to keep track of the maximum product
         up to the current number (we will call it 'max_so_far') and the minimum product up to the current number (we will
          call it 'min_so_far').

          'max_so_far' is used to keep track of the accumulated product of positive numbers.
          'min_so_far' is used to properly handle negative numbers.

          'max_so_far' is updated by taking the maximum value among:

            1- Current number: this value will be picked if the accumulated product has been bad (even compared to the
                 current number). This can happen when the current number has a preceding zero (e.g. [0,4]) or is
                 preceded by a single negative number (e.g. [-3,5]).

            2- Product of last 'max_so_far' and current number: this value will be picked if the accumulated product has
                 been steadily increasing (all positive numbers).

            3- Product of last 'min_so_far' and current number: this value will be picked if the current number is
                 negative and the combo chain has been disrupted by a single negative number before.

        'min_so_far' is updated the same way except that we are taking minimum among the above three numbers.

        In other words, at each new element, we could either add the new element to the existing product, or start fresh
        the product from the current index (wipe out previous results).

        The max result from nums[0] to nums[i] can only come from:

                Decision 1: discard previous result, restart at nums[i]
                Decision 2: take nums[i], max[i] = max[i-1] * nums[i]
                Decision 3: this is the trickiest part: nums[i] can be negative, then max[i-1] * nums[i] can be smaller
                than nums[i-1], and this is the reason we need to keep track of min[i] as well ('min_so_far')

    Time complexity: O(N)
    Space complexity: O(1)
    """
    # max_so_far/min_so_far store the max/min product of subarray that ends with the current element nums[i]
    max_so_far = min_so_far = 1
    global_max = nums[0]
    for num in nums:
        # These values are the candidates of maximum product and minimum product up to the current element in
        # the array: start a new product with nums[i], multiply the previous min product by nums[i], or multiply
        # the previous max product by nums[i]
        min_max_prod_candidates = (num, min_so_far * num, max_so_far * num)
        max_so_far = max(min_max_prod_candidates)
        min_so_far = min(min_max_prod_candidates)
        global_max = max(global_max, max_so_far)
    return global_max


def max_product_v2(nums):
    """ Same intuition as the previous solution.

         What do we need to know to calculate the maximum product at index i? The logic sounds similar to Kadane's
         algorithm, except that knowing only the maximum ending at index (i-1) is not enough for this problem.

         Due to negative numbers, we need the maximum and minimum ending at index (i-1). In case of a negative
         number at index i, we can swap min and max.

        Takeaway: If the current number is negative, the candidate for max should instead become the previous min
        product, because a bigger number multiplied by negative becomes smaller, hence the swap.

    Time complexity: O(N)
    Space complexity: O(1)
    """
    max_so_far = min_so_far = 1
    global_max = nums[0]
    for num in nums:
        if num < 0:
            # Multiplying by a negative makes a big number smaller and a small number bigger, so we redefine
            # min and max by swapping them
            max_so_far, min_so_far = min_so_far, max_so_far
        # max/min product for the current index is either the current number itself or the max/min of the previous
        # index times the current number
        max_so_far = max(num, max_so_far * num)
        min_so_far = min(num, min_so_far * num)
        global_max = max(global_max, max_so_far)
    return global_max


def max_product_v3(A):
    """ Calculate prefix product in A. Calculate suffix product in A. Return the max.
        It turns out that the only reason we'd ever need to use a sub-array is if there was an odd number of negative
        numbers in the array or a 0.
        If the number of negative values is even, the result is the total product, can be reached from start and end
        of array.
        If the number of negative values is odd, the result can be reached from either start or end of array, split by
        that negative value.
        This approach handles the first case by multiplying from both ends of array. It handles the second with the
        'or 1' clause that resets the product to 1 any time A[i - 1] or B[i - 1] are 0.
        In other words:
        Given an array of integers, the max product ignoring sign (i.e., absolute value) is simply the product of all
        the elements, as long there is no 0. Put another way, the more elements, the bigger the product.
        But we have to consider the sign, so if product is negative then we have an odd number of negatives. Therefore,
        the max product is the biggest of:
            1- Product of all excluding elements on the left, up to the first negative element
            2- Product of all excluding elements on the right, up to the last negative element
        So the solution is to calculate the running product, first from left to right, then from right to left. During
        the process, we are guaranteed to encounter the max product, and whenever 0 is encountered we reset product
        to 1 and continue.
    Time complexity: O(N)
    Space complexity: O(N)
    """
    B = A[::-1]
    n = len(A)
    for i in range(1, n):
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
