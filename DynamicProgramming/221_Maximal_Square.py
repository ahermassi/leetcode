""" Given a 2D binary matrix filled with 0's and 1's, find the largest square containing only 1's and return its
area. """

from collections import defaultdict
import unittest2 as unittest


# For full details, check out this article: https://leetcode.com/articles/maximal-square/
# Video explanation: https://youtu.be/6X7Ha2PrDmM
def maximal_square_v1(matrix):
    """ Top-Down Dynamic Programming.

         At first sight, this problem requires a DFS traversal - a dead giveaway that we need recursion. And it also
         wants us to find the largest square. So we'd go to the first 1 and ask it, "Hey, what's the largest square of
         1s that begins with you?". To calculate that it needs to know the largest squares its ADJACENT cells can begin.
         So, it'll ask the same question to its adjacent cells which will in turn will ask their adjacent cells and so
         on... The cell that began the question will deduce that the largest square that begins with it is:

                1 + the minimum of all the values its adjacent cells returned

         We then ask the same question to every 1 we find in the grid and keep track of the global maximum. In doing
         so, we notice that the recursion causes many cells to be asked the same question again and again
         (overlapping sub-problems)- so we use memoization.

         Let dfs(i, j) be the maximal SIDE LENGTH of the square whose top-left corner is (i, j).

         Base case: when we go out of boundaries, return 0.

         Since the current cell is the top-left corner, we recursively examine the remaining 3 corners,
         mainly bottom left (i + 1, j), top right (i, j + 1), and bottom right (i + 1, j + 1). The result is the
         minimum of the maximal side length that each corner contributes with plus 1.
         So we go to the first 1 and ask it, 'Hey, what's the largest square of 1s that begins with you?'.

    Time complexity: O((N * M)^2), in worst case we need to traverse the complete matrix for every cell equal to 1
    Space complexity: O(N * M)
    """

    def dfs(i, j):
        if not 0 <= i < n or not 0 <= j < m:
            return 0
        if matrix[i][j] == '0':
            return 0
        if (i, j) in memo:
            return memo[(i, j)]
        down = dfs(i + 1, j)
        right = dfs(i, j + 1)
        diagonal = dfs(i + 1, j + 1)
        memo[(i, j)] = 1 + min(down, right, diagonal)
        return memo[(i, j)]

    n, m, memo = len(matrix), len(matrix[0]), defaultdict(int)
    max_square_side = 0
    for i in range(n):
        for j in range(m):
            max_square_side = max(max_square_side, dfs(i, j))
    return max_square_side * max_square_side


def maximal_square_v2(matrix):
    """ Bottom-Up Dynamic Programming.

        We initialize a 2D matrix dp with the same dimensions as the original one initialized with all 0’s.
        Let dp[i, j] be the side length of the maximal square whose bottom-right corner is the cell at index (i,j)
        in the original matrix.

        Since the current cell is the bottom-right corner, we recursively examine the remaining 3 corners,
         mainly top right (i -1, j), bottom left (i, j -1 1), and top left (i -1, j - 1). The result is the
         minimum of the maximal side length that each corner contributes with plus 1.

        Starting from index (0,0), for every 1 found in the original matrix, we update the value of the current element
        as:
                    dp[i, j] = min(dp[i−1, j], dp[i, j−1], dp[i−1, j−1]) + 1

        We use min() because that is what limits the size of the square. If for example any corner was a 0, we know we
        don't have that row or column to form the bigger square at (i,j).

        Logic : Top right, bottom left, and top left decide the size of the square. If all of them are same, then the
        size of square increases by 1. If they're not same, they can increase by 1 to the minimal square.

    Time complexity: O(N * M)
    Space complexity: O(N * M)
    """
    n, m = len(matrix), len(matrix[0])
    dp, max_square_side = [[0] * m for _ in range(n)], 0
    for i in range(n):
        for j in range(m):
            if matrix[i][j] == '1':
                dp[i][j] = min(dp[i - 1][j], dp[i][j - 1], dp[i - 1][j - 1]) + 1
                max_square_side = max(max_square_side, dp[i][j])
    return max_square_side * max_square_side


def maximal_square_v3(matrix):
    """ Space-optimized Bottom-Up Dynamic Programming.

         In the previous, to calculate dp of the ith row, we used only the previous element and the (i−1)th
         row. Therefore, we don't need 2D dp matrix as 1D dp array will be sufficient for this.

         Initially, the dp array contains all 0's. As we scan the elements of the original matrix across a row, we keep
         updating the dp array as per the equation:
                    dp[j] = min(dp[j-1], dp[j], pre)

         where pre refers to the old dp[j-1] of the previous row. For every row, we repeat the same process and update
         in the same dp array.

    Time complexity: O(N * M)
    Space complexity: O(M)
    """
    n, m = len(matrix), len(matrix[0])
    cur, pre = [0] * m, 0
    max_len = 0
    for i in range(n):
        for j in range(m):
            if matrix[i][j] == '1':
                if i == 0 or j == 0:
                    cur[j], pre = 1, cur[j]
                else:
                    cur[j], pre = min(cur[j], cur[j-1], pre) + 1, cur[j]
                max_len = max(max_len, cur[j])
            else:
                cur[j] = 0
    return max_len * max_len


class Test(unittest.TestCase):
    data = [([['1', '0', '1', '0', '0'], ['1', '0', '1', '1', '1'], ['1', '1', '1', '1', '1'],
              ['1', '0', '0', '1', '0']], 4)]

    def test_maximal_square(self):
        for test_matrix, result in self.data:
            self.assertEqual(result, maximal_square_v1(test_matrix))
            self.assertEqual(result, maximal_square_v2(test_matrix))
            self.assertEqual(result, maximal_square_v3(test_matrix))


if __name__ == '__main__':
    unittest.main()
