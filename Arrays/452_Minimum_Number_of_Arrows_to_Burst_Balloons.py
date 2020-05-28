""" There are a number of spherical balloons spread in two-dimensional space. For each balloon, provided input is the
start and end coordinates of the horizontal diameter. Since it's horizontal, y-coordinates don't matter and hence
the x-coordinates of start and end of the diameter suffice. Start is always smaller than end. There will be at most
10^4 balloons.
An arrow can be shot up exactly vertically from different points along the x-axis. A balloon with x_start and x_end
bursts by an arrow shot at x if x_start ≤ x ≤ x_end. There is no limit to the number of arrows that can be shot.
An arrow once shot keeps travelling up infinitely. The problem is to find the minimum number of arrows that must be
shot to burst all balloons. """

import unittest2 as unittest


def find_min_arrow_shots_v1(points):
    """ The idea of greedy algorithm is to pick the locally optimal move at each step, that will lead to the globally
        optimal solution.
        Let's consider the following combinations of the balloons: [[10, 16], [2, 8], [1, 6], [7, 12]].
        That's quite obvious that two arrows is enough to burst them all, let's figure out how to compute this result
        with the help of greedy algorithm.
        Let's sort the balloons by the end coordinate, and then check them one by one:
        [[1, 6], [2, 8] [7, 12], [10, 16]]
        The first balloon ends at coordinate 6, and there is no balloons ending before it because of sorting. The other
        balloons have two possibilities:
            - To have a start coordinate smaller than 6, like the second balloon. These ones could be burst together
              with the first balloon by one arrow.
            - To have a start coordinate larger than 6, like the third balloon. These ones couldn't be burst together
              with the first balloon by one arrow, and hence we need to increase the number of arrows here.
        That means that we could always track the end of the current balloon, and ignore all the balloons which end
        before it. Once the current balloon is ended (= the next balloon starts after the current balloon), we have to
        increase the number of arrows by one and start to track the end of the next balloon.
        What arrow limit should we pick each time? We should shoot as to the right as possible, because since balloons
        are sorted, this gives us the best chance to take down more balloons. Therefore the arrow limit should always be
        balloon[i][1] for the ith balloon.
        So basically the idea is to sort by end points. This is because the end point decides how many balloons
        intersect when we start moving towards right. If there is no intersection with the next balloon, then this
        balloon needs a new arrow to be burst.
    Time complexity: O(N logN)
    Space complexity: O(N), for sorting
    """
    if not points:
        return 0
    points.sort(key=lambda interval: interval[1])
    arrow_limit, count = points[0][1], 1
    for start, end in points:
        if start > arrow_limit:  # If the current balloon starts after the end of another one, we need one more arrow
            arrow_limit = end
            count += 1
    return count


class Test(unittest.TestCase):
    data = [([[10, 16], [2, 8], [1, 6], [7, 12]], 2)]

    def test_find_min_arrow_shots(self):
        for test_points, result in self.data:
            self.assertEqual(result, find_min_arrow_shots_v1(test_points))


if __name__ == '__main__':
    unittest.main()

