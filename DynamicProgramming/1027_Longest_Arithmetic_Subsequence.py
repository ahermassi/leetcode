""" Given an array nums of integers, return the length of the longest arithmetic subsequence in nums.

Recall that a subsequence of an array nums is a list nums[i1], nums[i2], ..., nums[ik] with
0 <= i1 < i2 < ... < ik <= nums.length - 1, and that a sequence seq is arithmetic if seq[i+1] - seq[i] are all the same
value (for 0 <= i < seq.length - 1). """

from collections import defaultdict


def longest_arith_seq_length_v1(nums):
    """ The main idea is to maintain a map of arithmetic differences seen at each index.
        We iteratively build the map for a new index i by considering all elements to the left one by one.
        For each pair of indices (i,j) and difference d = nums[i] - nums[j], we check if there was an existing chain at
        the index j with arithmetic difference d already. If yes, we can then extend the existing chain length by 1.
        Otherwise, we can start a new chain of length 2 with this new difference d and (nums[j], nums[i]) as its
        elements. At the end, we can then return the maximum chain length that we have seen so far.
        This problem is similar to 300- Longest Increasing Subsequence. The difference is that we need to consider the
        arithmetic difference in this problem. How to keep track of the length as well as the difference? We can use a
        hash map, whose key is the difference and value is the length.
        For two elements nums[i] and nums[j] where j < i, the difference between nums[i] and nums[j] (call it 'diff')
        is critical. If the hash map at position j has the key 'diff', it means that there is an arithmetic subsequence
        ending at index j with arithmetic difference 'diff' and length map[j][diff]. We just extend its length by 1.
        If the hash map does not have the key 'diff', then those two elements can start a 2-length arithmetic
        subsequence.
        Example : nums = [3, 6, 9, 12]
        Store diffs found at each index, then add to previously found difference and calculate max.
        i = 0 -> {{}}
        i = 1 -> {{3,2}},  max = 2
        i = 2 -> {{6,2}, {3,3}} (adding 2 to previous)},  max = 3
        i = 3 -> {{9,2}, {6,2} , {3,4} (adding 3 from previous)},  max = 4
    Time complexity: O(N^2)
    Space complexity: O(N^2)
    """
    n = len(nums)
    # The map for each index i maintains elements of the form:
    # (arithmetic difference, length of max chain ending at i with that difference)
    # So longest_arithmetic_seq_at_index[i][diff] is equal to the longest arithmetic subsequence up to index i that
    # has common difference 'diff'.
    longest_arithmetic_seq_at_index = [defaultdict(int) for _ in range(n)]
    max_len = 1
    for i in range(n):
        for j in range(i):
            difference = nums[i] - nums[j]
            if not longest_arithmetic_seq_at_index[j][difference]:
                longest_arithmetic_seq_at_index[i][difference] = 2
            else:
                # If we had already seen an arithmetic difference 'difference' at index j, then we can potentially add
                # nums[i] to the same chain and extend its length at i by 1.
                longest_arithmetic_seq_at_index[i][difference] = longest_arithmetic_seq_at_index[j][difference] + 1
            max_len = max(max_len, longest_arithmetic_seq_at_index[i][difference])
    return max_len


def longest_arith_seq_length_v2(nums):
    """ Same solution using an array of arrays instead of an array of dictionaries.
        Note that the arithmetic common difference could be negative, therefore we offset the difference by its maximum
        value to ensure we would never have a negative index in our tabulation. According to the problem statement,
        0 <= nums[i] <= 500, so the lower bound of difference is (0 - 500 = -500), and its upper bound is
        (500 - 0 = 500). By offsetting, they become 0 and 1000, respectively. That's why each list is indexed up to
        1001.
    Time complexity: O(N^2)
    Space complexity: O(N^2)
    """
    n = len(nums)
    longest_arithmetic_seq_at_index = [[1] * 1001 for _ in range(n)]
    max_len = 1
    for i in range(n):
        for j in range(i):
            difference = nums[i] - nums[j] + 500
            longest_arithmetic_seq_at_index[i][difference] = longest_arithmetic_seq_at_index[j][difference] + 1
            max_len = max(max_len, longest_arithmetic_seq_at_index[i][difference])
    return max_len
