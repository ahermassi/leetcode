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


def find_min_arrow_shots_v2(points):
    """ We can also sort the balloons in increasing order of the start position. We then scan the sorted pairs, and
        maintain a pointer for the minimum end position 'arrow_limit' for current "active balloons" whose diameters
        are overlapping. When the next balloon starts after the 'arrow_limit' of active balloons, we shoot an arrow to
        burst all active balloons, and start to record next active balloons. Otherwise, we need to update 'arrow_limit'
        to be the minimum between current 'arrow_limit' and the end position of the current balloon we've just added.
        The so-called Overlapping Interval Problems share some similarities in their solutions:
            - Sort intervals/pairs in increasing order of the start position.
            - Scan the sorted intervals, and maintain an "active set" for overlapping intervals. At most times, we do
              not need to use an explicit set to store them. Instead, we just need to maintain several key parameters,
              e.g. the number of overlapping intervals (count), the minimum ending point among all overlapping intervals
              (min_end).
            - If the interval that we are currently checking overlaps with the active set, which can be characterized
              by cur.start > min_end, we need to renew those key parameters or change some states.
            - If the current interval does not overlap with the active set, we just drop current active set, record
              some parameters, and create a new active set that contains the current interval.
    Time complexity: O(N logN)
    Space complexity: O(N)
    """
    if not points:
        return 0
    points.sort()
    arrow_limit, res = points[0][1], 1
    for start, end in points:
        if start <= arrow_limit:
            arrow_limit = min(arrow_limit, end)
        else:
            arrow_limit = end
            res += 1
    return res


class Test(unittest.TestCase):
    data = [([[10, 16], [2, 8], [1, 6], [7, 12]], 2)]

    def test_find_min_arrow_shots(self):
        for test_points, result in self.data:
            self.assertEqual(result, find_min_arrow_shots_v1(test_points))
            self.assertEqual(result, find_min_arrow_shots_v2(test_points))


if __name__ == '__main__':
    unittest.main()

