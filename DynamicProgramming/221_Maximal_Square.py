''' Given a 2D binary matrix filled with 0's and 1's, find the largest square containing only 1's and return its
area. '''

import unittest2 as unittest


# For full details, check out this article: https://leetcode.com/articles/maximal-square/


def maximal_square_v1(matrix):
    """ Top down, recursive solution with memoization.
        dfs(i, j) returns the maximal side length of the square whose bottom right corner is (i, j).
        Base case: each square whose bottom right is at first row/column has only 1 element. So if matrix[i][j] == c,
        then dfs(i, j) = c, where c is in {0, 1}.
        After that, since the current cell is the bottom right corner, we recursively examine the remaining 3 corners,
        mainly top right (i - 1, j), bottom left (i, j - 1), and top left (i - 1, j - 1). The result is the minimum of
        the maximal side length that each corner contributes with plus 1.
    Time complexity: O((N * M)^2), in worst case we need to traverse the complete matrix for every cell equal to 1
    Space complexity: O(N * M)
    """
    def dfs(i, j):
        if matrix[i][j] == '0':
            return 0
        if (i, j) not in memo:
            memo[(i, j)] = min(dfs(i - 1, j), dfs(i, j - 1), dfs(i - 1, j - 1)) + 1
        return memo[(i, j)]

    if not matrix:
        return 0
    n, m, memo = len(matrix), len(matrix[0]), {}
    for j in range(m):
        memo[(0, j)] = int(matrix[0][j])
    for i in range(n):
        memo[(i, 0)] = int(matrix[i][0])
    res = 0
    for i in range(n):
        for j in range(m):
            res = max(res, dfs(i, j))
    return res * res


def maximal_square_v2(matrix):
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
            if i == 0 or j == 0:  # First row and first column are not changed as each square whose bottom right is
                # at first row/column has only 1 element. So if matrix[i][j] == c --> dp[i][j] = c; c in {0, 1}
                dp[i][j] = int(matrix[i][j])
            elif matrix[i][j] == '1':
                dp[i][j] = min(dp[i - 1][j],dp[i][j - 1], dp[i - 1][j - 1]) + 1  # min(top, left, top-left/diagonal) + 1
                max_len = max(max_len, dp[i][j])
    return max_len * max_len

# Review the following code. There is a bug somewhere.


def maximal_square_v3(matrix):
    """ In the previous approach for calculating dp of ith row, we are using only the previous element and the (i−1)th
        row. Therefore, we don't need 2D dp matrix as 1D dp array will be sufficient for this.
        Initially, the dp array contains all 0's. As we scan the elements of the original matrix across a row, we keep
        on updating the dp array as per the equation:
            dp[j] = min(dp[j-1],dp[j],prev)
        where prev refers to the old dp[j-1]. For every row, we repeat the same process and update in the same dp array.
    Time complexity: O(N * M)
    Space complexity: O(M)
    """
    if not matrix:
        return 0
    n, m = len(matrix), len(matrix[0])
    dp, max_len = [0] * m, 0
    prev = 0
    for i in range(1, n):
        for j in range(1, m):
            temp = dp[j]
            if matrix[i][j] == '1':
                dp[j] = min(dp[j], dp[j - 1], prev) + 1
                max_len = max(max_len, dp[j])
            prev = temp
    return max_len * max_len


class Test(unittest.TestCase):
    data = [([['1', '0', '1', '0', '0'], ['1', '0', '1', '1', '1'], ['1', '1', '1', '1', '1'],
              ['1', '0', '0', '1', '0']], 4)]

    def test_maximal_square(self):
        for test_matrix, result in self.data:
            self.assertEqual(result, maximal_square_v1(test_matrix))
            self.assertEqual(result, maximal_square_v2(test_matrix))


if __name__ == '__main__':
    unittest.main()
