""" Given n non-negative integers representing an elevation map where the width of each bar is 1, compute how much
water it is able to trap after raining. """

import unittest2 as unittest


# Great explanation for this solution: https://www.youtube.com/watch?v=HmBbcDiJapY

def trap_v1(height):
    """ For each element in the array, we find the maximum level of water it can trap after the rain, which is equal to
        the minimum of maximum height of bars on both the sides minus its own height.
    Time complexity: O(N^2), for each element of array we iterate the left and right parts
    Space complexity: O(1)
    """
    n, res = len(height), 0
    for i, h in enumerate(height):
        left = right = i
        max_left = max_right = h
        while left >= 0:
            max_left = max(max_left, height[left])
            left -= 1
        while right < n:
            max_right = max(max_right, height[right])
            right += 1
        res += min(max_left, max_right) - h
    return res


class Test(unittest.TestCase):
    data = [([0, 1, 0, 2, 1, 0, 1, 3, 2, 1, 2, 1], 6)]

    def test_trap(self):
        for test_array, result in self.data:
            self.assertEqual(result, trap_v1(test_array))


if __name__ == '__main__':
    unittest.main()
