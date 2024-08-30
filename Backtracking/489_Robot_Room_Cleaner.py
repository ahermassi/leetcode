""" You are controlling a robot that is located somewhere in a room. The room is modeled as an m x n binary grid
where 0 represents a wall and 1 represents an empty slot.

The robot starts at an unknown location in the root that is guaranteed to be empty, and you do not have access to the
grid, but you can move the robot using the given API Robot.

You are tasked to use the robot to clean the entire room (i.e., clean every empty cell in the room). The robot with
the four given APIs can move forward, turn left, or turn right. Each turn is 90 degrees.

When the robot tries to move into a wall cell, its bumper sensor detects the obstacle, and it stays on the current cell.

Design an algorithm to clean the entire room using the following APIs:
"""


class Robot:
    # Returns true if next cell is open and robot moves into the cell.
    # Returns false if next cell is obstacle and robot stays on the current cell.
    def move(self):
        pass

    # Robot will stay on the same cell after calling turnLeft/turnRight. Each turn will be 90 degrees.
    def turnLeft(self):
        pass

    def turnRight(self):
        pass

    # Clean the current cell.
    def clean(self):
        pass


# For a full visualization:
# https://assets.leetcode.com/users/images/fb1a84bd-ad35-485d-9c5c-7cdb4318ce4e_1622019997.0954082.gif
def clean_room(robot):
    """ This solution is based on the same idea as a maze-solving algorithm called right-hand rule. Go forward,
         cleaning and marking all the cells on the way as visited. At the obstacle turn right, again go forward, etc.
         Always turn right at the obstacles and then go forward. Consider already visited cells as virtual obstacles.

         What to do if, after the right turn, there is an obstacle just in front? Turn right again.

         How to explore the alternative paths from the cell? Go back to that cell and then turn right from the last
         explored direction.

         When to stop? Stop when we explored all possible paths, i.e. all 4 directions (up, right, down, and left) for
         each visited cell.

         Even though we do not have a matrix in input and do not know where the robot should start, we can use relative
         coordinates to represent the positions. We can assume the current cell that the robot is at is (0, 0), then the
         cell to its left will be (0, -1), and the cell above it will be (-1, 0), etc. Then, we should also use a hash
         set to keep track of the cells that the robot has already visited.

         For any of the locations the robot is currently at, it has 4 choices to expand: up, right, down, left.
         Note that in order to move left, we need to make sure that the robot is currently FACING left before we call
         move(). Therefore:

                        The core of this problem is to know the direction the robot is facing before we move to
                                        the next cell, only then we can move to the correct cell.

         Assume we already know the current direction that the robot is facing is left, what can we do at this point?
         We can ask the robot to keep moving, until it can't go any further.

         When the robot keeps moving in the direction of left, but then hits an obstacle or runs into a cell that has
         been visited before, what can we do? We try to ask the robot to make a turn so that it will face towards
         another direction, then it can keep moving. Since the robot can't move when it's facing left, we can first ask
         the robot to make a right turn, so it is now facing up, and we should now check if it can go up. If it can,
         then go up. We can keep asking the robot to make right turns until all the possible directions (up, right,
         down) are explored. Finally, when all the directions are tried, the robot should be facing the direction that
         it originally started from, which is left in this case.

         What happens if the robot has exhausted all the directions that it can visit?
         If this is the case, we should go back to the cell that we originally started from. As mentioned above, after
         trying out all the possible directions, the robot will be facing the direction that it originally was.
         This is where we use backtracking to restore the original state. Therefore, what we can do is ask the robot to
         make 2 right turns, and then move once. However, we should also make sure the robot is facing the exact same
         direction it started with, so we should make another 2 right turns.

         What does (next_direction = (facing_direction + k) % 4) mean?
         Assume the robot is currently facing left, so facing_direction is 3, and we want the robot to try all the
         directions in the following sequence: 3 (left), 0 (up), 1 (right), 2 (down). As we can see, since the starting
         direction is 3 (facing left), when we add 1 (turn right), the direction index becomes 4. However, the correct
         index should be 0 (up), since the robot is facing up. That's why we introduce the modulo operation to make sure
         the direction always falls into the range [0..3].

         We want to try all 4 directions, facing_direction is the index of the next direction vector since we are
         turning the robot right in every iteration (which is why the order is {-1,0},{0,1},{1,0},{0,-1}. Turning
         left works too, but then the direction's order will need to represent that. If we simply do something like
         (for direction in directions) this won't work as we always pick the first direction from the list to go to
         which is up, but what we need to do is continue in clockwise fashion from the current direction.

    Time complexity: O(N- M), where N is the number of cells in the room and M is a number of obstacles. We visit each
    non-obstacle cell once and only once. At each visit, we check 4 directions around the cell. Therefore, the total
    number of operations would be 4⋅(N−M).
    Space complexity: O(N - M), used by the hash set to keep track of visited non-obstacle cells
    """

    def dfs(i, j, facing_direction):
        # facing_direction: 0 (up), 1 (right), 2 (down), 3(left)
        robot.clean()
        visited.add((i, j))
        for k in range(4):
            # Try out 4 different directions:
            # k = 0: keep moving towards the current direction that we're facing
            # k = 1: make 1 right turn and try that new direction
            # k = 2: make 2 right turns and try that new direction
            # k = 3: make 3 right turns and try that new direction
            next_direction = (facing_direction + k) % 4
            x, y = directions[next_direction]
            next_i, next_j = i + x, j + y
            if (next_i, next_j) not in visited and robot.move():
                # Next cell has not been visited and is accessible
                dfs(next_i, next_j, next_direction)
                # Come back from the above recursive call, and the robot is currently at (next_i, next_j). We should
                # do a backtracking here to ask the robot to return to (i, j).
                # When we return from the DFS, the robot is one cell ahead facing the same direction it started from.
                # 2 right turns make it face the opposite direction: down if it started up, right if it started left,
                # etc.
                robot.turnRight()
                robot.turnRight()
                # Move to the starting cell
                robot.move()
                # Moved to the starting cell, but still facing the opposite direction. 2 right turns will fix that.
                robot.turnRight()
                robot.turnRight()
            # The current direction has been explored. We should make a right turn and try to explore another direction
            robot.turnRight()

    directions = [(-1, 0), (0, 1), (1, 0), (0, -1)]  # [(go up), (go right), (go down), (go left)]
    visited = set()
    dfs(0, 0, 0)
