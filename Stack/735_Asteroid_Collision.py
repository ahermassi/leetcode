""" We are given an array asteroids of integers representing asteroids in a row.
For each asteroid, the absolute value represents its size, and the sign represents its direction (positive meaning
right, negative meaning left). Each asteroid moves at the same speed.
Find out the state of the asteroids after all collisions. If two asteroids meet, the smaller one will explode. If both
are the same size, both will explode. Two asteroids moving in the same direction will never meet. """

import unittest2 as unittest


def asteroid_collision_v1(asteroids):
    """ A row of asteroids is stable if no further collisions will occur. After adding a new asteroid to the right,
        some more collisions may happen before it becomes stable again, and all of those collisions (if they happen)
        must occur right to left. This is the perfect situation for using a stack.
        Say we have our answer as a stack with rightmost asteroid top, and a new asteroid comes in. If new is moving
        right (asteroid > 0), or if top is moving left (stack[-1] < 0), no collision occurs.
        Otherwise, if abs(asteroid) < abs(stack[-1]), then the new asteroid will blow up;
        if abs(asteroid) == abs(stack[-1]), then both asteroids will blow up; and if abs(asteroid) > abs(stack[-1]),
        then the top asteroid will blow up and possibly more asteroids will, so we should continue checking.
    Time complexity: O(N)
    Space complexity:  O(N)
    """
    stack = []
    for asteroid in asteroids:
        while stack and asteroid < 0 and stack[-1] > 0:  # We only need to resolve collisions under the following
            # conditions: 1) Stack is non-empty  2) Current asteroid is negative  3) Top of the stack is positive
            if abs(asteroid) == abs(stack[-1]):  # Both asteroids are equal, destroy both and break
                stack.pop()
                break
            elif abs(asteroid) > stack[-1]:  # Stack top is smaller, remove it and continue the comparison
                stack.pop()
            else:  # Stack top is larger, incoming negative asteroid is destroyed
                break
        else:  # Incoming negative asteroid made it all the way to the bottom of the stack and destroyed all asteroids
            stack.append(asteroid)
    return stack


class Test(unittest.TestCase):
    data = [([5, 10, -5], [5, 10]),
            ([8, -8], []),
            ([10, 2, -5], [10]),
            ([-2, -1, 1, 2], [-2, -1, 1, 2])]

    def test_asteroid_collision(self):
        for test_asteroids, result in self.data:
            self.assertEqual(result, asteroid_collision_v1(test_asteroids))


if __name__ == '__main__':
    unittest.main()

