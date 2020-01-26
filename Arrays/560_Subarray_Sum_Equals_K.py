""" Given an array of integers and an integer k, you need to find the total number of continuous subarrays whose sum
equals to k. """

from collections import defaultdict


def subarray_sum(nums, k):
    """ The idea behind this approach is as follows: If the cumulative sum up to two indices is the same, the sum of
        the elements lying in between those indices is zero.
        Extending the same thought further, if the cumulative sum up to two indices, say i and j, is at a difference of
        k, i.e. if sum[i] - sum[j] = k, the sum of elements lying between indices i and j is k.
        Based on these thoughts, we make use of a hash map which is used to store the cumulative sum up to all the
        indices possible along with the number of times the same sum occurs. For every sum encountered, we also
        determine the number of times the sum (sum - k) has occurred already, since it will determine the number of
        times a sub array with sum k has occurred up to the current index. We increment the count by the same amount.
        In other words:
        Remember the frequency of all prefix sums, sum to keep track of sum of all the elements so far. If we can find
        a prefix sum in the map for (sum - k), it means we can form sum == k using the elements after the element
        corresponding to that prefix sum till the current element (included). Count all such sums at each element.
    Time complexity: O(N)
    Space complexity: O(N)
    """
    prefix_sum = defaultdict(int)
    prefix_sum[0] = 1
    s = res = 0
    for num in nums:
        s += num
        if s - k in prefix_sum:
            res += prefix_sum[s - k]
        prefix_sum[s] += 1
    return res

