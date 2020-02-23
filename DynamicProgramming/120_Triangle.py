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
    Time complexity: O(N^2), the time spent per element is O(1) and there are 1 + 2 +...+ n = n(n+1) elements
    Space complexity: O(N^2)
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


def minimum_total_v3(triangle):
    """ Same as previous solution, but since after we complete processing row i we do not need the results for row
        (i - 1) to process row (i + 1), we can reuse storage.
    Time complexity: O(N^2)
    Space complexity: O(N)
    """
    n, pre = len(triangle), triangle[0]
    for i in range(1, n):
        cur = [0] * (i + 1)
        for j in range(i + 1):
            if j == 0:
                cur[j] = pre[j] + triangle[i][j]
            elif j == i:
                cur[j] = pre[j - 1] + triangle[i][j]
            else:
                cur[j] = min(pre[j - 1], pre[j]) + triangle[i][j]
        pre = cur
    return min(pre)


def minimum_total_v4(triangle):
    """ Yet another bottom-up dynamic programming solution.
        If we look closely, we would notice that the adjacent nodes always share a 'branch'. In other word, there are
        overlapping sub-problems. Also, suppose x and y are 'children' of k. Once minimum paths from x and y to the
        bottom are known, the minimum path starting from k can be decided in O(1), that is optimal substructure.
        Therefore, dynamic programming would be the best solution to this problem in terms of time complexity.
        We start from the nodes on the bottom row; the min path sums for these nodes are the values of the nodes
        themselves. From there, the min path sum at the jth node on the ith row would be the smallest of the path sums
        of its two (below) children plus the value of itself:
            dp[i][j] = min( dp[i+1][j], dp[i+1][j+1]) + triangle[i][j]
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
    """ Same as previous solution, but since after we complete processing row i we do not need the results for row
        (i + 1) to process row (i - 1), we can reuse storage.
    Time complexity: O(N^2)
    Space complexity: O(N)
    """
    n, pre = len(triangle), triangle[-1]
    for i in reversed(range(n - 1)):
        cur = [0] * (n + 1)
        for j in range(i + 1):
            cur[j] = min(pre[j], pre[j + 1]) + triangle[i][j]
        pre = cur
    return pre[0]

