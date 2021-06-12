""" There are n buildings in a line. You are given an integer array heights of size n that represents the heights of
the buildings in the line.

The ocean is to the right of the buildings. A building has an ocean view if the building can see the ocean without
obstructions. Formally, a building has an ocean view if all the buildings to its right have a smaller height.

Return a list of indices (0-indexed) of buildings that have an ocean view, sorted in increasing order. """


def find_buildings_v1(heights):
    """ Build a monotonically decreasing stack. It is in decreasing order for element value (height) and increasing
    order for element index. When the current height is greater than the top of the stack, we keep popping those
    shorter buildings because they can't have an ocean view.
    Time complexity: O(N) in the best case where all buildings are in decreasing order of height
    Space complexity: O(1)
    """
    stack = []
    for i, height in enumerate(heights):
        while stack and heights[stack[-1]] <= height:
            stack.pop()
        stack.append(i)
    return stack


def find_buildings_v2(heights):
    """ We can traverse the buildings from the nearest to the ocean to the furthest. We record the maximum to the
    right while traversing to determine if we can see the ocean or not. Put index in the result array if the current
    building is taller than the highest building seen so far. In the end, we need to reverse the array.
    Time complexity: O(N)
    Space complexity: O(1)
    """
    n, res = len(heights), []
    cur_max = 0
    for i in reversed(range(n)):
        cur_height = heights[i]
        if cur_height > cur_max:  # If the current building is taller than the tallest building to its right, then it's
            # taller than all buildings to its right, so it has an ocean view.
            res.append(i)
            cur_max = cur_height
    return res[::-1]
