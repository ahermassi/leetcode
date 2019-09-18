""" We are given an array asteroids of integers representing asteroids in a row.
For each asteroid, the absolute value represents its size, and the sign represents its direction (positive meaning
right, negative meaning left). Each asteroid moves at the same speed.
Find out the state of the asteroids after all collisions. If two asteroids meet, the smaller one will explode. If both
are the same size, both will explode. Two asteroids moving in the same direction will never meet. """

import unittest2 as unittest


def asteroid_collision(asteroids):
    """ This is a recursive solution. The recursion arises because whenever a collision happens, the same logic/process
        needs to be applied to the remaining stack elements in order to detect further collisions. In other words, a
        collision might trigger another collision, and so on and so forth, even before a 'new' asteroid comes into play.
    Time complexity: O(N)
    Space complexity:  O(N)
    """

    def collide(asteroid, stack):
        if not stack or asteroid * stack[-1] > 0:
            stack.append(asteroid)
        elif stack[-1] > 0 and asteroid < 0:
            if stack[-1] == abs(asteroid):  # Asteroids of same size cancel each other
                stack.pop()
            elif abs(asteroid) > stack[-1]:  # This is where a recursion might appear: a collision is detected
                stack.pop()
                collide(asteroid, stack)
        else:
            stack.append(asteroid)

    stack = []
    for asteroid in asteroids:
        collide(asteroid, stack)
    return stack


class Test(unittest.TestCase):
    data = [([5, 10, -5], [5, 10]),
            ([8, -8], []),
            ([10, 2, -5], [10]),
            ([-2, -1, 1, 2], [-2, -1, 1, 2])]

    def test_asteroid_collision(self):
        for test_asteroids, result in self.data:
            self.assertEqual(result, asteroid_collision(test_asteroids))


if __name__ == '__main__':
    unittest.main()

