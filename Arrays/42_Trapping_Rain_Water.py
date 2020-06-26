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


def trap_v2(height):
    """ In the previous solution, we iterate over the left and right parts again and again just to find the highest bar
        size up to current index. However, this could be pre-computed and stored.
        Find maximum height of bar from the left end up to an index i in the 'left_max' map.
        Find maximum height of bar from the right end up to an index i in the array 'right_max' map.
        Therefore, at each index i, the water that can be trapped is:
            min(left_max[i], right_max[i]) − height[i]
    Time complexity: O(N)
    Space complexity: O(N)
    """
    if not height:
        return 0
    n, res = len(height), 0
    left_max, right_max = {0: height[0]}, {n-1: height[-1]}
    for i in range(1, n):
        left_max[i] = max(left_max[i-1], height[i])
    for i in reversed(range(n-1)):
        right_max[i] = max(right_max[i+1], height[i])
    for i, h in enumerate(height):
        max_left, max_right = left_max[i], right_max[i]
        res += min(max_left, max_right) - h
    return res


class Test(unittest.TestCase):
    data = [([0, 1, 0, 2, 1, 0, 1, 3, 2, 1, 2, 1], 6)]

    def test_trap(self):
        for test_array, result in self.data:
            self.assertEqual(result, trap_v1(test_array))
            self.assertEqual(result, trap_v2(test_array))


if __name__ == '__main__':
    unittest.main()
