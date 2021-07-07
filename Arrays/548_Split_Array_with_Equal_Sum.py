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
    Time complexity: O(n^4)
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
