""" Given a 2D matrix matrix, find the sum of the elements inside the rectangle defined by its upper left corner
(row1, col1) and lower right corner (row2, col2). """

import unittest2 as unittest


class NumMatrixV1(object):
    """ Brute force. TLE
        Each time sumRegion is called, we use a double for loop to sum all elements from(row1,col1) → (row2,col2).
    Time complexity: O(N * M) per query, where N and M represent the number of rows and columns respectively
    Space complexity: O(1)
    """

    def __init__(self, matrix):
        self.matrix = matrix

    def sumRegion(self, row1, col1, row2, col2):
        res = 0
        for i in range(row1, row2 + 1):
            for j in range(col1, col2 + 1):
                res += self.matrix[i][j]
        return res


class NumMatrixV2(object):
    """ Caching rows.
        Try to see the 2D matrix as N rows of 1D arrays. To find the region sum, we just accumulate the sum in the
        region row by row.
    Time complexity: O(N) per query, O(N * M) for pre-calculation, where N and M represent the number of rows and
    columns respectively
    Space complexity: O(N * M) to store the cumulative sum of all rows
    """

    def __init__(self, matrix):
        if not matrix:
            return
        n, m = len(matrix), len(matrix[0])
        self.dp = [[0 for _ in range(m)] for _ in range(n)]
        for i in range(n):
            self.dp[i][0] = matrix[i][0]
        for i in range(n):
            for j in range(1, m):
                self.dp[i][j] = self.dp[i][j - 1] + matrix[i][j]

    def sumRegion(self, row1, col1, row2, col2):
        dp, res = self.dp, 0
        for i in range(row1, row2 + 1):
            res += self.dp[i][col2] - self.dp[i][col1 - 1] if col1 >= 1 else self.dp[i][col2]
        return res


class NumMatrixV3(object):
    """ Bottom-up dynamic programming.
        We used a cumulative sum array in the previous solution. We notice that the cumulative sum is computed with
        respect to the origin at index 0. Extending this analogy to the 2D case, we could pre-compute a cumulative
        region sum with respect to the origin at (0,0).
        Let dp[i][j] be the preSum of all elements in the rectangle area between (0,0) to (i-1, j-1)
        Notice: we add additional blank row dp[0][col+1]={0} and blank column dp[row+1][0]={0} to remove the edge
        case checking.
        dp[i+1][j+1] represents the sum of area from matrix[0][0] to matrix[i][j]
        Base case: dp[1][1] = matrix[0][0]
        Recurrence relation:
            dp[i][j] = dp[i - 1][j]   +  dp[i][j - 1]    -  dp[i - 1][j - 1]          +  matrix[i - 1][j - 1]
                       Top rectangle  +  left rectangle  -  top left common rectangle +  new value at current point
        To calculate dp, the idea is as below:

        +-----+-+-------+     +--------+-----+     +-----+---------+     +-----+--------+
        |     | |       |     |        |     |     |     |         |     |     |        |
        |     | |       |     |        |     |     |     |         |     |     |        |
        +-----+-+       |     +--------+     |     |     |         |     +-----+        |
        |     | |       |  =  |              |  +  |     |         |  -  |              |
        +-----+-+       |     |              |     +-----+         |     |              |
        |               |     |              |     |               |     |              |
        |               |     |              |     |               |     |              |
        +---------------+     +--------------+     +---------------+     +--------------+

        sums[i][j]      =    sums[i-1][j]    +     sums[i][j-1]    -   sums[i-1][j-1]   +   matrix[i-1][j-1]

        So, we use the same idea to find the specific area's sum:

        +---------------+   +--------------+   +---------------+   +--------------+   +--------------+
        |               |   |         |    |   |   |           |   |         |    |   |   |          |
        |   (r1,c1)     |   |         |    |   |   |           |   |         |    |   |   |          |
        |   +------+    |   |         |    |   |   |           |   +---------+    |   +---+          |
        |   |      |    | = |         |    | - |   |           | - |      (r1,c2) | + |   (r1,c1)    |
        |   |      |    |   |         |    |   |   |           |   |              |   |              |
        |   +------+    |   +---------+    |   +---+           |   |              |   |              |
        |        (r2,c2)|   |       (r2,c2)|   |   (r2,c1)     |   |              |   |              |
        +---------------+   +--------------+   +---------------+   +--------------+   +--------------+

    Time complexity: O(1) time per query, O(N * M) time pre-computation. The pre-computation in the constructor takes
    O(N * M), and each sumRegion query takes O(1)
    Space complexity: O(N * M) to store the cumulative region sum
    """

    def __init__(self, matrix):
        if not matrix:
            return
        n, m = len(matrix), len(matrix[0])
        self.dp = [[0 for _ in range(m+1)] for _ in range(n+1)]
        for i in range(1, n+1):
            for j in range(1, m+1):
                self.dp[i][j] = matrix[i-1][j-1] + self.dp[i-1][j] + self.dp[i][j-1] - self.dp[i-1][j-1]

    def sumRegion(self, row1, col1, row2, col2):
        dp = self.dp
        return dp[row2 + 1][col2 + 1] - dp[row2 + 1][col1] - dp[row1][col2 + 1] + dp[row1][col1]


class Test(unittest.TestCase):
    matrix1 = NumMatrixV1([[3, 0, 1, 4, 2], [5, 6, 3, 2, 1], [1, 2, 0, 1, 5], [4, 1, 0, 1, 7], [1, 0, 3, 0, 5]])
    matrix2 = NumMatrixV1([[3, 0, 1, 4, 2], [5, 6, 3, 2, 1], [1, 2, 0, 1, 5], [4, 1, 0, 1, 7], [1, 0, 3, 0, 5]])
    matrix3 = NumMatrixV1([[3, 0, 1, 4, 2], [5, 6, 3, 2, 1], [1, 2, 0, 1, 5], [4, 1, 0, 1, 7], [1, 0, 3, 0, 5]])
    data = [(2, 1, 4, 3, 8), (1, 1, 2, 2, 11), (1, 2, 2, 4, 12)]

    def test_sum_region(self):
        for test_row1, test_col1, test_row2, test_col2, result in self.data:
            self.assertEqual(result, self.matrix1.sumRegion(test_row1, test_col1, test_row2, test_col2))
            self.assertEqual(result, self.matrix2.sumRegion(test_row1, test_col1, test_row2, test_col2))
            self.assertEqual(result, self.matrix3.sumRegion(test_row1, test_col1, test_row2, test_col2))


if __name__ == '__main__':
    unittest.main()
