""" You are given an n x n binary matrix grid. You are allowed to change at most one 0 to be 1.

Return the size of the largest island in grid after applying this operation.

An island is a 4-directionally connected group of 1s. """


def largest_island_v1(grid):
    """ For each 0 in the grid, let's temporarily change it to a 1, then count the size of the group from that square.
        For each 0, change it to a 1, then do a depth first search to find the size of that component. The answer is
        the maximum size component found. Of course, if there is no 0 in the grid, then the answer is the size of the
        whole grid.
    Time complexity: O(N^4)
    Space complexity: O(N^2)
    """

    def dfs(i, j, visited):
        if not 0 <= i < n or not 0 <= j < n or not grid[i][j] or (i, j) in visited:
            return 0
        visited.add((i, j))
        return 1 + dfs(i - 1, j, visited) + dfs(i + 1, j, visited) + dfs(i, j - 1, visited) + dfs(i, j + 1, visited)

    n = len(grid)
    res = 0
    for i in range(n):
        for j in range(n):
            if not grid[i][j]:
                grid[i][j] = 1
                res = max(res, dfs(i, j, set()))  # A new 'visited' set for every dfs exploration from a 0
                grid[i][j] = 0
    return res if res != 0 else n * n
