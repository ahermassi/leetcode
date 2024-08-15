""" Given a triangle, find the minimum path sum from top to bottom. Each step you may move to adjacent numbers on the
row below. """


def minimum_total_v1(triangle):
    """ Top-Down Dynamic Programming.

         We'll define a recursive helper function dfs(row, col) that returns the minimum path sum from the cell at
         (row, col), down to the base of the triangle. The minimum path sum for the entire triangle, would, therefore,
         be dfs(0, 0).

         The base case is where there are no more rows. In this case, we should simply return 0.
         Another base case is where there are no more rows below. In this case, we return the current cell's value.

         The recursive case is where there is still at least one row below the current cell. We simply need to add the
         current cell to the minimum path sum of the cells below it.

         To avoid re-calculating the same results over and over again, we can use a memoization hashmap.

    Time complexity: O(N^2), where N is the number of rows in the triangle. The memoization map ensures that dfs is only
    called once for each cell. As there are N^2 cells, we get a total time complexity of O(N^2).
    Space complexity: O(N^2), for the call stack and cache
    """

    def dfs(row, col):
        if row == n:
            return 0
        if row == n - 1:
            return triangle[row][col]
        if (row, col) in memo:
            return memo[(row, col)]
        lower_left, lower_right = dfs(row + 1, col), dfs(row + 1, col + 1)
        memo[(row, col)] = triangle[row][col] + min(lower_left, lower_right)
        return memo[(row, col)]

    n = len(triangle)
    memo = {}
    return dfs(0, 0)


def minimum_total_v2(triangle):
    """ Bottom-Up Dynamic Programming.

         We can solve the problem by iterating through each row of the triangle, from top to bottom, updating each
         number to be the sum of itself + the minimum out of the two numbers above it. For each cell in the triangle,
         we could have reached there from the previous row/level either from the same column index or column-1.

         So, obviously, the optimal choice to arrive at the current position in the triangle would be to come from the
         cell having the minimum value of these two choices.

         We need to be quite careful designing the algorithm: the rows and columns are all different sizes, greatly
         increasing the risk of off-by-one errors. The rows are numbered from top to bottom (so the triangle tip is the
         first row), and the columns are numbered left to right.

         We can use the following rules for obtaining the cells above a cell with coordinate (row, col):

            - If row == 0: this is the top of the triangle: it stays the same.
            - If col == 0: there is only one cell above, located at (row - 1, col).
            - If col == row: There is only one cell above, located at (row - 1, col - 1).
            - In all other cases: there are two cells above, located at (row - 1, col - 1) and (row - 1, col).

        Let dp[i][j] be the minimum path sum in the triangle whose "base tip" is triangle[i][j]. Based on the rules
        above, we have the transition function:

                 dp[i][j] = triangle[i][j] + min(dp[i-1][j], dp[i-1][j-1])

        Finally, we can return the minimum value that we get at the bottom-most row of the dp table.

    Time complexity: O(N^2), the time spent per element is O(1) and there are 1 + 2 +...+ N = N * (N+1) elements
    Space complexity: O(N^2)
    """
    n, dp = len(triangle), [[0] * len(row) for row in triangle]
    dp[0][0] = triangle[0][0]
    for i in range(1, n):
        # The row at index i has i+1 elements.
        # Calculate the minimum path sum ending at each cell j of the current row i.
        for j in range(i + 1):
            upper_left = upper_right = float('inf')
            if j == 0:
                # The first cell has only 1 previous "parent" cell above
                upper_right = dp[i - 1][j]
            elif j == i:
                # The last cell has only 1 previous "parent" cell above
                upper_left = dp[i - 1][j - 1]
            else:
                upper_left = dp[i - 1][j - 1]
                upper_right = dp[i - 1][j]
            # The minimum path sum ending at this cell is the min sum of its two previous adjacent cells at the row
            # above plus the current cell's value
            dp[i][j] = triangle[i][j] + min(upper_left, upper_right)
    return min(dp[-1])  # Each cell of the last row contains the minimum sum of the path ending at that cell


def minimum_total_v3(triangle):
    """ Space-optimized Bottom-Up Dynamic Programming.

         Notice that as we worked our way down the rows of the triangle, we only ever needed to look at the row
         immediately above. This means that we only need to maintain the current row and the previous row.

    Time complexity: O(N^2)
    Space complexity: O(N)
    """
    n, pre = len(triangle), triangle[0]
    for i in range(1, n):
        cur = [0] * (i + 1)  # The row at index i has i+1 elements.
        for j in range(i + 1):
            upper_left = upper_right = float('inf')
            if j == 0:
                upper_right = pre[j]
            elif j == i:
                upper_left = pre[j - 1]
            else:
                upper_left = pre[j - 1]
                upper_right = pre[j]
            cur[j] = triangle[i][j] + min(upper_left, upper_right)
        pre = cur
    return min(pre)


# Video explanation: https://youtu.be/OM1MTokvxs4
def minimum_total_v4(triangle):
    """ Bottom-up Dynamic Programming.

         The problem description tells us that we need to find the minimum path sum from top to bottom. This immediately
         suggests that we should be working from top to bottom, like what we did in the previous approaches. But is this
         actually necessary? Could we go from bottom to top instead?

         It turns out, we can! The exact same ideas apply - each cell instead becomes the sum of itself plus the minimum
         of the two cells below it. The only difference is that we need to do the edge case handling a bit differently.
         There is a big advantage though: the code turns out a lot simpler. Some cells only had one cell above them, but
         here every cell has two cells below it!

         When we worked from top to bottom, the edge cells had only one cell above them. But when we work from bottom to
         top, all cells, except for those in the bottom row (which are the base case and so don't need to be modified
         anyway) have exactly two cells below them. Where (row, col) is the current cell, the cells below are located at
         (row + 1, col) and (row + 1, col + 1).

         Let dp[i][j] be the minimum path sum in the triangle whose top is triangle[i][j]. Based on the rules
        above, we have the transition function:

                    dp[i][j] = triangle[i][j] + min(dp[i+1][j], dp[i+1][j+1])

        Finally, the answer is the minimum path sum in the triangle whose top is triangle[0][0], i.e. dp[0][0].

    Time complexity: O(N^2)
    Space complexity: O(N^2)
    """
    n = len(triangle)
    dp = [[0] * n for _ in range(n)]
    for j in range(n):
        dp[n - 1][j] = triangle[n - 1][j]  # Base case: the last row
    for i in reversed(range(n - 1)):
        for j in range(i + 1):
            dp[i][j] = min(dp[i + 1][j], dp[i + 1][j + 1]) + triangle[i][j]
    return dp[0][0]


def minimum_total_v5(triangle):
    """ Space-optimized Bottom-Up Dynamic Programming.

            Notice that as we worked our way from bottom to top, we only ever needed to look at the row immediately
            below. This means that we only need to maintain the current row and the row below.

    Time complexity: O(N^2)
    Space complexity: O(N)
    """
    n, below = len(triangle), triangle[-1]
    for i in reversed(range(n - 1)):
        cur = [0] * (i + 1)
        for j in range(i + 1):
            cur[j] = triangle[i][j] + min(below[j], below[j + 1])
        below = cur
    return below[0]


def minimum_total_v6(triangle):
    """ Or even better, since the row below would be useless after the current row is processed, we can use a single
         array that we keep updating.

    Time complexity: O(N^2)
    Space complexity: O(N)
    """
    n, dp = len(triangle), triangle[-1]
    for i in reversed(range(n - 1)):
        for j in range(i + 1):
            dp[j] = triangle[i][j] + min(dp[j], dp[j + 1])
    return dp[0]

