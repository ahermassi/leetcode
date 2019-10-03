""" Given a collection of distinct integers, return all possible permutations. """

import unittest2 as unittest


def permute_v1(nums):
    """ Here is a backtrack function which takes the index of the first integer to consider as an argument backtrack(first).
        If the first integer to consider has index n that means that the current permutation is done.
        Iterate over the integers from index first to index n - 1.
            Place i-th integer first in the permutation, i.e. swap(nums[first], nums[i]).
            Proceed to create all permutations which starts from i-th integer : backtrack(first + 1).
            Now backtrack, i.e. swap(nums[first], nums[i]) back.
    Time complexity: O(N * N!), because we generate N! permutations and each permutation requires O(N) to copy into res
    Space complexity: O(N) for the recursive call stack (max depth of call tree)
    """

    def backtrack(start):
        if start == n:
            res.append(nums[:])
        for i in range(start, n):
            nums[start], nums[i] = nums[i], nums[start]
            backtrack(start + 1)
            nums[start], nums[i] = nums[i], nums[start]  # Second swap: backtracking. Think of it as moving back up
            # in the tree to explore the next branch. When we moved down of one level, we swapped 2 elements (1st
            # swap in the code). So when we go back up in the tree we need to swap these 2 elements back to their
            # original order at the parent node level (2nd swap in the code). This is called backtracking = done
            # exploring a branch, let's go back up and explore more branches.

    n, res = len(nums), []
    backtrack(0)
    return res

