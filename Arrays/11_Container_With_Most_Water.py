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
    most_water = float('-inf')
    for i, v in enumerate(height):
        for j in range(i + 1, len(height)):
            most_water = max(most_water, (j - i) * min(v, height[j]))
    return most_water


def max_area_v2(height):
    """ The intuition behind this approach is that the area formed between the lines will always be limited by the
        height of the shorter line. Further, the farther the lines, the more will be the area obtained. Initially we
        consider the area constituting the exterior most lines. Now, to maximize the area, we need to consider the area
        between the lines of larger lengths. If we try to move the pointer at the longer line inwards, we won't gain any
        increase in area, since it is limited by the shorter line. But moving the shorter line's pointer could turn out
        to be beneficial, as per the same argument, despite the reduction in the width. This is done since a relatively
        longer line obtained by moving the shorter line's pointer might overcome the reduction in area caused by the
        width reduction.
        In other words:
        1- The widest container (using first and last line) is a good candidate, because of its width. Its water level
        is the height of the smaller one of first and last line.
        2- All other containers are less wide and thus would need a higher water level in order to hold more water.
        Proof by contradiction: We have two heights H_left and H_right, and H_right < H_left, then we know we have two
        choices, we want to move one of them. If we move the larger one, we cannot increase the height for the simple
        reason that we are always limited by the shortest, and we would be decreasing j-i, the width as well.
        To clarify: let's say we kept the shortest forever, what would happen? Well, j-i would decrease, and either we
        come across a taller block, which doesn't matter because our shorter one we kept only mattered, or we find a
        shorter one, in which case that one matters.
        Either way we end up with a smaller area, so we must move the shorter one because moving the larger one cannot
        give an increase in area.
    Time complexity: O(N)
    Space complexity: O(1)
    """
    left, right, max_water = 0, len(height) - 1, float('-inf')
    while left < right:
        max_water = max(max_water, (right - left) * min(height[left], height[right]))
        if height[left] < height[right]:
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
