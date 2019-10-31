""" Given an array of integers nums and a positive integer k, find whether it's possible to divide this array into k
non-empty subsets whose sums are all equal. """

import unittest2 as unittest


def can_partition_k_subsets_v1(nums, k):
    """ Assume sum is the sum of nums[] . The DFS/backtracking process is to find a subset of nums[] which sum equals
        to target = sum/k. We use an array used[] to record which element in nums[] is used. Each time when we get a
        cur_sum = target, we will start from position 0 in nums[] to look up the elements that are not used yet and
        find another cur_sum = target. We exhaustively try all the possible combinations.
    Time complexity: not trivial to calculate
    Space complexity: O(N) for call stack and 'used' array, where N is the length of nums
    """
    def helper(index, k, cur_sum, target):
        if k == 1:  # If we have filled all (k - 1) subsets/buckets up to this point and we are now on our last subset,
            # we can stop and be finished.
            return True
        if cur_sum == target:
            return helper(0, k - 1, 0, target)  # Subset full. continue the recursion with (k - 1) as the new k value,
            # BUT the target stays the same. We just have 1 less subset to fill.
        for i in range(index, n):
            if not used[i] and cur_sum + nums[i] <= target:  # Try all values from 'index' to the end of array ONLY if:
                # 1- They have not been used up to this point in the recursion's path
                # 2- They do not overflow  the current subset/bucket we are filling
                used[i] = True
                if helper(i + 1, k, cur_sum + nums[i], target):  # See if we can partition from this point with the
                    # item added to the current subset progress
                    return True
                used[i] = False  # This is where we backtrack and drop the previous choice of nums[i]
        return False

    total = sum(nums)
    if total % k != 0:
        return False
    target = total // k
    used, n = [False for _ in range(len(nums))], len(nums)
    return helper(0, k, 0, target)


def can_partition_k_subsets_v2(nums, k):
    """ Put n items into k buckets so each bucket has same total item value. For each item, try all possible destined
        buckets.
    Time complexity: O(k^n), because for each bucket, we have to check whether one specific subset of the nums array
    can be put into it
    Space complexity: TODO
    """

    def dfs(index):
        if index == n:  # All items in bucket, no overflow
            return True
        for i in range(k):
            bucket[i] += nums[index]
            if bucket[i] <= target and dfs(index + 1):  # No overflow in bucket, so move on to next item
                return True
            bucket[i] -= nums[index]  # No solution, wrong bucket. Take item out
            if bucket[i] == 0:  # No need to try other empty bucket. This line means that we tried to insert an
                # element in this bucket and moved on to the next elements and they did not match. So we remove this
                # element from this bucket in order to try other combinations. But if we tried to put the biggest
                # number in an empty bucket and it did not fit, whats the point to try another smallest items? We
                # will have to fit the biggest in another bucket but we already tried the best bucket which is the
                # empty one. So if by putting nums[index] in this empty bucket can't solve the game, putting nums[index]
                # on other empty buckets can't solve the game either.
                # Without this check, we are actually making each bucket unique.
                # However, it doesn't make sense because all buckets have the same size and they are the same.
                # If a single number couldn't fit into one bucket, it is a waste of time to put it into the other
                # bucket.
                break
        return False

    nums.sort(reverse=True)  # Starting with bigger values makes it faster. Always start from big numbers for this
    # kind of problems. Just by doing it yourself for a few times you will find out that the big numbers are the
    # easiest to place.
    total = sum(nums)
    if total % k != 0:
        return False
    target, n = total // k, len(nums)
    bucket = [0] * k
    return dfs(0)


class Test(unittest.TestCase):
    data = [([4, 3, 2, 3, 5, 2, 1], 4, True)]

    def test_can_partition_k_subsets(self):
        for test_nums, test_k, result in self.data:
            self.assertEqual(result, can_partition_k_subsets_v1(test_nums, test_k))
            self.assertEqual(result, can_partition_k_subsets_v2(test_nums, test_k))


if __name__ == '__main__':
    unittest.main()
