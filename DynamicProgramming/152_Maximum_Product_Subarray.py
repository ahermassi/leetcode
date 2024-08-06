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
         algorithm, except that knowing only the maximum ending at index i-1 is not enough for this problem.

         Due to negative numbers, we need the maximum and minimum ending at index i-1. In the case of a negative number
         at index i, we can swap min and max.

        Takeaway: if the current number is negative, the candidate for max should instead become the previous min
        product, because a bigger number multiplied by a negative becomes smaller, hence the swap.

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
        # max/min product for the current index is either the current number itself or the max/min up to the previous
        # index multiplied by the current number
        max_so_far = max(num, max_so_far * num)
        min_so_far = min(num, min_so_far * num)
        global_max = max(global_max, max_so_far)
    return global_max


def max_product_v3(nums):
    """ We can derive the maximum product from the prefix and suffix products.

         It turns out that the only reason the answer could be a subarray is if there is an odd number of negative
         numbers in the array or a 0.

         If the number of negative values is even, the result is the product of all numbers in the array.
         However, If the number of negative values is odd, the result can be reached from either the start or the end of
         the array, split by that negative value.

         Given an array of integers, the max product ignoring sign (i.e., absolute value) is simply the product of all
         the elements, as long as there is no 0. Put another way, the more elements, the bigger the product.
         But we have to consider the sign, so if the product is negative then we have an odd number of negatives.

         Therefore, the max product is the maximum of:

             1- Prefix product up to and excluding the last negative number
             2- Suffix product up to and excluding the first negative number

         So the solution is to calculate the running product, first from left to right, then from right to left. During
         the process, we are guaranteed to encounter the max product, and whenever 0 is encountered we reset the
         product to 1 and continue.

         If we have an odd number of negative numbers, then the solution is the product of numbers from left till the
         last negative number or the other way around. We cannot exclude a negative number that is not the first or the
         last, because if by doing so we will need to exclude all other negative nums following that negative number
         (because we are breaking the product at this point) and then that wouldn't result in the maximum product.

         The best subarray in terms of product will definitely not contain zeroes, and it will definitely contain an
         EVEN number of negatives. It's best to shave off one from the left or one from the right. It doesn't benefit us
         to take one out the middle, since we could always extend more to the other side and get a bigger product.
         So the idea is we are excluding only one negative number so that we are able to make the number of negative
         elements even.

         Assume the array has an odd number of negative numbers. The first negative number is -2 and the last negative
         number is -3. So the array looks like .....-2.......-3.......
         The maximum product can either be made of all numbers from the beginning of the array to the first non-zero
         number just before -3, or from the end of the array to the first non-zero number just after -2.

         We only need to consider sub-arrays without 0. If an array has 0 in it, then the array should be divided into
         two parts on either side of 0 because 0 cannot ever be included in the product (hence resetting the product
         to 1). Example: [1,2,0,3,4,5]. Maximum product should be on either side of 0.

         Example case 1: -ve, Max Subarray, -ve
         In this case, we can include both negative numbers and get a larger product.

         Example case 2: +ve, Max Subarray, +ve
         This case is trivial as both positive numbers need to be included in the product.

         Example case 3: -ve, Max Subarray, +ve
         Example case 4: +ve, Max Subarray, -ve
         In both the above cases we can extend max subarray to cover the positive element to get a larger product and
         thus anchor the array to the right or left end.

         Now the problem is reduced to calculating the product of numbers from left, and then doing the same from right,
         and then calculating the max product.

         !!! IMPORTANT !!!
         We don't need to explicitly find out the indices of first ad last negative elements in the case of an odd
         number of negatives. Running the prefix and suffix products guarantees the max product is encountered.

         Example: nums = [-1, -2, -3]
         cur_prod takes the following values during the iteration:
         left -> right: -1, 2, -6
         right -> left: -3, 6, -6
         The max product 6 is encountered right before the first negative (-1).

         Example: nums = [-1, -2, 0, -3]
         cur_prod takes the following values during the iteration:
         left -> right: -1, 2, 0, -3
         right -> left: -3, 0, -2, 2
         The max product 2 is encountered for the first time to the left of the first zero (-1), and a second time as
         the product of all elements of sub-array [-1, -2] which has an even number of negative elements.

    Time complexity: O(N)
    Space complexity: O(1)
    """
    n = len(nums)
    max_prod = nums[0]
    cur_prod = 1
    for num in nums:
        cur_prod *= num
        max_prod = max(max_prod, cur_prod)
        if cur_prod == 0:
            cur_prod = 1
    cur_prod = 1
    for i in reversed(range(n)):
        cur_prod *= nums[i]
        max_prod = max(max_prod, cur_prod)
        if cur_prod == 0:
            cur_prod = 1
    return max_prod


class Test(unittest.TestCase):
    data = [([2, 3, -2, 4], 6), ([-2, 0, -1], 0)]

    def test_max_product(self):
        for test_array, result in self.data:
            self.assertEqual(result, max_product_v1(test_array))
            self.assertEqual(result, max_product_v2(test_array))


if __name__ == '__main__':
    unittest.main()
