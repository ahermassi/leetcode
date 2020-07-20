""" Given n non-negative integers representing the histogram's bar height where the width of each bar is 1, find the
area of largest rectangle in the histogram. """

import unittest2 as unittest


# Video explanation (set speed to 1.25x lol): https://www.youtube.com/watch?v=RVIh0snn4Qc

def largest_rectangle_area(heights):
    """ Firstly, we need to take into account the fact that the height of the rectangle formed between any two bars
        will always be limited by the height of the shortest bar lying between them.
        For any bar i, the maximum rectangle is of width (r-l-1), where r is the first coordinate of the bar to the
        right with height h[r] < h[i] and l is the first coordinate of the bar to the left with height h[l] < h[i]
        (See first comment on this thread:
        https://leetcode.com/problems/largest-rectangle-in-histogram/discuss/28902/5ms-O(n)-Java-solution-explained-(beats-96))
        So if for any i coordinate, if we know its utmost higher (or of the same height) neighbors to the right and to
        the left, we can easily find the largest rectangle using:
            maxArea = max(maxArea, height[i] * (lessFromRight[i] - lessFromLeft[i] - 1))
        The main trick is how to effectively calculate lessFromRight and lessFromLeft.
        So, the basic idea behind this algorithm is that we would like to calculate the maximum rectangle for every
        bar i with width (r-l-1) and height heights[i], where r / l is the index of the first bar in right / left with
        height lower than bar i. Once we got the maximum rectangle for every bar, the result could be derived by
        choosing the largest maximum rectangle. Calculating and storing l and r will be too cumbersome, so a stack is
        introduced here. At each step, we need the information of previously seen 'candidate' bars - bars which give us
        hope. These are the bars of increasing heights. And since they'll need to be put in the order of their
        occurrence, stack should come to mind.
        The current bar index is stack.pop(); i is the index of first bar in the right with height lower than current
        bar, and stack[-1] is the index of first bar in the left with height not higher than current bar. The stack
        maintains the indices of buildings in ascending height. Before adding a new building, we pop the building that
        is taller than the new one. The building popped out represents the height of a rectangle with the new building
        as the right boundary and the current stack top as the left boundary. Right boundary is handled using a dummy
        building of height 0.
        So the idea is that:
            1- For each bar, take its height as the rectangle's height, then find the left and right boundaries of this
               rectangle
            2- (The second top bar in stack) is always the first bar lower than (the top bar in stack) on the left
            3- (The bar that i points to) is always the first bar lower than (the top bar in stack) on the right
            4- After steps 2 and 3, we know the left and right boundaries, then know the width, then know the area
        Check out the first comment on this thread for a walk through example:
        https://leetcode.com/problems/largest-rectangle-in-histogram/discuss/28900/Short-and-Clean-O(n)-stack-based-JAVA-solution
    Time complexity: O(N), each height is pushed and popped once
    Space complexity: O(N)
    """
    heights.append(0)  # Append 0 to heights to ensure that it pops out all previous heights from the stack
    n, res, stack = len(heights), 0, [-1]
    for i, height in enumerate(heights):
        while heights[stack[-1]] > height:  # As long as the current bar is shorter than the last one in the stack, we
            # keep popping out the stack and calculate the area based on the popped bar
            h = heights[stack.pop()]
            w = i - stack[-1] - 1
            res = max(res, h * w)
        stack.append(i)  # Push current bar's index to the stack
    return res


class Test(unittest.TestCase):
    data = [([2, 1, 5, 6, 2, 3], 10)]

    def test_largest_rectangle_area(self):
        for test_heights, result in self.data:
            self.assertEqual(result, largest_rectangle_area(test_heights))


if __name__ == '__main__':
    unittest.main()
