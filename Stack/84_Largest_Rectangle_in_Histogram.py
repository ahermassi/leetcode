""" Given n non-negative integers representing the histogram's bar height where the width of each bar is 1, find the
area of largest rectangle in the histogram. """


def largest_rectangle_area(heights):
    """
    Pattern: Monotonic increasing stack — previous smaller + next smaller boundaries.

    First-principles idea:

    For any particular bar i with height h, the largest rectangle that uses
    height h can extend left and right for as long as every bar in that range
    has height >= h.

    Therefore, the rectangle is bounded by:

        - the first bar smaller than h on the left
        - the first bar smaller than h on the right

    If those boundaries are L and R, then they themselves cannot participate
    in the rectangle, so:

        width = R - L - 1
        area  = h * (R - L - 1)

    --------------------------------------------------------------------------
    Brute force
    --------------------------------------------------------------------------

    For every bar i, we could:

        1. Scan left until we find the first smaller bar.
        2. Scan right until we find the first smaller bar.
        3. Compute:

               area = heights[i] * (right - left - 1)

    This is correct, but in the worst case we scan O(N) positions for each of
    the N bars, giving:

        Time complexity: O(N^2)

    --------------------------------------------------------------------------
    How the monotonic stack improves this
    --------------------------------------------------------------------------

    Instead of repeatedly searching for the previous-smaller and next-smaller
    boundaries, we process the bars from left to right and maintain a
    monotonically increasing stack of indices.

    The important event is encountering a bar that is shorter than the bar at
    the top of the stack.

    Suppose the current index is i and:

        heights[i] < heights[stack[-1]]

    The bar at the top can no longer extend any farther to the right while
    keeping its own height, because the current shorter bar blocks it.

    Therefore, when we pop that bar:

        popped_index = stack.pop()

    we have just discovered its NEXT smaller boundary:

        right boundary = i

    What about its previous smaller boundary?

    After popping it, the new top of the stack is the closest bar to its left
    that is shorter than the popped bar.

    Therefore:

        left boundary = stack[-1]

    At that exact moment, both boundaries are known:

        left smaller             popped bar               right smaller
             |                       |                          |
             v                       v                          v
        ... [L] ... >= h ... >= h [h] ... >= h ... >= h ... [R]

        L = stack[-1]
        R = i

    So we can immediately finalize the largest rectangle that uses the popped
    bar's height:

        width = i - stack[-1] - 1
        area  = heights[popped_index] * width

    We keep popping because one short bar can simultaneously become the right
    boundary for several taller bars.

    --------------------------------------------------------------------------
    Why the stack is monotonically increasing
    --------------------------------------------------------------------------

    Before pushing the current bar, we remove every taller bar that the current
    shorter bar resolves.

    Therefore, after all necessary pops, the bar underneath the current one is
    no taller than it.

    The stack consequently remains monotonically increasing by height.

    More importantly, each bar on the stack represents a bar whose right
    smaller boundary has NOT been discovered yet.

    --------------------------------------------------------------------------
    Sentinel bars
    --------------------------------------------------------------------------

    We add a height-0 bar to both ends:

        heights = [0] + heights + [0]

    The left sentinel solves the "no smaller bar to the left" case.

    Because every real bar has height >= 0, the sentinel remains at the bottom
    of the stack. Therefore, after popping a real bar, stack[-1] always exists.

    Conceptually, this sentinel represents a boundary just before the beginning
    of the original histogram.

    The right sentinel solves the "no smaller bar to the right" case.

    Example:

        [1, 2, 3, 4]

    Without a smaller bar at the end, none of these bars would naturally get
    popped.

    Adding the final 0 gives:

        [0, 1, 2, 3, 4, 0]

    The last 0 is smaller than every remaining real bar, so it forces all of
    them to be popped and finalized.

    This removes the need for a separate cleanup loop.

    --------------------------------------------------------------------------
    Example walkthrough
    --------------------------------------------------------------------------

        heights = [2, 1, 5, 6, 2, 3]

    After adding sentinels:

        [0, 2, 1, 5, 6, 2, 3, 0]

    Start with the left sentinel:

        stack values = [0]

    Process 2:

        2 >= 0
        push 2

        stack values = [0, 2]

    Process 1:

        1 < 2

        Pop 2.

        current index = right smaller boundary
        new stack top = left smaller boundary

        width = 2 - 0 - 1 = 1
        area  = 2 * 1 = 2

        Push 1.

        stack values = [0, 1]

    Process 5:

        push 5

        stack values = [0, 1, 5]

    Process 6:

        push 6

        stack values = [0, 1, 5, 6]

    Process 2:

        2 < 6

        Pop 6.

        width = 5 - 3 - 1 = 1
        area  = 6 * 1 = 6

        2 < 5

        Pop 5.

        After popping 5, the stack top corresponds to height 1.

        width = 5 - 2 - 1 = 2
        area  = 5 * 2 = 10

        This represents the rectangle formed by:

            [5, 6]

        whose limiting height is 5 and width is 2.

        Now 2 > 1, so stop popping and push 2.

    Eventually the final sentinel 0 forces all remaining bars to be finalized.

    The largest area found is:

        10

    --------------------------------------------------------------------------
    Reusable invariant
    --------------------------------------------------------------------------

    The stack contains bars whose NEXT smaller element has not been found yet.

    When a shorter bar arrives:

        - pop taller bars
        - current index = their next smaller boundary
        - new stack top = their previous smaller boundary
        - compute their maximum rectangle immediately

    This is the O(N) version of the original brute-force idea of finding the
    first smaller bar on both sides of every bar.

    Time complexity: O(N). Each index is pushed onto the stack once and popped
    at most once, so there are O(N) total stack operations.
    Space complexity: O(N). The monotonic stack can contain O(N) indices.
    """

    heights = [0] + heights + [0]
    stack = []
    res = 0
    for i, height in enumerate(heights):
        while stack and height < heights[stack[-1]]:
            bar = stack.pop()
            # After popping:
            #   stack[-1] = first smaller bar to the left
            #   i         = first smaller bar to the right
            width = i - stack[-1] - 1
            res = max(res, heights[bar] * width)
        stack.append(i)
    return res
