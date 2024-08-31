""" Given n non-negative integers representing an elevation map where the width of each bar is 1, compute how much
water it is able to trap after raining. """

import unittest2 as unittest


# Video explanation: https://www.youtube.com/watch?v=HmBbcDiJapY
def trap_v1(height):
    """ For each element in the array, we find the maximum level of water it can trap after the rain, which is equal to
         the minimum of maximum height of bars on both the sides minus its own height.

         The ith bar can trap water if and only if there exists a higher bar to its left and a higher bar to its right.
         To calculate how much amount of water the ith bar can trap, we need to look at the maximum height of the left
         bar and the maximum height of the right bar, then the water level that can be formed at ith bar is:

                     water_level[i] = min(max_left[i], max_right[i])

         If water_level[i] >= height[i] then ith bar can trap:

                     amount of water[i] = water_level[i] - height[i]

    Time complexity: O(N^2), for each element of the array we iterate the left and right parts
    Space complexity: O(1)
    """
    n, res = len(height), 0
    for i, cur_height in enumerate(height):
        left = right = i
        max_left = max_right = height[i]
        while left >= 0:
            max_left = max(max_left, height[left])
            left -= 1
        while right < n:
            max_right = max(max_right, height[right])
            right += 1
        res += min(max_left, max_right) - cur_height
    return res


# Video explanation: https://www.youtube.com/watch?v=VZpJxINSvfs
def trap_v2(height):
    """ In the previous solution, we iterate over the left and right parts again and again just to find the highest bar
         size up to the current index. However, this could be pre-computed and stored.

         Find the maximum height of bars from the left up to AND INCLUDING index i in the left_max array.
         Find the maximum height of bars from the right up to AND INCLUDING index i in the right_max array.

         Therefore, at each index i, the water that can be trapped is:

                    amount of water[i] =min(max_left[i], max_right[i]) − height[i]

         !!! IMPORTANT !!!
         If instead we were to calculate the maximum heights from the left and from the right if each index EXCLUDING
         that index, the equation would have to change to:

                    amount of water[i] = max(0, min(max_left[i], max_right[i]) − height[i])

        to account for the case where a bar has only one higher bar to either end or none at all, in which case the
        amount of water the bar can trap is 0.


    Time complexity: O(N)
    Space complexity: O(N)
    """
    n, res = len(height), 0
    max_left, max_right = [0] * n, [0] * n
    max_left[0], max_right[-1] = height[0], height[-1]
    for i in range(1, n):
        max_left[i] = max(max_left[i-1], height[i])
    for i in reversed(range(n-1)):
        max_right[i] = max(max_right[i+1], height[i])
    for i, cur_height in enumerate(height):
        res += min(max_left[i], max_right[i]) - cur_height
    return res


# Video explanation: https://youtu.be/ZI2z5pq0TqA?t=660
def trap_v3(height):
    """ Instead of computing the left and right parts separately, we may think of some way to do it in one iteration.

         Notice that as long as max_left[i] < max_right[i], the water trapped depends upon max_left ONLY, and similar
         is the case when max_right[i] < max_left[i]. So, we can say that if there is a larger bar at one end, say
         right for example, we are assured that the water trapped would be dependent on height of the left bar in
         current direction (from left to right).
         As soon as we find out that the bar at the other end, which is right in this example, is smaller, we start
         iterating in opposite direction (from right to left).

         We must maintain max_left and max_right during the iteration, but now we can do it in one iteration
         using 2 pointers, switching between the two.

        If max_left is smaller, use left bar as current container rim.
        If max_right is smaller, use right bar as current container rim.

         In other words:

         We calculate the stored water at each index 'left' and 'right'. At the start of every iteration, we update
         the current maximum height from left side (that is from height[:left+1]) and the maximum height from right side
         (from height[right:]).

         If max_left < max_right, then AT LEAST (min(max_left, max_right) - height[left]) = (max_left- height[left])
         water can definitely be stored no matter what exists between [left, right] since we know there is a barrier on
         the right side (max_left < max_right).
         On the other hand, we cannot store more water than (max_left - height[left]) at index 'left' since the left
         barrier is of height max_left. So, we know the water that can be stored at index 'left' is exactly
         (max_left - height[left]).
         The same logic applies to the case when max_right < max_left.

        At each iteration, we can make 'left' and 'right' one step closer.

        !!! IMPORTANT !!!
        Since left and right pointers scan the entire [0, n-1] interval, we're sure the trapped water is calculated for
        all the bars by the end of the algorithm.
        The key point is that any bars between max_left and max_right bars will NOT influence how much water the
        current position can trap.
        For example, left=3, right=7, max_left < max_right. We KNOW that the maximum bar height up to AND INCLUDING
        index left is exactly max_left. However, max_right is the maximum bar height STARTING FROM index right. But what
        about all the bars between [left+1, right-1]?? They don't matter! Remember the equation:

                    amount of water[i] = min(max_left[i], max_right[i]) − height[i]

        The lowest of the highest bars is the BOTTLENECK. In this example, max_left is the bottleneck. Therefore,
        min(max_left[i], max_right[i]) will always resolve to max_left[i], or max_left for i=left, no matter what's
        between [left+1, right-1], as we try to MINIMIZE.

    Time complexity: O(N)
    Space complexity: O(1)
    """
    left, right = 0, len(height) - 1
    max_left = max_right = 0
    res = 0
    while left < right:
        max_left = max(max_left, height[left])
        max_right = max(max_right, height[right])
        # How much water the current position can trap depends on the shorter bar
        if max_left < max_right:
            # We know that we can fill the current point with water up to the previous left maximum as any more than
            # that limit will overflow
            res += max_left - height[left]
            left += 1
        else:
            res += max_right - height[right]
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
