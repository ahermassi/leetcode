""" Given an integer array nums, find the contiguous subarray (containing at least one number) which has the largest
sum and return its sum. """

import unittest2 as unittest


# Video explanation https://youtu.be/2MmGzdiKR9Y
def maximum_subarray_v1(nums):
    """ Kadane's algorithm.

         Whenever a question asks for the maximum or minimum of something, consider Dynamic Programming as a
         possibility. The difficult part of this problem is figuring out when a negative number is "worth" keeping in a
         subarray. This question in particular is a popular problem that can be solved using an algorithm called
         Kadane's Algorithm.

         Let's focus on one important part: where the optimal subarray begins. We'll use the following example:
         nums = [-2, 1, -3, 4, -1, 2, 1, -5, 4]

        We can see that the optimal subarray couldn't possibly involve the first 3 values - the overall sum of those
        numbers would always subtract from the total. Therefore, the subarray either starts at the first 4, or
        somewhere further to the right.

        What if we had this example though? nums = [-2, 1000000000, -3, 4, -1 ,2, 1, -5, 4]
        We need a general way to figure out when a part of the array is worth keeping.

        As expected, any subarray whose sum is positive is worth keeping. Let's start with an empty array, and iterate
        through the input, adding numbers to our array as we go along. Whenever adding the current element to the
        current sub array results in smaller value than the current element taken alone , we know the entire array is
        not worth keeping, so we'll reset it back to a single element sub array made up of the current element only.

        However, we don't actually need to build the subarray, we can just keep an integer variable max_ending_here and
        add the values of each element ending at the current index. When it becomes negative, we reset it to 0
        (an empty array).

         Iterate over the array, and at each step ask the following question: which is greater, the current element x or
         (sum thus far + x) ? If max_ending_here becomes negative, we know it isn't worth keeping, so throw it away.

         Judging if a subarray is "worth keeping" happens every time we reach a new number. Even if all the numbers are
         negative, it just means that it is never worth keeping more than 1 element.

    Time complexity: O(N)
    Space complexity: O(1)
    """
    n = len(nums)
    max_so_far = max_ending_here = nums[0]
    for i in range(1, n):
        # What's the maximum sub array ending here ? Either [current element] or [previous sub array, current element]
        max_ending_here = max(nums[i], max_ending_here + nums[i])
        max_so_far = max(max_so_far, max_ending_here)  # Update global max
    return max_so_far


def maximum_subarray_v2(nums):
    """ This is an optimization problem, which can be usually solved using DP. So when it comes to DP, the first thing
        for us to figure out is the format of the sub problem (or the state of each sub problem).
        The format of the sub problem is something like: maxSubArray(int A[], int i), which means the maxSubArray for
        A[0:i] which must has A[i] as the end element. Now the connection between the sub problem and the original one
        becomes clear. Let dp[i] be the maximum sum of a contiguous sub array ending at index i:
            dp[i] = max(nums[i], dp[i-1] + nums[i])
        If the maximum sum of a contiguous sub array up to index (i-1) is positive, it is possible to make the maximum
        sum value bigger, so we add the current element to the sum.
        If the maximum sum is negative, adding it to the current element will only make a smaller sum. So we start over
        a new sum with the current element.
    Time complexity: O(N)
    Space complexity: O(N)
    """
    n = len(nums)
    dp = [0] * n
    dp[0] = nums[0]
    for i in range(1, n):
        dp[i] = max(nums[i], dp[i-1] + nums[i])
    return max(dp)


class Test(unittest.TestCase):
    data = [
        ([-2, 1, -3, 4, -1, 2, 1, -5, 4], 6),
        ([0, -1, 5], 5)
    ]

    def test_maximum_subarray(self):
        for test_array, result in self.data:
            self.assertEqual(result, maximum_subarray_v1(test_array))
            self.assertEqual(result, maximum_subarray_v2(test_array))


if __name__ == '__main__':
    unittest.main()
