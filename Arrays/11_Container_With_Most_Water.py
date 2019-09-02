""" Given n non-negative integers a1, a2, ..., an , where each represents a point at coordinate (i, ai). n vertical
lines are drawn such that the two endpoints of line i is at (i, ai) and (i, 0). Find two lines, which together with
x-axis forms a container, such that the container contains the most water. """

import unittest2 as unittest


def max_area_v1(height):
    """ Brute force. TLE.
        Simply consider the area for every possible pair of the lines and find out the maximum area out of those.
    Time complexity: O(N ** 2)
    Space complexity: O(1)
    """
    most_water = float('-inf')
    for i, v in enumerate(height):
        for j in range(i + 1, len(height)):
            most_water = max(most_water, (j - i) * min(v, height[j]))
    return most_water


class Test(unittest.TestCase):
    data = [1, 8, 6, 2, 5, 4, 8, 3, 7]
    result = 49

    def test_max_area(self):
        self.assertEqual(self.result, max_area_v1(self.data))


if __name__ == '__main__':
    unittest.main()
