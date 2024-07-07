""" There are n buildings in a line. You are given an integer array heights of size n that represents the heights of
the buildings in the line.

The ocean is to the right of the buildings. A building has an ocean view if the building can see the ocean without
obstructions. Formally, a building has an ocean view if all the buildings to its right have a smaller height.

Return a list of indices (0-indexed) of buildings that have an ocean view, sorted in increasing order. """


def find_buildings_v1(heights):
    """ The most naive approach is as follows: for each building, we iterate over all the buildings to its right and
         check if there is any building with equal or greater height than the current building. However, this approach
         requires O(N^2) time because, for all N buildings, we check every building to its right to see if any are of
         equal height or taller, which requires O(N) time per building.

         So what can we change to improve on the naive solution?

         When looking for a way to optimize the naive solution, sometimes it helps to consider the problem from a new
         perspective. How about instead of looking right and asking, "does any building block this building's view?", we
         look left and ask "which buildings' view is blocked by this building?"

         For each building, initially, let's assume that it has an ocean view. Currently, we're not worrying about any
         of the buildings to the right. Instead, we look left and see if any of the buildings that had an ocean view are
         blocked by the current building. Any buildings whose view is blocked must be removed from the answer array
         before we can add the current building into the answer array.

         Now, if the current building is strictly shorter than the last building in the answer array, then it will not
         block the ocean view of any of the buildings that are already present in the answer array. This is because the
         last building present in the array was not blocking the ocean view of any other buildings, and the current
         building must be even shorter. Thus, the current building will be shorter than all the other buildings in the
         answer array.

         By repeating this process of removing any building with a blocked view from the array and then appending the
         current building to the array, every building will be added to the answer array once, and every blocked
         building will be removed from the answer array once.

        This process builds a monotonically decreasing stack. It is in decreasing order for height and increasing order
        for index. When the current height is greater than the top of the stack, we keep popping those shorter buildings
        because they can't have an ocean view.

    Time complexity: O(N), each building's index can be pushed and popped at most once
    Space complexity: O(N), there is no auxiliary space used other than the output which does not count towards the
    space complexity. However, in the worst-case scenario, the stack may contain as many as N−1 indices, and then the
    very last building is the tallest, so the output will reduce to one index. In this scenario, the algorithm must
    store N−1 elements at some point, but only 1 element is included in the output.
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
