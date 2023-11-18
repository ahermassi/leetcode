""" Given n non-negative integers a1, a2, ..., an , where each represents a point at coordinate (i, ai). n vertical
lines are drawn such that the two endpoints of line i is at (i, ai) and (i, 0). Find two lines, which together with
x-axis forms a container, such that the container contains the most water. """

import unittest2 as unittest


def max_area_v1(height):
    """ Brute force. TLE.
        Simply consider the area for every possible pair of the lines and find out the maximum area out of those.
    Time complexity: O(N^2)
    Space complexity: O(1)
    """
    n, most_water = len(height), float('-inf')
    for i, cur_height in enumerate(height):
        for j in range(i + 1, n):
            most_water = max(most_water, (j - i) * min(cur_height, height[j]))
    return most_water


def max_area_v2(height):
    """ The intuition behind this approach is that the area formed between the lines will always be limited by the
        height of the shorter line: The shorter line is a BOTTLENECK. Moreover, the farther the lines, the greater will
        be the area obtained.

        Initially, we consider the area constituting the exterior most lines. Now, to maximize the area, we need to
        consider the area between the lines of larger lengths. If we try to move the pointer at the longer line inwards,
        we won't gain any increase in area, since it is limited by the shorter line. But moving the shorter line's
        pointer could turn out to be beneficial, as per the same argument, despite the reduction in the width.

        This is done since a relatively longer line obtained by moving the shorter line's pointer might make up for the
        reduction in area caused by the width reduction.

        In other words:

        1- The widest container (using first and last line) is a good candidate because of its width. Its water level
           is the height of the smaller one of first and last line.
        2- All other containers are less wide and thus would need a higher water level in order to hold more water.

        Proof by contradiction: We have two heights H_left and H_right, and H_right < H_left, then we know we have two
        choices: we need to move one of them. If we move the larger one, we cannot increase the height for the simple
        reason that we are always limited by the shortest, and we would be decreasing the width as well.

        Let's say we kept the shortest forever, what would happen? Well, the width would decrease, and
        either we come across a taller block which doesn't matter because our shorter one we kept only mattered, or we
        find a shorter one, in which case that one matters.
        Either way we end up with a smaller area, so we must move the shorter line because moving the larger cannot
        give an increase in area.

        At each state S(i, j), no matter whether the left line or right line moves to the middle, it will decrease
        the width. However:

        If we move the shorter line, min(h[i], h[j]) of the container may hold more water, so the area may increase.
        IF we move the longer line, min(h[i], h[j]) of the container will remain the same or less, so the area will
        definitely decrease.

        Every time we narrow the container the width becomes smaller. So, the only way to get a larger area is
        to find higher lines.

        How can we prove greedy works for all cases and there won't be a case where choosing greedily will fail?
        The reason greedy works in this problem is the following:

        For a container delimited by i and j, where height[i] < height[j], when we increment i, we skip all the
        possible container combinations (i, j-1), (i, j-2)... (i, i+1). All of these lines have height equal to or
        greater than height[i] and width less than j-i. Since the area is (j-i)*min(height[i], height[j]), we couldn't
        have possibly skipped any better solution: the width is shrinking and height[i] is the height BOTTLENECK.
        Therefore, we can just increment the index at the lesser height.

    Time complexity: O(N)
    Space complexity: O(1)
    """
    left, right, max_water = 0, len(height) - 1, float('-inf')
    while left < right:
        left_height, right_height = height[left], height[right]
        max_water = max(max_water, (right - left) * min(left_height, right_height))
        if left_height < right_height:
            left += 1
        else:
            right -= 1
    return max_water


class Test(unittest.TestCase):
    data = [1, 8, 6, 2, 5, 4, 8, 3, 7]
    result = 49

    def test_max_area(self):
        self.assertEqual(self.result, max_area_v1(self.data))
        self.assertEqual(self.result, max_area_v2(self.data))


if __name__ == '__main__':
    unittest.main()
