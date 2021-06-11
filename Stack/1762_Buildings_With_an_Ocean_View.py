""" There are n buildings in a line. You are given an integer array heights of size n that represents the heights of
the buildings in the line.

The ocean is to the right of the buildings. A building has an ocean view if the building can see the ocean without
obstructions. Formally, a building has an ocean view if all the buildings to its right have a smaller height.

Return a list of indices (0-indexed) of buildings that have an ocean view, sorted in increasing order. """


def find_buildings_v1(heights):
    """ Build a monotonically decreasing stack. It is in decreasing order for element value (height) and increasing
    order for element index. When the current height is greater than the top of the stack, we keep popping those
    shorter buildings because they can't have an ocean view.
    Time complexity:
    Space complexity: O(1)
    """
    stack = []
    for i, height in enumerate(heights):
        while stack and heights[stack[-1]] <= height:
            stack.pop()
        stack.append(i)
    return stack