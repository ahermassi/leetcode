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
