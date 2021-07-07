""" Given an integer array nums of length n, return true if there is a triplet (i, j, k) which satisfies the following
conditions:

0 < i, i + 1 < j, j + 1 < k < n - 1
The sum of subarrays (0, i - 1), (i + 1, j - 1), (j + 1, k - 1) and (k + 1, n - 1) is equal.

A subarray (l, r) represents a slice of the original array starting from the element indexed l to the element indexed
r. """


def split_array_v1(nums):
    """ The limits based on the length of the array n can be rewritten as:
            1 ≤ i ≤ n-6     -->  1 ≤ i < n-5
            i+2 ≤ j ≤ n-4   -->  i+2 ≤ j < n-3
            j+2 ≤ k ≤ n-2   -->  j+2 ≤ k < n-1
        Let's look at the first solution that comes to our mind.
        We simply traverse over all the elements of the array. We consider all the possible subarrays taking care of
        the constraints imposed on the cuts, and check if any such cuts exist which satisfy the given equal sum
        quadruples criteria.
    Time complexity: O(N^4)
    Space complexity: O(1)
    """
    n = len(nums)
    if n < 6:
        return False
    for i in range(1, n - 5):
        for j in range(i + 2, n - 3):
            for k in range(j + 2, n - 1):
                if sum(nums[:i]) == sum(nums[i + 1:j]) == sum(nums[j + 1:k]) == sum(nums[k + 1:]):
                    return True
    return False


def split_array_v2(nums):
    """ In the brute force approach, we traversed over the subarrays for every triplet of cuts considered. Rather than
        doing this, we can save some calculation effort if we make use of a cumulative sum array 'prefix_sum', where
        prefix_sum[i] stores the cumulative sum of the array nums up to the ith index. Thus, now in order to find the
        sum(nums[i:j]), we can simply use (prefix_sum[j] − prefix_sum[i]). Rest of the process remains the same.
    Time complexity: O(N^3)
    Space complexity: O(N), used for storing the cumulative sum
    """
    n = len(nums)
    if n < 6:
        return False
    prefix_sum = [0] * n
    prefix_sum[0] = nums[0]
    for i in range(1, n):
        prefix_sum[i] = prefix_sum[i - 1] + nums[i]
    for i in range(1, n-5):
        for j in range(i + 2, n - 3):
            for k in range(j + 2, n - 1):
                s1 = prefix_sum[i-1]
                s2 = prefix_sum[j-1] - prefix_sum[i]
                s3 = prefix_sum[k-1] - prefix_sum[j]
                s4 = prefix_sum[n-1] - prefix_sum[k]
                if s1 == s2 == s3 == s4:
                    return True
    return False
