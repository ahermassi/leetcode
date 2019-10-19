''' Given a 2D binary matrix filled with 0's and 1's, find the largest square containing only 1's and return its
area. '''

import unittest2 as unittest


# For full details, check out this article: https://leetcode.com/articles/maximal-square/

def maximal_square_v1(matrix):
    """ We initialize another matrix (dp) with the same dimensions as the original one initialized with all 0’s.
        dp(i,j) represents the side length of the maximum square whose bottom right corner is the cell with index (i,j)
        in the original matrix.
        Starting from index (0,0), for every 1 found in the original matrix, we update the value of the current element
        as:
            dp(i, j)= min(dp(i−1, j), dp(i−1, j−1), dp(i, j−1))+1.
        Logic : Top, Left, and Top Left decides the size of the square. If all of them are same, then the size of
        square increases by 1. If they're not same, they can increase by 1 to the minimal square.
        At first sight, this problem requires a DFS traversal - a dead giveaway that we need recursion. And it also
        wants you to find the largest square. So you'd go to the first 1 and ask it, "Hey, what's the largest square of
        1s that begins with you?". To calculate that it needs to know the largest squares its adjacent cells can begin.
        So, it'll ask the same question to its adjacent cells which will in turn will ask their adjacent cells and so
        on... The cell that began the question will deduce that the largest square that begins with it is 1 + the
        minimum of all the values its adjacent cells returned.
        You'd then ask the same question to every 1 you find in the grid and keep track of the global maximum. In doing
        so, you'll notice that the recursion causes many cells to be asked the same question again and again
        (overlapping sub-problems)- so you'd use memoization.
    Time complexity: O(N * M)
    Space complexity: O(N * M)
    """
    if not matrix:
        return 0
    n, m = len(matrix), len(matrix[0])
    dp, max_len = [[0] * m for _ in range(n)], 0
    for i in range(n):
        for j in range(m):
            if i == 0 or j == 0:
                dp[i][j] = int(matrix[i][j])
            elif matrix[i][j] == '1':
                dp[i][j] = min(dp[i - 1][j - 1], dp[i][j - 1], dp[i - 1][j]) + 1
            max_len = max(max_len, dp[i][j])
    return max_len * max_len


class Test(unittest.TestCase):
    data = [([['1', '0', '1', '0', '0'], ['1', '0', '1', '1', '1'], ['1', '1', '1', '1', '1'],
              ['1', '0', '0', '1', '0']], 4)]

    def test_maximal_square(self):
        for test_matrix, result in self.data:
            self.assertEqual(result, maximal_square_v1(test_matrix))


if __name__ == '__main__':
    unittest.main()
