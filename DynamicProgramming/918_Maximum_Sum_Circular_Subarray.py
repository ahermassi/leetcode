""" Given a circular integer array nums of length n, return the maximum possible sum of a non-empty subarray of nums.

A circular array means the end of the array connects to the beginning of the array. Formally, the next element of
nums[i] is nums[(i + 1) % n] and the previous element of nums[i] is nums[(i - 1 + n) % n].

A subarray may only include each element of the fixed buffer nums at most once. Formally, for a subarray nums[i],
nums[i + 1], ..., nums[j], there does not exist i <= k1, k2 <= j with k1 % n == k2 % n.
"""


# Video explanation: https://youtu.be/fxT9KjakYPM
def max_subarray_sum_circular(nums):
    """ Kadane's algorithm. Similar to 53- Maximum Subarray.

        As a circular array, the maximum subarray sum can be either the maximum "normal sum" which is the maximum sum of
         the ordinary array or a "special sum" which would involve elements that wrap around the array.

         The "special sum" would be the combination of a prefix sum and a suffix sum. A prefix is a subarray that starts
         at the first element of the array and a suffix is a subarray that ends at the final element of the array.
         The "special sum" would involve a prefix and suffix that do not overlap.

         The normal sum is the 53- Maximum Subarray problem and can be solved with Kadane's algorithm. As such, we can
         focus on finding the "special sum".

         Instead of thinking about the "special sum" as the sum of a prefix and a suffix, we can think about it as the
         sum of all elements, minus a subarray in the middle. In this case, we want to minimize this middle subarray
         sum, which we can calculate using Kadane's algorithm as well (check the .img file).

         By minimizing the middle subarray, we necessarily maximize the subarray surrounding that subarray, i.e., the
         circular one. The smaller the middle subarray we get, the bigger the circular array around it will be.

         If we use Kadane's algorithm but use min() instead of max() to update the current subarray sum, it will give us
         the minimum subarray. Then, we can just subtract the minimum subarray from the total sum to find the
         "special sum".

         There is one case we need to consider, however. What if the minimum subarray contains all elements, such as in
         the case where every element is negative? In that case, the "special sum" would represent an empty array, which
         is invalid because the problem explicitly states that we need a non-empty subarray.

         If we find that the minimum subarray is equal to the total sum, then we need to ignore the "special sum" and
         just return the "normal sum". So if the minimum subarray is just the entire array, no circular array is better.
         If there were any better circular subarray, then the minimum middle array would not contain all elements
         because the subarray sum could be decreased by removing those elements. Therefore, if the minimum is simply
         the entire array, we can throw out all circular arrays and just evaluate this normally. So we return the answer
         if the array weren't circular.

         In other words, if all numbers are negative, global_max = max(nums) and global_min = sum(nums). In this case,
         max(global_max, total - global_min) = 0, which means the sum of an empty subarray. According to the
         description, we need to return max(nums), i.e. whatever the largest negative value was, instead of the sum of
         an empty subarray. So we return global_max to handle this corner case.

         max(prefix+suffix) = max(total sum - subarray)
                                       = total sum + max(-subarray)
                                       = total sum - min(subarray)

    Time complexity: O(N)
    Space complexity: O(1)
    """
    min_ending_here = max_ending_here = 0
    global_max = global_min = nums[0]
    total = 0
    for num in nums:
        total += num
        max_ending_here = max(num, max_ending_here + num)
        global_max = max(global_max, max_ending_here)
        min_ending_here = min(num, min_ending_here + num)
        global_min = min(global_min, min_ending_here)
    if global_min == total:
        # The entire array is the minimum sum, so a better circular cannot exist. Return the best subarray if the
        # problem weren't circular
        return global_max
    # The greatest subarray may be circular, or it may not be. Return the max of the best non-circular and
    # circular subarray.
    return max(global_max, total - global_min)
