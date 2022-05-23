""" Given a set of candidate numbers (candidates) (without duplicates) and a target number (target), find all unique
combinations in candidates where the candidate numbers sums to target.
The same repeated number may be chosen from candidates unlimited number of times.
Note:
All numbers (including target) will be positive integers.
The solution set must not contain duplicate combinations. """

import unittest2 as unittest


def combination_sum_v1(candidates, target):
    """ Backtracking is a general algorithm for finding all (or some) solutions to some computational problems. The idea
         is that it incrementally builds candidates to the solutions, and abandons a candidate ("backtracks") as soon
         as it determines that this candidate cannot lead to a final solution.

         Specifically, to our problem, we could incrementally build the combination, and once we find the current
         combination is not valid, we backtrack and try another option.

        An important detail on choosing the next number for the combination is that we select the candidates in order,
        where the total candidates are treated as a list. Once a candidate is added into the current combination, we
        will not look back to all the previous candidates in the next explorations.

        To demonstrate the idea, let us consider the example of candidates = [3, 4, 5], target = 8, and zoom in a node
        to see how we can choose the next numbers.

        When we are at the node of [4], the precedent candidates are [3], and the candidates followed are [4, 5].
        We don't add the precedent numbers into the current node, since they would have been explored in the nodes in
        the left part of the subtree, i.e. the node of [3].

        Even though we have already the element 4 in the current combination, we are giving the element another chance
        in the next exploration, since the combination can contain duplicate numbers.

        As a result, we would branch out in two directions, by adding the element 4 and 5 respectively into the current
        combination.

        We define a recursive function dfs(index, combination, remaining), which populates the combinations, starting
        from the current combination (combination), the remaining sum to fulfill (remaining) and the current cursor
        (index) to the list of candidates.

        For the first base case of the recursive function, if remaining==0, i.e. we fulfilled the desired target sum,
        therefore we can add the current combination to the final list.
        As another base case, if remaining < 0, i.e. we exceed the target value, we will cease the exploration here.

        Other than the above two base cases, we would then continue to explore the sublist of candidates as
        [index ... n]. For each of the candidate, we invoke the recursive function itself with updated parameters.

            - Specifically, we add the current candidate into the combination.
            - With the added candidate, we now have less sum to fulfill, i.e. remaining - candidate.
            - For the next exploration, still we start from the current cursor start.

    Time complexity: O(#candidates ^ (target/m)), where m is the minimal value among the candidates. The total number
    of steps during the backtracking would be the number of nodes in the execution tree. The fan-out of each node would
    be bounded to the total number of candidates (number of choices). The maximal depth of the tree would be (target/m),
    where we keep on adding the smallest candidate to the combination. Note that the actual number of nodes in the
    execution tree would be much smaller than the upper bound, since the fan-out of the nodes are decreasing level by
    level.
    Space complexity: O(target/m), for the call stack. The number of recursive calls can pile up to (target/m), where
    we keep on adding the smallest element to the combination
    """

    def dfs(index, combination, remaining):
        # This function call populates the combinations, starting from the current combination 'combination', the
        # remaining sum to fulfill 'remaining', and the current cursor 'index' to the list of candidates.
        if remaining < 0:  # There is no use in exploring a combination that sums beyond target
            return
        if remaining == 0:
            res.append(combination)
            return
        for i in range(index, n):
            # We include 'index' because we're allowed to choose the same number multiple times.
            # We are giving the element another chance in the next exploration, since the combination can contain
            # duplicate numbers.
            # With each iteration of the for loop, we will reduce the number of candidates. This is important to prevent
            # duplicates.
            dfs(i, combination + [candidates[i]], remaining - candidates[i])

    n, res = len(candidates), []
    dfs(0, [], target)
    return res


def combination_sum_v2(candidates, target):
    """ The solution can be optimized by sorting the input array. The only help with sorting is that we can stop
        searching earlier by breaking from the for loop when candidate is larger than 'remaining' target.

        Sorting is not for correctness but for speed. What we do by sorting is we limit the range of numbers on which
        we call DFS recursively, as we know the numbers outside the range cannot be in our solution. For small inputs,
        this speed up may not be substantial. For larger inputs, sorting will definitely give a faster solution.

    Time complexity: O(#candidates ^ (target/m)), where m is the minimal value among the candidates. The largest number
    of elements in a combination sum would be [min(candidates), min(candidates), min(candidates) ...] (think when
    candidates = [1, 2, 3] and target = 1000), and to get the upper bound, we can say that for each element in the max
    length combination array, we can pick from any of the elements we are given.
    Space complexity: O(target/m), for call stack
    """

    def dfs(index, combination, remaining):
        if remaining == 0:
            res.append(combination)
            return
        for i in range(index, n):
            if candidates[i] > remaining:  # If one 'candidate' in bigger than 'remaining', the remaining items must
                # be bigger than 'remaining', so break early. No use exploring a combination that sums beyond 'target'.
                break
            dfs(i, combination + [candidates[i]], remaining - candidates[i])

    n, res = len(candidates), []
    candidates.sort()
    dfs(0, [], target)
    return res


def combination_sum_v3(candidates, target):
    """ This solution uses a clear backtracking template: Add current candidate to the path, explore, and finally
         backtrack.

    Time complexity: O(#candidates ^ (target/m))
    Space complexity: O(target/m), for call stack
    """

    def dfs(index, remaining):
        if remaining == 0:
            res.append(combination[:])  # This is the difference: We append a copy of the path as it is shared amongst
            # the recursive calls
            return
        if remaining < 0:  # There is no use in exploring a combination that sums beyond target
            return
        for i in range(index, n):  # We include 'index' because we're allowed to choose the same number multiple times
            combination.append(candidates[i])  # Add current candidate to the path
            dfs(i, remaining - candidates[i])  # Explore
            combination.pop()  # Backtrack

    n, res, combination = len(candidates), [], []
    dfs(0, target)
    return res


class Test(unittest.TestCase):
    data = [([2, 3, 6, 7], 7, [[7], [2, 2, 3]]), ([2, 3, 5], 8, [[2, 2, 2, 2], [2, 3, 3], [3, 5]])]

    def test_combination_sum(self):
        for test_candidates, test_target, result in self.data:
            self.assertEqual(sorted(result), combination_sum_v1(test_candidates, test_target))
            self.assertEqual(sorted(result), combination_sum_v2(test_candidates, test_target))
            self.assertEqual(sorted(result), combination_sum_v3(test_candidates, test_target))


if __name__ == '__main__':
    unittest.main()
