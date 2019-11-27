""" Given a set of candidate numbers (candidates) (without duplicates) and a target number (target), find all unique
combinations in candidates where the candidate numbers sums to target.
The same repeated number may be chosen from candidates unlimited number of times.
Note:
All numbers (including target) will be positive integers.
The solution set must not contain duplicate combinations. """

import unittest2 as unittest


def combination_sum_v1(candidates, target):
    """ Explore all the possible paths that reduce the target to 0, passing an index parameter to DFS call to indicate
        where to start adding candidates. At every step that is taken to complete a path, only elements explored from
        that point onwards are considered. As a result, extending the path always involves adding a larger or equal
        number to what was previously present. That is why it stays unique.
    Time complexity: O(#candidates ^ target)
    Space complexity: Space complexity: O(target) for call stack
    """

    def dfs(index, path, remaining):
        if remaining == 0:
            res.append(path)
            return
        for i in range(index, n):  # We include 'index' because we're allowed to choose the same number multiple times
            if candidates[i] <= remaining:  # There is no use in exploring a combination that sums to beyond target
                dfs(i, path + [candidates[i]], remaining - candidates[i])

    n, res = len(candidates), []
    dfs(0, [], target)
    return res


def combination_sum_v2(candidates, target):
    """ Same as above, but after sorting the input array. The only help with sorting is that we can stop searching 
        earlier by breaking the for loop when candidate is larger than 'remaining' target.
        Sorting is not for correctness but for speed. What we do by sorting is we limit the range of numbers on which
        we call DFS recursively, as we know the numbers outside the range cannot be in our solution. For small inputs
        this speed up may not be substantial but for larger inputs, sorting will definitely give a faster solution.
    Time complexity: O(#candidates ^ (target/min(candidates))), the largest number of elements in a combination sum
    would be [min(candidates), min(candidates), min(candidates) ...] (think when candidates = [1, 2, 3] and
    target = 1000), and to get the upper bound, we can say that for each element in the max length combination array,
    we can pick from any of the elements we are given.
    Space complexity: Space complexity: O(target) for call stack
    """

    def dfs(index, path, remaining):
        if remaining == 0:
            res.append(path)
            return
        for i in range(index, n):
            if candidates[i] > remaining:  # If one 'candidate' in bigger than 'remaining', the remaining items must
                # bigger than 'remaining', so break early
                break
            dfs(i, path + [candidates[i]], remaining - candidates[i])

    n, res = len(candidates), []
    candidates.sort()
    dfs(0, [], target)
    return res


class Test(unittest.TestCase):
    data = [([2, 3, 6, 7], 7, [[7], [2, 2, 3]]), ([2, 3, 5], 8, [[2, 2, 2, 2], [2, 3, 3], [3, 5]])]

    def test_combination_sum(self):
        for test_candidates, test_target, result in self.data:
            self.assertEqual(sorted(result), combination_sum_v1(test_candidates, test_target))
            self.assertEqual(sorted(result), combination_sum_v2(test_candidates, test_target))


if __name__ == '__main__':
    unittest.main()
