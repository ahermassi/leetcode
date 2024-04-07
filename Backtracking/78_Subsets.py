""" Given a set of distinct integers, nums, return all possible subsets (the power set).
Note: The solution set must not contain duplicate subsets. """

import unittest2 as unittest


def subsets_v1(nums):
    """ Let's start from an output list with an empty subset. While iterating over the numbers, for each number, we can
         either pick it or not pick it.

             1- If picked, add the current number to every existing subset

             2- If not picked, leave all existing subsets unchanged

         We then combine both into the result.

         Here's an example to help understand the code. The list of numbers to generate the power set for is [1, 2, 3].
         The power set initially has only the empty subset (empty list), [].
         In each iteration, append the current number to each previously generated subset, then extend the power set.

            all_subsets = [[]]
            number      ->      all_subsets after each iteration
            num = 1    ->      [[], [1]]
            num = 2    ->      [[], [1], [2], [1, 2]]
            num = 3    ->      [[], [1], [2], [1, 2], [3], [1, 3], [2, 3], [1, 2, 3]]

         The solution comes from the observation that the subsets are 'nested', meaning it is easy to construct a subset
         of n numbers if we already have the subsets of the first (n - 1) numbers, where the base case for n=0 is the
         empty subset S = {}. Then we can obtain S_n from S_(n-1) in the following way:

                    S_n = {S_(n-1), S_(n-1) + n)}

         (S_(n-1) + n) is obtained by appending n to each element in S_(n-1).
         For example, S_(1) = {{}, {1}}, then S_(2) = {S_(1), S_(1) + 2} = {S_(1), {2}, {1,2}} = {{}, {1}, {2}, {1,2}}.

    Time complexity: O(N * 2^N), to generate all subsets and then copy them into output list
    Space complexity: O(N * 2^N)
    """
    power_set = [[]]
    for num in nums:
        subsets = []
        for subset in power_set:
            subsets.append(subset + [num])
        power_set.extend(subsets)
    return power_set


def subsets_v2(nums):
    """ Backtracking.

         The power set is the set of all possible combinations of all possible lengths, from 0 to n.
         Given this definition, the problem can also be interpreted as finding the power set from a sequence.

         At each index i, add the current number nums[i] to the current subset/path, recursively find the other subsets
         that contain nums[i], then finally retract nums[i] from the current path to explore other possibilities.

         We define a backtracking function compute_subsets_at_index(index, subset) which takes the index of the current
         number and the subset that's being created.

             - Add the current subset to the final output

              - Iterate over all the indices from 'index' to the length of the entire sequence n. At each index i:

                  * Add nums[i] to the current subset
                  * Proceed recursively to add more numbers to the subset : compute_subsets_at_index(i + 1, subset).
                  * Backtrack by removing nums[i] from the subset

        Example: nums = [1, 2, 3]
        compute_subsets_at_index(index = 0, subset = []), res = []
        |
        |__ compute_subsets_at_index(index = 1 , subset = [1]),                       res = [[]]
        |    |__ compute_subsets_at_index(index = 2 , subset = [1,2]),               res = [[],[1]]
        |    |    |__ compute_subsets_at_index(index = 3, subset = [1,2,3]),        res = [[],[1],[1,2]]
        |    |                                                                                                        res = [[],[1],[1,2],[1,2,3]]
        |    |         // for loop will not be executed because index=n=3
        |    |
        |    |__ compute_subsets_at_index(index = 3 , subset = [1,3]),               res = [[],[1],[1,2],[1,2,3]]
        |    	  	                                                                                                  res = [[],[1],[1,2],[1,2,3],[1,3]]
        |    	  	   // for loop will not be executed because index=n=3
        |
        |__ compute_subsets_at_index(index = 2, subset = [2]),                        res = [[],[1],[1,2],[1,2,3],[1,3]]
        |    |__ compute_subsets_at_index(index = 3 , subset = [2,3]),               res = [[],[1],[1,2],[1,2,3],[1,3],[2]]
        |    	  	                                                                                                  res =  [[],[1],[1,2],[1,2,3],[1,3],[2],[2,3]]
        |    	  	   // for loop will not be executed because index=n=3
        |
        |__ compute_subsets_at_index(index = 3, subset = [3]),                        res =  [[],[1],[1,2],[1,2,3],[1,3],[2],[2,3]]
     	  	                                                                                                          res =  [[],[1],[1,2],[1,2,3],[1,3],[2],[2,3],[3]]
     	  	   // for loop will not be executed because index=n=3

    Time complexity: O(2^N), there are 2^N subsets to generate. The recursive function is called 2^N times, since we
    have 2 choices at each iteration in nums array: either include nums[i] in or exclude it from the current subset.
    Space complexity: O(N), for the call stack
    """

    def compute_subsets_at_index(index, subset):
        res.append(subset)
        for i in range(index, n):
            # Find all subsets that contain nums[i] and the rest of the numbers
            compute_subsets_at_index(i + 1, subset + [nums[i]])

    n, res = len(nums), []
    compute_subsets_at_index(0, [])
    return res


def subsets_v3(nums):
    """ This solution uses an explicit backtracking template: Add the current number to the path, explore, and finally
         backtrack. Notice that we reuse the same path/subset for all recursive calls.

    Time complexity: O(N * 2^N), there are 2^N subsets to generate and each one takes O(N) time to copy to the output.
    The recursive function is called 2^N times. Because we have 2 choices at each iteration in nums array: either
    include nums[i] in or exclude it from the current subset. We need to create a copy of the current subset because we
    reuse the original one to build all the valid subsets. This copy costs O(N) and is performed at each call of the
    recursive function, which is called 2^N times. So total time complexity is O(N * 2^N).
    Space complexity: O(N), for the call stack
    """

    def compute_subsets_at_index(index):
        res.append(subset[:])
        for i in range(index, n):
            subset.append(nums[i])  # Find all subsets that contain the current number by adding nums[i] to the subset
            compute_subsets_at_index(i + 1)  # Explore
            subset.pop()  # Backtrack. Explore subsets that don't contain nums[i] by removing nums[i] from the subset

    n, subset, res = len(nums), [], []
    compute_subsets_at_index(0)
    return res


# Video explanation: https://youtu.be/REOH22Xwdkk
def subsets_v4(nums):
    """ Good ol' backtracking without the use of a for loop.

    Time complexity: O(N * 2^N)
    Space complexity: O(N)
    """

    def compute_subsets_at_index(index, subset):
        if index == n:
            res.append(subset)
            return
        compute_subsets_at_index(index + 1, subset + [nums[index]])
        compute_subsets_at_index(index + 1, subset)

    n, res = len(nums), []
    compute_subsets_at_index(0, [])
    return res


def subsets_v5(nums):
    """ The idea of this solution originated from Donald E. Knuth.

         We map each subset to a bitmask of length n, where 1 in the ith position of the bitmask means the presence of
         nums[i] in the subset, and 0 means its absence.

         For instance, the bitmask 0..00 (all zeroes) corresponds to an empty subset, and the bitmask 1..11 (all ones)
         corresponds to the entire input array nums.

         Hence, to generate the power set, we just need to generate 2^n bitmasks from 0..00 to 1..11.

    Time complexity: O(N * 2^N)
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


def subsets_v6(nums):
    """ Simplified version of the previous solution.

    Time complexity: O(N * 2^N)
    Space complexity: O(1)
    """
    n = len(nums)
    p, res = 1 << n, []
    for i in range(p):
        # generate bitmask, from 0..00 to 1..11
        # If i = 3 = 011 -> i|p = 0011|1000 = 0011 -> bin(i|p) = 0b0011 -> bin(i|p)[3:] = 011
        # So each bitmask ends up being the string representation of the binary format of i
        bitmask = bin(i | p)[3:]
        # Map a subset to each bitmask: 1 at the jth position in the bitmask means the presence of nums[j] in the
        # subset, and 0 means its absence.
        res.append([nums[j] for j in range(n) if bitmask[j] == '1'])
    return res
    # Similar to:
    # for i in range(2**n, 2**(n + 1)):
    #     bitmask = bin(i)[3:]


class Test(unittest.TestCase):
    data = [([1, 2, 3], [[], [1], [1, 2], [1, 2, 3], [1, 3], [2], [2, 3], [3]])]

    def test_subsets(self):
        for test_array, result in self.data:
            self.assertEqual(result, sorted(subsets_v1(test_array)))
            self.assertEqual(result, sorted(subsets_v2(test_array)))
            self.assertEqual(result, sorted(subsets_v3(test_array)))
            self.assertEqual(result, sorted(subsets_v4(test_array)))
            self.assertEqual(result, sorted(subsets_v5(test_array)))
            self.assertEqual(result, sorted(subsets_v6(test_array)))


if __name__ == '__main__':
    unittest.main()
