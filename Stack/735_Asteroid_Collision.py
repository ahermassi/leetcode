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
    Space complexity: O(N)
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


def asteroid_collision_v2(asteroids):
    """ We can make some observations about the asteroids.
        - Negative asteroids without any positive asteroids on the left can be ignored as they will never interact with
        the upcoming asteroids regardless of their direction.
        - Positive asteroids (right-moving) may interact with negative asteroids (left-moving) that come LATER.
        We can iterate through the list of asteroids and handle those scenarios.
        If the asteroid is positive, push it into the stack. It will never interact with existing asteroids in the
        stack but may interact with future negative asteroids.
        If the asteroid is negative, we need to simulate the collision process by repeatedly popping the positive
        smaller asteroids from the top of the stack. We may or may not need to push the negative asteroid to the stack
        depending on the value of the positive asteroids it encounters. Push the negative asteroid if it survives all
        the collisions.
    Time complexity: O(N)
    Space complexity: O(N)
    """
    stack = []
    for asteroid in asteroids:
        if asteroid > 0:
            stack.append(asteroid)
        else:
            while stack and 0 < stack[-1] < abs(asteroid):
                stack.pop()
            if not stack or stack[-1] < 0:  # The asteroid and stack[-1] are both negative, moving in the same direction
                stack.append(asteroid)
            elif abs(asteroid) == abs(stack[-1]):
                stack.pop()
    return stack


class Test(unittest.TestCase):
    data = [([5, 10, -5], [5, 10]),
            ([8, -8], []),
            ([10, 2, -5], [10]),
            ([-2, -1, 1, 2], [-2, -1, 1, 2])]

    def test_asteroid_collision(self):
        for test_asteroids, result in self.data:
            self.assertEqual(result, asteroid_collision_v1(test_asteroids))
            self.assertEqual(result, asteroid_collision_v2(test_asteroids))


if __name__ == '__main__':
    unittest.main()

