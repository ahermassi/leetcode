""" Given a set of distinct integers, nums, return all possible subsets (the power set).
Note: The solution set must not contain duplicate subsets. """

import unittest2 as unittest


def subsets_v1(nums):
    """ While iterating through all numbers, for each new number, we can either pick it or not pick it.
            1- If pick, just add current number to every existing subset.
            2- If not pick, just leave all existing subsets as they are.
        We just combine both into our result.
        Here's an example to help understand the code:
        The set to iterate over/generate the power set for: input_set = [1, 2, 3]
        Subset initially only has the empty set (empty list), []
        In each iteration, concatenate each element/list in subset with the list[n], then extend the results into
        subset.
            subset = [[]]
            element -> subset list after each iteration
            num = 1 -> [[], [1]]
            num = 2 -> [[], [1], [2], [1, 2]]
            num = 3 -> [[], [1], [2], [1, 2], [3], [1, 3], [2, 3], [1, 2, 3]]
    Time complexity: O(2^N)
    Space complexity: O(1)
    """
    res = [[]]
    for num in nums:
        temp = []
        for l in res:
            temp.append(l + [num])
        res.extend(temp)
    return res


def subsets_v2(nums):
    """ DFS recursively. At each index i, add the current element to the current subset, recursively find the subsets
        that include nums[i], and finally retract nums[i] from the current subset to explore other possibilities.
    Time complexity: O(N * 2^N), here are 2^N subsets to generate and each one takes O(N) time to copy into 'res'
    Space complexity: O(N), for call stack
    """

    def compute_subsets_at_index(index, subset):
        res.append(subset)
        for i in range(index, n):
            compute_subsets_at_index(i + 1, subset + [nums[i]])  # Finding all subsets that include nums[i]

    n, res = len(nums), []
    compute_subsets_at_index(0, [])
    return res


def subsets_v3(nums):
    """ This solution uses a clear backtracking template: add current candidate to the path, explore, and finally
        backtrack.
    Time complexity: O(N * 2^N)
    Space complexity: O(N), for call stack
    """

    def compute_subsets_at_index(index):
        res.append(path[:])
        for i in range(index, n):
            path.append(nums[i])  # Finding all subsets that include nums[i]. Add current candidate to the path
            compute_subsets_at_index(i + 1)  # Explore
            path.pop()  # Backtrack. Remove nums[i] from the present subset and move further to explore subsets that
            # don't contain nums[i]

    n, path, res = len(nums), [], []
    compute_subsets_at_index(0)
    return res


def subsets_v4(nums):
    """ The idea of this solution originated from Donald E. Knuth.
        We map each subset to a bitmask of length n, where 1 on the ith position in bitmask means the presence of
        nums[i] in the subset, and 0 means its absence.
        For instance, the bitmask 0..00 (all zeros) corresponds to an empty subset, and the bitmask 1..11 (all ones)
        corresponds to the entire input array nums.
        Hence, to solve the initial problem, we just need to generate 2^n bitmasks from 0..00 to 1..11.
    Time complexity: O(2^N)
    Space complexity: O(1)
    """
    n = len(nums)
    p = 1 << n  # p = 2^n
    res = [[] for _ in range(p)]
    for i in range(p):
        for j in range(n):
            if (i >> j) & 1:
                res[i].append(nums[j])
    return res


class Test(unittest.TestCase):
    data = [([1, 2, 3], [[], [1], [1, 2], [1, 2, 3], [1, 3], [2], [2, 3], [3]])]

    def test_subsets(self):
        for test_array, result in self.data:
            self.assertEqual(result, sorted(subsets_v1(test_array)))
            self.assertEqual(result, sorted(subsets_v2(test_array)))
            self.assertEqual(result, sorted(subsets_v3(test_array)))
            self.assertEqual(result, sorted(subsets_v4(test_array)))


if __name__ == '__main__':
    unittest.main()
