""" Given an integer array nums, find the sum of the elements between indices i and j (i ≤ j), inclusive. """


class NumArray:
    """ Imagine that sum_range is called one thousand times with the exact same arguments. How could we speed that up?
        We could trade in extra space for speed by pre-computing the cumulative sum from index 0 to k. Could we use
        this information to derive Sum(i, j)?
        We can calculate sum_range as following:
            sum_range(i,j) = sum[j] − sum[i-1]
    Time complexity: O(1) time per query, O(N) time pre-computation
    Space complexity: O(N)
    """

    def __init__(self, nums):
        self.memo = []
        n, acc = len(nums), 0
        for i in range(n):
            acc += nums[i]
            self.memo.append(acc)

    def sum_range(self, i: int, j: int) -> int:
        if i == 0:
            return self.memo[j]
        return self.memo[j] - self.memo[i-1]
