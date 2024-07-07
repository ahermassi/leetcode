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
    """ Monotonically increasing stack

        In the previous approach, by removing all shorter buildings from the array before adding the current building,
        we inadvertently maintained a monotonic stack where the building heights are in decreasing order. So the key to
        the first approach's success was using a monotonic stack and traversing the array from left to right but looking
        left (to see which buildings are blocked) instead of looking right (to see if any building is blocking the
        current building's view).

        This time, we traverse from right to left and check if the current building's ocean view is blocked by any
        building to its right. We use a stack to store the buildings to the right in increasing order. For each
        building, we check if the top of the stack is strictly shorter than the current building and then add the
        current building to the stack.

        This process of checking for shorter buildings on the top of the stack before adding the current building to the
        stack means that the stack will always contain buildings in increasing order of height, hence it is called
        monotonically increasing stack.

        The basic idea is to only push the new element onto the stack if it is strictly larger than the top element.
        Since we are traversing the buildings from right to left, this means that the stack will only contain buildings
        of smaller height that are to the right of the current building. Thus, the current building will only have an
        ocean view.

        Therefore, by maintaining a monotonically increasing stack as we traverse the buildings from right to left, we
        can tell if a building has an ocean view by whether it is taller than the top of the stack. If it is, then it's
        taller than every other building to its right.

        Note that since we traverse the input array from right to left, the building indices are added to the stack in
        reverse order. Thus, before returning, we must reverse the stack so that it is in ascending order.

    Time complexity: O(N), each building's index can be pushed at most once
    Space complexity: O(N), an extra stack is created
    """
    n = len(heights)
    stack = []
    for i in reversed(range(n)):
        if not stack or heights[i] > heights[stack[-1]]:
            stack.append(i)
    return stack[::-1]


def find_buildings_v3(heights):
    """ Do we really need to store all the shorter buildings the right of the current building in the stack?

         As we iterated over the array from right to left, we pushed each building into the stack. Each building would
         remain in the stack until we reached a shorter building. At which point, the shorter building would only need
         to peek at the top of the stack to determine whether it could have an ocean view. would be popped from the stack.

         This means that the tallest building seen so far would always be in the stack unless the current building is
         the tallest building seen so far. Simply put, while traversing from right to left, the current building will
         only have an ocean view if it is the tallest building seen so far.

         Therefore, we can simplify the previous approach by traversing from right to left and just keep one variable to
         denote the tallest building seen so far. Then, if the current building's view is not blocked by the tallest
         building seen so far, the current building must have an ocean view. Thus, we just need to track the maximum
         height building encountered so far while traversing from right to left.

    Time complexity: O(N)
    Space complexity: O(1)
    """
    n, res = len(heights), []
    tallest_building = float('-inf')
    for i in reversed(range(n)):
        if heights[i] > tallest_building:
            # If the current building is taller than the tallest building to its right, then it's taller than all
            # buildings to its right, so it has an ocean view.
            tallest_building = heights[i]
            res.append(i)
    return res[::-1]
