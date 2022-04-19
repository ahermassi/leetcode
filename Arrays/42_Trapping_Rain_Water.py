""" Given n non-negative integers representing an elevation map where the width of each bar is 1, compute how much
water it is able to trap after raining. """

import unittest2 as unittest


# Great explanation for this solution: https://www.youtube.com/watch?v=HmBbcDiJapY

def trap_v1(height):
    """ For each element in the array, we find the maximum level of water it can trap after the rain, which is equal to
        the minimum of maximum height of bars on both the sides minus its own height.

        The ith bar can trap water if and only if there exists a higher bar to the left and a higher bar to the right
        of it. To calculate how much amount of water the ith bar can trap, we need to look at the maximum height
        of the left bar and the maximum height of the right bar, then the water level that can be formed at ith bar is:

                water_level = min(max_left[i], max_right[i])

        If water_level >= height[i] then ith bar can trap:

                amount of water = water_level - height[i]

    Time complexity: O(N^2), for each element of array we iterate the left and right parts
    Space complexity: O(1)
    """
    n, res = len(height), 0
    for i, cur_height in enumerate(height):
        left = right = i
        max_left = max_right = 0
        while left >= 0:
            max_left = max(max_left, height[left])
            left -= 1
        while right < n:
            max_right = max(max_right, height[right])
            right += 1
        res += min(max_left, max_right) - cur_height
    return res

# Great explanation for this solution: https://www.youtube.com/watch?v=VZpJxINSvfs


def trap_v2(height):
    """ In the previous solution, we iterate over the left and right parts again and again just to find the highest bar
        size up to current index. However, this could be pre-computed and stored.
        Find maximum height of bar from the left end up to an index i in the 'left_max' array.
        Find maximum height of bar from the right end up to an index i in the array 'right_max' array.
        Therefore, at each index i, the water that can be trapped is:
            min(left_max[i], right_max[i]) − height[i]
    Time complexity: O(N)
    Space complexity: O(N)
    """
    if not height:
        return 0
    n, res = len(height), 0
    left_max, right_max = [0] * n, [0] * n
    left_max[0], right_max[-1] = height[0], height[-1]
    for i in range(1, n):
        left_max[i] = max(left_max[i-1], height[i])
    for i in reversed(range(n-1)):
        right_max[i] = max(right_max[i+1], height[i])
    for i, cur_height in enumerate(height):
        max_left, max_right = left_max[i], right_max[i]
        res += min(max_left, max_right) - cur_height
    return res


def trap_v3(height):
    """ Instead of computing the left and right parts separately, we may think of some way to do it in one iteration.
        Notice that as long as left_max[i] < right_max[i], the water trapped depends upon 'left_max', and similar is
        the case when right_max[i] < left_max[i]. So, we can say that if there is a larger bar at one end (say right),
        we are assured that the water trapped would be dependant on height of (left) bar in current direction (from
        left to right). As soon as we find out that the bar at other end (right) is smaller, we start iterating in
        opposite direction (from right to left). We must maintain 'left_max' and 'right_max' during the iteration, but
        now we can do it in one iteration using 2 pointers, switching between the two.
        If 'left_max' is smaller, use left bar as current container rim.
        If 'right_max' is smaller, use right bar as current container rim.
        In other words:
        We calculate the stored water at each index. At the start of every iteration, we update the current maximum
        height from left side (that is from height[:left]) and the maximum height from right side (from height[right:]).
        If left_max < right_max, then at least (left_max- height[left]) water can definitely be stored no matter what
        exists between [left, right] since we know there is a barrier at the right side (left_max < right_max).
        On the other hand, we cannot store more water than (left_max - height[left]) at index 'left' since the left
        barrier is of height 'left_max'. So, we know the water that can be stored at index 'left' is exactly
        (left_max - height[left]). The same logic applies to the case when right_max < left_max. At each loop we can
        make 'left' and 'right' one step closer.
    Time complexity: O(N)
    Space complexity: O(1)
    """
    left, right = 0, len(height) - 1
    left_max = right_max = 0
    res = 0
    while left < right:
        left_max = max(left_max, height[left])
        right_max = max(right_max, height[right])
        if left_max < right_max:
            res += left_max - height[left]  # We know that we can fill the current point with water up to the previous
            # left maximum as any more will overflow
            left += 1
        else:
            res += right_max - height[right]
            right -= 1
    return res


class Test(unittest.TestCase):
    data = [([0, 1, 0, 2, 1, 0, 1, 3, 2, 1, 2, 1], 6)]

    def test_trap(self):
        for test_array, result in self.data:
            self.assertEqual(result, trap_v1(test_array))
            self.assertEqual(result, trap_v2(test_array))
            self.assertEqual(result, trap_v3(test_array))


if __name__ == '__main__':
    unittest.main()
