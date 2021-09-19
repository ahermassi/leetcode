""" A storekeeper is a game in which the person pushes boxes around in a warehouse trying to get them to target
locations.

The game is represented by an m x n grid of characters grid where each element is a wall, floor, or box.

Your task is to move the box 'B' to the target position 'T' under the following rules:

The character 'S' represents the person. The person can move up, down, left, right in grid if it is a floor
(empty cell).
The character '.' represents the floor which means a free cell to walk.
The character '#' represents the wall which means an obstacle (impossible to walk there).
There is only one box 'B' and one target cell 'T' in the grid.
The box can be moved to an adjacent free cell by standing next to the box and then moving in the direction of the box.
This is a push.
The person cannot walk through the box.
Return the minimum number of pushes to move the box to the target. If there is no way to reach the target, return -1.
"""

from collections import deque


def min_push_box(grid):
    """ Let's break the question into two simple parts:

        Let's think that we have no person and we have to find the minimum path between box and the target. Easy right?
        Simple BFS.

        If we know how to solve the first part, what we actually do is modify that part with few constraints:
            - We check whether the box can be shifted to the new position (up, down, left, right)
            - For it to be shifted to the new position, the person has to be in a corresponding position from the
              other side.
            - So we check if the person can travel from his old position to his corresponding new position using
              a second BFS.
            - If the person can travel to his new position then the box can be shifted, otherwise the box cannot be
              shifted.

        We keep repeating step 2 until we reach the target or it is not possible to move the box anymore.

        We need to make sure the storekeeper a has room to push the box AND has a way to go to the cell to push the box.
        Therefore, need another BFS to find if the path exists. When the person moves a box, they will take the place
        of the box.

        While trying to record the visited position of a box, we need to include an additional dimension to record
        which direction the person pushed the box from. For example, there are 4 previous positions that the box can
        arrive at position (x, y). We have to treat those 4 states separately. For this reason, we represent the search
        state as (person_row, person_col, box_row, box_col), or (person, box).

        The box itself is an obstacle so we need to check if a person can walk separately for each box position. As a
        consequence, we need to track (person + box) positions as visited.
        The same position of the person and the box can be walkable or not depending on where the person starts. So we
        should mark the (person + box) position as visited only when it is reachable.

    Time complexity: O((N * M)^2)
    Space complexity: O(N * M)
    """

    def is_valid(x, y):
        return 0 <= x < n and 0 <= y < m and grid[x][y] != '#'

    def person_can_reach(cur_person, dest_person, box):
        # Check if the person at position 'cur_person' can walk to stand in front of the box at position 'dest_person'
        # without walking through the box at position 'box'
        queue = deque([cur_person])
        visited = {cur_person}
        while queue:
            person = queue.popleft()
            if person == dest_person:
                return True
            i, j = person
            for a, b in (i - 1, j), (i + 1, j), (i, j - 1), (i, j + 1):
                if is_valid(a, b) and (a, b) not in visited and (a, b) != box:
                    queue.append((a, b))
                    visited.add((a, b))
        return False

    box, person, target = None, None, None
    n, m = len(grid), len(grid[0])
    for i in range(n):
        for j in range(m):
            if grid[i][j] == 'B':
                box = (i, j)
            elif grid[i][j] == 'S':
                person = (i, j)
            elif grid[i][j] == 'T':
                target = (i, j)
    queue = deque([(box, person, 0)])
    visited = set()
    while queue:
        box, person, pushes = queue.popleft()
        if box == target:
            return pushes

        # These are the new possible coordinates the box can be pushed to (up, down, right, left).
        new_box_pos =    [(box[0] - 1, box[1]), (box[0] + 1, box[1]), (box[0], box[1] - 1), (box[0], box[1] + 1)]
        # These are the corresponding positions the person has to be in to push the box in the new coordinates
        new_person_pos = [(box[0] + 1, box[1]), (box[0] - 1, box[1]), (box[0], box[1] + 1), (box[0], box[1] - 1)]

        for new_box, new_person in zip(new_box_pos, new_person_pos):
            if is_valid(*new_box) and is_valid(*new_person) \
                    and (new_box, new_person) not in visited \
                    and person_can_reach(person, new_person, box):
                visited.add((new_box, new_person))
                queue.append((new_box, new_person, pushes + 1))
    return -1
