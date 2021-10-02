""" You are given an m x n grid grid of values 0, 1, or 2, where:

each 0 marks an empty land that you can pass by freely,
each 1 marks a building that you cannot pass through, and
each 2 marks an obstacle that you cannot pass through.
You want to build a house on an empty land that reaches all buildings in the shortest total travel distance. You can
only move up, down, left, and right.

Return the shortest travel distance for such a house. If it is not possible to build such a house according to the
above rules, return -1.

The total travel distance is the sum of the distances between the houses of the friends and the meeting point.

The distance is calculated using Manhattan Distance, where distance(p1, p2) = |p2.x - p1.x| + |p2.y - p1.y|. """

from collections import deque, defaultdict


def shortest_distance_v1(grid):
    """ BFS from Empty Land to All Houses.

        Our graph is not weighted. We can consider each edge to have the same weight of 1. Since the graph is
        unweighted, BFS can be used to find the shortest path between a starting cell and any other reachable cell.
        The actual distance calculation measures grid distance in terms of only horizontal and vertical movements.
        Since we can only move up, down, left, and right, we can apply BFS to calculate the actual distance. At each
        iteration in the BFS, we will only consider expanding our search in the horizontal or vertical direction.

        For each empty cell (cell value equals 0) in the grid, start a BFS and sum all the distances to houses
        (cell value equals 1) from this cell. We will also keep track of the number of houses we have reached from
        this source cell (empty cell). If we cannot reach all the houses from the current empty cell, then it is not a
        valid empty cell. Furthermore, we can be certain that any cell visited during this BFS also cannot reach all
        of the houses. So we will mark all cells visited during this BFS as obstacles to ensure that we do not start
        another BFS from this region.

        Every time we reach a house, increment houses reached counter 'houses_found' by 1, and increase the total
        distance by the current distance (i.e., the distance from the start cell to the house).
        If 'houses_found' equals 'number_of_houses', then return the total distance. Otherwise, the starting cell
        (and every cell visited during this BFS) cannot reach all of the houses. So set every visited EMPTY land cell
        equal to 2 so that we do not start a new BFS from that cell.

    Time complexity: O(N^2 * M^2)
    Space complexity: O(N * M), we use an extra hash set to track the visited cells, and the queue will store each
    matrix element at most once during each BFS
    """
    n, m = len(grid), len(grid[0])
    res = float('inf')
    number_of_houses = 0
    for i in range(n):
        for j in range(m):
            if grid[i][j] == 1:
                number_of_houses += 1
    for i in range(n):
        for j in range(m):
            if not grid[i][j]:
                queue = deque([(i, j, 0)])
                visited = {(i, j)}
                distance = houses_found = 0
                while queue:
                    row, col, cur_distance = queue.popleft()
                    # If this cell is a house, then add the distance from source to this cell and go past from this cell
                    if grid[row][col] == 1:
                        distance += cur_distance
                        houses_found += 1
                        continue
                    for x, y in (row-1, col), (row+1, col), (row, col-1), (row, col+1):
                        if 0 <= x < n and 0 <= y < m and (x, y) not in visited and grid[x][y] != 2:
                            queue.append((x, y, cur_distance + 1))
                            visited.add((x, y))
                if houses_found == number_of_houses:
                    res = min(res, distance)
                # If we did not reach all houses, then any cell visited also cannot reach all houses. Set all cells
                # visited to 2 so we do not check them again.
                else:
                    for x, y in visited:
                        if not grid[x][y]:
                            grid[x][y] = 2
    return res if res != float('inf') else -1


def shortest_distance_v2(grid):
    """ BFS from Houses to Empty Land.

        In the previous approach, to get the minimum distance we started a BFS from each empty land (cell value equal
        to 0) to all the houses (cell value equal to 1), but another way to look at the problem is starting from a
        house and finding all reachable empty lands. If we can reach a house from an empty land, then we can also
        traverse the other way (i.e., reach empty land from a house).

        Previously, we were calculating the total minimum distance sum of one empty cell in one BFS traversal, hence
        we were only returning the distance sum from the BFS for each cell. But if we start BFS from a house instead
        of an empty cell, we will be generating partial distance (i.e., distance from only one house to the current
        empty cell and not the sum distance from all the houses to this empty cell), hence we need some extra space
        to store the sum of the partial distances from each house cell.

        We will need to store 2 values at each cell position of empty cells: total distance sum from all houses to
        this empty land AND number of houses that can reach this empty land.

        For each empty cell we reach, increase the cell's sum of distances distances[(i,j)] by the steps taken to
        reach the cell. We also increment the cell's house counter reachable_houses[(i,j)] by 1.

        After traversing all houses, get the minimum distance from all empty cells which have reachable_houses[(i,j)]
        equal to 'number_of_houses'.

    Time complexity: O(N^2 * M^2)
    Space complexity: O(N * M), we use an extra hash set to track the visited cells and two hash maps to store distance
    sum along with the house counter for each empty cell, and the queue will store each matrix element at most once
    during each BFS
    """
    n, m = len(grid), len(grid[0])
    res = float('inf')
    number_of_houses = 0
    distances = defaultdict(int)
    reachable_houses = defaultdict(int)
    for i in range(n):
        for j in range(m):
            if grid[i][j] == 1:
                number_of_houses += 1
                queue = deque([(i, j, 0)])
                visited = set()
                while queue:
                    row, col, cur_distance = queue.popleft()
                    for x, y in (row-1, col), (row+1, col), (row, col-1), (row, col+1):
                        if 0 <= x < n and 0 <= y < m and (x, y) not in visited and not grid[x][y]:
                            # If we reached an empty cell, then add the distance and increment the count of houses
                            # reached at this cell
                            reachable_houses[(x, y)] += 1
                            distances[(x, y)] += cur_distance + 1
                            queue.append((x, y, cur_distance + 1))
                            visited.add((x, y))
    for land in distances:
        # Check all empty lands with houses count equal to total houses
        if grid[land] == 0 and reachable_houses[land] == number_of_houses:
            res = min(res, distances[land])
    return res if res != float('inf') else -1
