""" Given n non-negative integers representing the histogram's bar height where the width of each bar is 1, find the
area of largest rectangle in the histogram. """

import unittest2 as unittest


def largest_rectangle_area_v1(heights):
    """  Brute Force. TLE.

         We can simply start off by considering every possible pair of bars and finding the area of the rectangle formed
         between them using the height of the shortest bar lying between them as the height and the spacing between them
         as the width of the rectangle. We can thus, find the required rectangle with the maximum area.

    Time complexity: O(N^2)
    Space complexity: O(1)
    """
    n, res = len(heights), 0
    for i in range(n):
        min_height = heights[i]
        for j in range(i, n):
            min_height = min(min_height, heights[j])
            res = max(res, min_height * (j - i + 1))
    return res


# Video explanation (set speed to 1.25x): https://www.youtube.com/watch?v=RVIh0snn4Qc
# Video explanation: https://www.youtube.com/watch?v=zx5Sw9130L0
def largest_rectangle_area_v2(heights):
    """ First, we need to take into account the fact that the height of the rectangle formed between any two bars
         will always be limited by the height of the shortest bar lying between them.

         For any bar at index i, the maximum rectangle is of width r-l+1, where r is the index of the rightmost
         SUBSEQUENT bar with height h[r] >= h[i] (contiguous bars), and l is the index of the leftmost SUBSEQUENT bar
         with height h[l] >= h[i] (see the first comment on this thread:
         https://leetcode.com/problems/largest-rectangle-in-histogram/discuss/28902/5ms-O(n)-Java-solution-explained-(beats-96)).
         These two particular bars represent the expansion boundaries of the rectangle which the ith bar be part of
         because a rectangle can only be formed using contiguous neighboring bars to the right and to the left with
         heights greater than or equal to the ith bar's height.

         NOTE: for the rest of the explanation, leftmost/rightmost refer to leftmost subsequent / rightmost subsequent.

         So for any index i, if we know its utmost higher (or of the same height) neighbors to the right and to
         the left, we can easily find the largest rectangle using:

                    maxArea = max(maxArea, height[i] * (greaterOrEqualFromRight[i] - greaterOrEqualFromLeft[i] + 1))

         The trick is how to effectively calculate greaterOrEqualFromRight and greaterOrEqualFromLeft.

         The basic idea behind this algorithm is that we would like to calculate the maximum rectangle for every
         bar at index i with width r-l+1 and height heights[i], where r / l is the index of the rightmost / leftmost bar
         with height greater than or equal to bar i. Once we get the maximum rectangle for every bar, the result could
         be derived by choosing the largest maximum rectangle.

         Calculating and storing l and r will be too cumbersome, so a stack is introduced here.

        At each step, we need the information of previously seen 'candidate' bars - bars which give us hope of
        expansion. These are the bars of increasing heights. And since they'll need to be put in the order of their
        occurrence, a stack should come to mind.

         We process the bars from left to right and keep pushing indices to the stack as long as the corresponding
         heights are in increasing order. As soon as we encounter a bar with a height that disrupts the increasing order
         at index i, it's stime to pause and reflect.

         With a shorter bar B1 in hand, the bars in the stack have no hope of further expansion to the right.
         Therefore, we need to pop them one by one and calculate the maximum area of the rectangle that they can be
         part of.

        The previous bar B2 index is stack.pop(). The current index i is the index of the first bar to the right
        of B2 with lower height, and stack[-1] is the index of the first bar B3 to the left of B2 with less height than
        B2 after popping B2 (remember that the stack if monotonically increasing). Thus, B1 and B3 represent,
        respectively, the right and the left boundaries of the largest rectangle that B2 can be part of.

         So, before adding the new bar B1 to the stack, we pop the bar(s) that is/are taller than B1. The popped bar(s)
         represents the height of a rectangle with B1 as the right boundary and the current stack's top as the left
         boundary.

         So the idea is that, when we encounter a shorter bar at index i, then for each bar B in the monotonically
         increasing stack:

             1- Take its height as the rectangle's height, then find the left and right boundaries of this rectangle
             2- The bar at current index i is always the rightmost bar lower than B
             3- The top of the stack is always the leftmost bar lower than B (after popping B). Let's call the index j.
             4- After steps 2 and 3, we know the left and right boundaries, then know the width, then can calculate
                  the area.
                  width = (i - 1) - (j+1) + 1 = i - 1 - j - 1 + 1 = i - j - 1

         Why i-1? The bar to the right at current index i can't be part of the rectangle because it's... well, lower.
         Why j+1? The bar to the left at index j can't be part of the rectangle because it's... well, lower.

         So the algorithm boils down to:

            - Maintain a stack such that heights are always in increasing order.
            - When we see a bar that's lower than the top of the stack, we use it as the right side and compute all the
               possible rectangles using what's on the stack to derive left side and height.
            - Remove each considered rectangle / bar from the stack.

         We append a dummy 0 to either side of the list of heights for the following reasons:

         Without the [0] appended to the end of the list of heights, we would need to basically repeat what we did in
         the inner while loop once at the very end of the algorithm in case there are bars left in the stack (for
         example, when the input list of heights is strictly increasing). With the dummy 0 at the end, however, every
         element left in the stack will have a height >= 0, and so they will be popped and included in the calculation.
         So the [0] is used to "force pop" all the remaining elements in the stack.

        Without the dummy 0 added to the start of the list, we wouldn't be able to calculate the maximum area of
        rectangle when the input list of heights has a single element.

        Check the first comment on this thread for a walk through example:
         https://leetcode.com/problems/largest-rectangle-in-histogram/discuss/28900/Short-and-Clean-O(n)-stack-based-JAVA-solution

         Example: heights = [2, 1, 5, 6, 2, 3]

         Let's take the bar at index 4 with height 2.

         When i=4, the top of stack is bar(6). If we take bar(6) as the current height of the rectangle, we need to find
         the left and right boundary bars of the rectangle. It is always true that both left and right boundary bars have
         heights either equal to or greater than bar(6).

         Right Boundary: bar(2), which i points to, is the rightmost bar that is lower than bar(6), so the right boundary
         is i-1.
        Left Boundary: bar(5), which is the top in stack after bar(6) is popped, is the leftmost bar that is lower than
        bar(6), so the left boundary is stack.peek()+1.

         Now we have both left and right boundaries, then let's get the width of the rectangle:
         width = index of right boundary - index of left boundary + 1 = (i - 1) - (stack.peek() + 1) + 1 =
         i - stack.peek() - 1
         Then the area = (height of bar(6)) * (i - stack.peek() - 1).

         Let's move to the next iteration. The top of the stack is bar(5), and i still points to bar(2). So we pop bar(5)
         and take bar(5)'s height as the rectangle's height.

         Right Boundary: bar(2) is the rightmost bar that is lower than bar(5). Then the right boundary is i-1.
         Left Boundary: bar(1), which is the top in stack after bar(5) is popped, is the leftmost bar that is lower than
         bar(5). So the left boundary is stack.peek()+1.

         width = (i - 1) - (stack.peek() + 1) = i - stack.peek() - 1 and
         area = (height of bar(5)) * (i - stack.peek() - 1).

         There is only bar(1) left in the stack, and it is lower than bar(2), to which i points. So we continue pushing
         bars to the stack till the height starts to decrease or the end of the histogram.

         Now the stack has [bar(1), bar(2), bar(3)] and bar(3) is in the top. i points to the position of the right
         bar(3).
         We pop bar(3) out of the stack and take its height as the rectangle's height. The right boundary is i-1.
         The left boundary is bar(2) which is stack.peek()+1.

         Next, pop bar(2) and take its height as the rectangle's height. Remember that the boundary's height is either
         equal to or larger than bar(2)'s height. The right boundary is bar(3), which is i-1. The left boundary is
         bar(1)'s right which is stack.peek()+1.

    Time complexity: O(N), each height is pushed and popped once
    Space complexity: O(N)
    """
    heights.append(0)
    heights = [0] + heights
    heights.append(0)  # Append 0 to heights to ensure that it pops out all previous heights from the stack
    stack = []
    res = 0
    for i, height in enumerate(heights):
        while stack and height < heights[stack[-1]]:
            # As long as the current bar is shorter than the one at the top of the stack, we keep popping out the stack
            # and calculate the area based on the popped bar
            index = stack.pop()
            w = i - stack[-1] - 1
            res = max(res, heights[index] * w)
        # We'll need to consider the rectangle of height 'height'. We don't know how far to the right this rectangle
        # will extend, so we'll just push i to the stack.
        stack.append(i)
    return res


class Test(unittest.TestCase):
    data = [([2, 1, 5, 6, 2, 3], 10)]

    def test_largest_rectangle_area(self):
        for test_heights, result in self.data:
            self.assertEqual(result, largest_rectangle_area_v1(test_heights))
            self.assertEqual(result, largest_rectangle_area_v2(test_heights))


if __name__ == '__main__':
    unittest.main()
