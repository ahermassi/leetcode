""" You are given an n x n binary matrix grid. You are allowed to change at most one 0 to be 1.

Return the size of the largest island in grid after applying this operation.

An island is a 4-directionally connected group of 1s. """


def largest_island_v1(grid):
    """ Brute force. TLE.

         For each 0 in the grid, temporarily change it to a 1, then count the size of the group from that square.
         From each flipped 0, we perform a DFS to find the size of that component. The answer is the maximum size
         component found.

         If there is no 0 in the grid, then the answer is the size of the entire grid.

    Time complexity: O(N^4)
    Space complexity: O(N^2)
    """

    def dfs(i, j):
        if not 0 <= i < n or not 0 <= j < n or not grid[i][j] or (i, j) in visited:
            return 0
        visited.add((i, j))
        area = 1
        for x, y in (i - 1, j), (i + 1, j), (i, j - 1), (i, j + 1):
            area += dfs(x, y)
        return area

    n, res = len(grid), 0
    for i in range(n):
        for j in range(n):
            if not grid[i][j]:
                grid[i][j] = 1
                visited = set()  # A new visited set for every DFS exploration from a 0
                res = max(res, dfs(i, j))
                grid[i][j] = 0
    return res if res != 0 else n * n


def largest_island_v2(grid):
    """ As in the previous solution, we check every 0. However, we also store the size of each group, so that we do not
        have to use DFS to repeatedly calculate the same size.

        But, this idea fails when the 0 touches the same group. For example, consider grid = [[1,1],[1,0]]. When we are
        in the bottom-right corner, the left neighbor and the upper neighbor are part of the same island.

        We can remedy this problem by keeping track of a group index that is unique for each island. Then, we'll only
        add areas of neighboring groups with different indices.

        For each 1 in the grid, we paint all connected 1s with the next available color (index). Since the grid has
        cells values 0 and 1, the island indices start from 2. We also remember the size of the island we just painted
        with that color by saving the result in a {index: area} map.
        Note that the grid elements are updated with their corresponding island index.

        Now, the problem boils down to merging multiple islands if there is just one 0 separating them. All these
        neighboring islands will become one island if we flip this 0 to 1.

        Then, for every 0 in the grid, we sum the sizes of connected islands based on the island color/index, plus 1 for
        the 0 we are toggling. This gives us a candidate answer for each 0 in the grid (see .img files).
        The possible connected islands indices are stored in a set to remove duplicate indices.

        Example:
            1 0 1 -> 2 0 3
            0 1 1 -> 0 3 3
            1 0 1 -> 4 0 3
        For the 0 at (0,1), area = 1 + island_area[2] + island_area[3] = 1 + 4 + 1 = 6
        For the 0 at (1,0), area = 1 + island_area[2] + island_area[3] + island_area[4] = 1 + 1 + 4 + 1 = 7

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
        area = 1
        for x, y in (i - 1, j), (i + 1, j), (i, j - 1), (i, j + 1):
            area += dfs(x, y, island_index)
        return area

    n = len(grid)
    res, visited = 0, set()
    island_area = dict()  # {color: area}: area of island painted with that color
    island_index = 2  # 0 and 1 are already used in the grid, hence we start the color index from 2
    for i in range(n):
        for j in range(n):
            if grid[i][j]:
                island_area[island_index] = dfs(i, j, island_index)
                island_index += 1
    for i in range(n):
        for j in range(n):
            if not grid[i][j]:
                # We collect unique color indices to avoid calculating the size of 2 connected components twice (e.g. if
                # the left neighbor and the upper neighbor are part of the same island)
                surrounding_islands_indices = set()
                for x, y in (i - 1, j), (i + 1, j), (i, j - 1), (i, j + 1):
                    if 0 <= x < n and 0 <= y < n and grid[x][y]:
                        surrounding_islands_indices.add(grid[x][y])
                surrounding_islands_areas = 0
                for index in surrounding_islands_indices:
                    surrounding_islands_areas += island_area[index]
                res = max(res, 1 + surrounding_islands_areas)  # +1 to account for the flipped 0
    return res if res > 0 else n * n


def largest_island_v3(grid):
    """ The previous implementation mutates the input, which in practice is not desirable.

         We can create another map {cell coordinates -> island index} and use it to retrieve the index of the island to
         which a neighbor cell belongs. This also means we no longer need to start the color/index from 2.

         In addition, we check for the maximum island area while enumerating the connected components to avoid the
         conditional check at the end of the algorithm.

    Time complexity: O(N^2)
    Space complexity: O(N^2)
    """

    def dfs(i, j, island_index):
        if not 0 <= i < n or not 0 <= j < n or not grid[i][j] or (i, j) in visited:
            return 0
        visited.add((i, j))
        island_map[(i, j)] = island_index
        area = 1
        for x, y in (i - 1, j), (i + 1, j), (i, j - 1), (i, j + 1):
            area += dfs(x, y, island_index)
        return area

    n, res = len(grid), 0
    island_map, island_area = dict(), dict()
    island_index = 1
    visited = set()
    for i in range(n):
        for j in range(n):
            if grid[i][j] == 1:
                area = dfs(i, j, island_index)
                island_area[island_index] = area
                res = max(res, area)
                island_index += 1
    for i in range(n):
        for j in range(n):
            if grid[i][j] == 0:
                surrounding_islands_indices = set()
                for x, y in (i - 1, j), (i + 1, j), (i, j - 1), (i, j + 1):
                    if 0 <= x < n and 0 <= y < n and grid[x][y]:
                        surrounding_islands_indices.add(island_map[(x, y)])
                surrounding_islands_areas = 0
                for index in surrounding_islands_indices:
                    surrounding_islands_areas += island_area[index]
                res = max(res, 1 + surrounding_islands_areas)
    return res

