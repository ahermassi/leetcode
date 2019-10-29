""" Given a string s, find the longest palindromic subsequence's length in s. You may assume that the maximum length
of s is 1000. """

import unittest2 as unittest


def longest_palindrome_subseq_v1(s):
    """ Brute force. TLE
        If the two ends of a string are the same, then they must be included in the longest palindrome sub sequence.
        Otherwise, both ends cannot be included in the longest palindrome sub sequence.
    Time complexity: O(2^N)
    Space complexity: O(N), recursion call stack
    """
    def helper(i, j):
        if i == j:
            return 1
        if i > j:
            return 0
        if s[i] == s[j]:
            return 2 + helper(i + 1, j - 1)
        return max(helper(i + 1, j), helper(i, j - 1))

    n = len(s)
    return helper(0, n - 1)


def longest_palindrome_subseq_v2(s):
    """ Top-down dynamic programming. Improving the brute force with memoization of intermediate calculations. No TLE.
        Without memoization, the time complexity would be O(2^N). This follows from the fact that any recursive
        function's time complexity is O(branches^depth). However, because we are memoizing, we 'prune' the recursive
        tree and do not recurse into/solve the same sub-problem twice. We can prove this by drawing the recursive call
        tree without memoization, we will see that there will be MANY overlapping sub problems. But because we memoize,
        in the worst case, we only need to solve all sub problems ONCE, of which there are an upper bound of N^2 total.
    Time complexity: O(N ** 2)
    Space complexity: O(2 ^ N), recursion call stack and 'memo' hash map
    """
    def helper(i, j):
        if i > j:
            return 0
        if (i, j) in memo:
            return memo[(i, j)]
        if s[i] == s[j]:
            memo[(i + 1, j - 1)] = helper(i + 1, j - 1)
            return 2 + memo[(i + 1, j - 1)]
        memo[(i + 1, j)], memo[(i, j - 1)] = helper(i + 1, j), helper(i, j - 1)
        return max(memo[(i + 1, j)], memo[(i, j - 1)])

    n = len(s)
    memo = {(i, i): 1 for i in range(n)}  # Base case (i == j)
    return helper(0, n - 1)


# Checkout:
# https://leetcode.com/problems/longest-palindromic-subsequence/discuss/216717/Python-DP-solution-w-explanation

def longest_palindrome_subseq_v3(s):
    """ Bottom-up Dynamic Programming.
        Let dp[i][j] be the longest palindromic sub sequence length of substring(i, j).
        State transition:
            dp[i][j] = dp[i+1][j-1] + 2 if s[i] == s[j]
            otherwise, dp[i][j] = Math.max(dp[i+1][j], dp[i][j-1])
            Initialization: dp[i][i] = 1
        We will be considering substrings starting at left and ending at right (inclusive). To do this we iterate over
        all lengths from 1 to n, and within each length iterate over staring (or left) position. The key is that we
        get the answers for a single length at all start positions before going to the next length because the DP
        depends on the answers from shorter lengths. If we do it this way, we will have 3 cases to consider on every
        iteration, pick the one with the highest value:
            The answer from removing the left edge char
            The answer from removing the right edge char
            And if the left and right chars are equal, 2 plus the answer from removing both left and right chars
    Time complexity: O(N ** 2)
    Space complexity: O(N ** 2)
    """
    n = len(s)
    if s == s[::-1]:
        return n
    dp = [[0 for _ in range(n)] for _ in range(n)]
    for i in reversed(range(n)):
        dp[i][i] = 1
        for j in range(i + 1, n):
            if s[i] == s[j]:
                dp[i][j] = dp[i + 1][j - 1] + 2
            else:
                dp[i][j] = max(dp[i + 1][j], dp[i][j - 1])
    return dp[0][n - 1]


class Test(unittest.TestCase):
    data = [('bbbab', 4), ('cbbd', 2)]

    def test_longest_palindrome(self):
        for test_s, result in self.data:
            self.assertEqual(result, longest_palindrome_subseq_v1(test_s))
            self.assertEqual(result, longest_palindrome_subseq_v2(test_s))
            self.assertEqual(result, longest_palindrome_subseq_v3(test_s))


if __name__ == '__main__':
    unittest.main()