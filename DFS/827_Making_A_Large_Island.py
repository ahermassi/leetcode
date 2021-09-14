""" You are given an n x n binary matrix grid. You are allowed to change at most one 0 to be 1.

Return the size of the largest island in grid after applying this operation.

An island is a 4-directionally connected group of 1s. """

from collections import defaultdict


def largest_island_v1(grid):
    """ Brute force. TLE.
        For each 0 in the grid, let's temporarily change it to a 1, then count the size of the group from that square.
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


def largest_island_v2(grid):
    """ For each 1 in the grid, we paint all connected 1s with the next available color (2, 3, and so on). We also
        remember the size of the island we just painted with that color. Then, for every 0 in the grid, we sum the
        sizes of connected islands based on the island color/index.
        Explore every island using DFS, calculate its area, give it an island index, and save the result to a
        {index: area} map. Note that the grid elements are updated with their corresponding island index. Since the
        grid has elements 0 and 1, the island index is initialized with 2. Then, for every cell == 0, check its
        connected islands and calculate total islands' area. The possible connected islands indices are stored in a set
        to remove duplicate indices.
        Example:
            1 0 1 -> 2 0 3
            0 1 1 -> 0 3 3
            1 0 1 -> 4 0 3
        For the 0 at (0,1), area = island_area[2] + island_area[3] + 1 = 1 + 4 + 1 = 6
        For the 0 at (1,0), area = island_area[2] + island_area[3] + island_area[4] + 1 = 1 + 4 + 1 + 1 = 7
    Time complexity: O(N^2)
    Space complexity: O(N^2)
    """

    def dfs(i, j, island_index):
        # This method paints the current island starting at cell (i,j) and all its connected neighbors and returns the
        # size of the painted island
        if not 0 <= i < n or not 0 <= j < n or not grid[i][j] or (i, j) in visited:
            return 0
        grid[i][j] = island_index
        visited.add((i, j))
        return 1 + dfs(i - 1, j, island_index) + dfs(i + 1, j, island_index) + dfs(i, j - 1, island_index) + \
               dfs(i, j + 1, island_index)

    n = len(grid)
    res, visited = 0, set()
    island_area = defaultdict(int)  # {color: area}: Area of island painted of that color
    island_index = 2  # 0 and 1 are already used in grid, hence we start color index from 2
    for i in range(n):
        for j in range(n):
            if grid[i][j]:
                island_area[island_index] = dfs(i, j, island_index)
                island_index += 1
    for i in range(n):
        for j in range(n):
            if not grid[i][j]:
                # We get unique color indices to avoid calculating the size of 2 connected components twice (it can
                # happen that for example left neighbor and upper neighbor are the same island)
                indices = set()
                for x, y in (i - 1, j), (i + 1, j), (i, j - 1), (i, j + 1):
                    if 0 <= x < n and 0 <= y < n:
                        indices.add(grid[x][y])
                sum_areas = sum(island_area[index] for index in indices)
                res = max(res, 1 + sum_areas)  # +1 to account for the flipped 0
    return res if res != 0 else n * n

