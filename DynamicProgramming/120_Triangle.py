""" Given a triangle, find the minimum path sum from top to bottom. Each step you may move to adjacent numbers on the
row below. """


def minimum_total_v1(triangle):
    """ Recursive, bottom-up. TLE
    Time complexity: O(2^N), where N is the number of rows in the triangle
    Space complexity: O(N)
    """

    def dfs(i, j, path):
        if i == n - 1:
            res.append(path + triangle[i][j])
            return
        path += triangle[i][j]
        for x, y in (i + 1, j), (i + 1, j + 1):
            dfs(x, y, path)

    n, res = len(triangle), []
    dfs(0, 0, 0)
    return min(res)


def minimum_total_v2(triangle):
    """ Bottom-up dynamic programming.
        A far better way is to consider entries in the ith row. For any such entry, if we look at the minimum weight
        path ending at it, the part of the path that ends at the previous row must also be a minimum weight path. This
        gives us a DP solution. We iteratively compute the minimum weight of a path ending at each entry in row i using
        the results at row (i - 1).
    """
    n, dp = len(triangle), [[0] * len(row) for row in triangle]
    dp[0][0] = triangle[0][0]
    for i in range(1, n):
        for j in range(i + 1):  # We calculate the minimum path sum ending at each cell j of the current row i
            if j == 0:  # The first cell has only 1 previous adjacent cell
                dp[i][j] = dp[i - 1][j] + triangle[i][j]
            elif j == i:  # The last cell has only 1 previous adjacent cell
                dp[i][j] = dp[i - 1][j - 1] + triangle[i][j]
            else:  # The minimum path sum ending at this cell is the least sum of its two previous adjacent cells plus
                # the current cell's value
                dp[i][j] = min(dp[i - 1][j - 1], dp[i - 1][j]) + triangle[i][j]
    return min(dp[-1])  # Each cell of the last row contains the minimum sum of the path ending at that cell
