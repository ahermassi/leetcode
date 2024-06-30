""" There are a number of spherical balloons spread in two-dimensional space. For each balloon, provided input is the
start and end coordinates of the horizontal diameter. Since it's horizontal, y-coordinates don't matter and hence
the x-coordinates of start and end of the diameter suffice. Start is always smaller than end. There will be at most
10^4 balloons.
An arrow can be shot up exactly vertically from different points along the x-axis. A balloon with x_start and x_end
bursts by an arrow shot at x if x_start ≤ x ≤ x_end. There is no limit to the number of arrows that can be shot.
An arrow once shot keeps travelling up infinitely. The problem is to find the minimum number of arrows that must be
shot to burst all balloons. """

import unittest2 as unittest


# Video explanation: https://youtu.be/lPmkKnvNPrw
def find_min_arrow_shots_v1(points):
    """ Similar to 435- Non-overlapping Intervals.

        Finding the minimum number of arrows to shoot is equivalent to finding the maximum number of overlapping
        balloons' diameters.

        Scan the sorted points, and maintain an "active set" for overlapping balloons/diameters. If two diameters
        overlap, we greedily choose to remove the diameter with the biggest end position as the active set needs to
        contain all the balloons that overlap and so is represented by the diameter with smaller end position.

        While considering the points in the ascending order of starting position, we make use of a pointer
        prev_end to keep track of the end position of the previously processed balloon diameter. While traversing, we
        can encounter 3 possibilities:

            - The current and previous diameters are non-overlapping: In this case, we shoot an arrow to burst all
               active balloons, and start to record next active balloons.

            - The current and previous diameters are overlapping and the end position of the current diameter falls
               before the end diameter of the previous diameter: In this case, we can simply take the current diameter.
               Hence, prev_end pointer is updated to current diameter's end position.

            - The current and previous diameters are overlapping and the end position of the current diameter falls
               after the end position of the previous diameter: In this case, prev_end pointer remains unchanged.

        The heuristic is: Always keep the diameter with the smallest end position. This ensures that the active set of
        overlapping balloons hasn't been disrupted, thus the minimal number of arrows to shoot.

        Summary:
        We scan the sorted pairs and maintain a pointer for the minimum end position 'prev_end' for current
        "active balloons" whose diameters are overlapping. When the next balloon starts after 'prev_end' of active
        balloons, we shoot an arrow to burst all active balloons and start to record next active balloons. Otherwise, we
        need to update 'prev_end' to the minimum between current 'prev_end' and the end position of the current balloon
        we've just added to the active set.

    Time complexity: O(N logN)
    Space complexity: O(N), for sort
    """
    points.sort()
    prev_end = float('-inf')
    arrows = 0
    for start, end in points:
        if start > prev_end:
            arrows += 1
            prev_end = end
        else:
            prev_end = min(prev_end, end)
    return arrows


def find_min_arrow_shots_v2(points):
    """ The previous approach was based on choosing points greedily based on the starting position. In this approach, we
        choose greedily based on the end position.

        For this, we sort the given points based on the end position. Then, we traverse the sorted points. We can
         encounter 2 possibilities:

            - The current and previous diameters are non-overlapping: in this case, we shoot an arrow to burst all
               active balloons, and start to record next active balloons.

            - The current and previous diameters are overlapping: we don't need to update prev_end, because the current
               diameter's end position is greater than 'prev_end' (points are sorted by end time).

        Let's consider the following combinations of the balloons: [[10, 16], [2, 8], [1, 6], [7, 12]].
        It's quite obvious that two arrows are enough to burst them all, let's figure out how to compute this result
        with the help of greedy algorithm.

        Let's sort the balloons by the end coordinate, and then check them one by one:
        [[1, 6], [2, 8] [7, 12], [10, 16]]
        The first balloon ends at coordinate 6, and there is no balloons ending before it because of sorting. The other
        balloons have two possibilities:

            - To have a start coordinate smaller than 6, like the second balloon. These could be burst together with the
               first balloon using one arrow.

            - To have a start coordinate larger than 6, like the third balloon. These couldn't be burst together with
               the first balloon using one arrow, and hence we need to increase the number of arrows here.

        That means that we could always track the end of the current balloon, and ignore all the balloons which end
        before it. Once the current balloon is ended (= the next balloon starts after the current balloon), we have to
        shoot a new arrow and start tracking the end of the next active set of balloons.

        What arrow limit should we pick each time? We should shoot as to the right as possible, because since balloons
        are sorted, this gives us the best chance to take down more balloons. Therefore, the arrow limit should always be
        balloon[i][1] for the ith balloon.

        So basically the idea is to sort by end points. This is because the end point decides how many balloons
        intersect when we start moving towards right. If there is no intersection with the next balloon, then this
        balloon needs a new arrow to be burst.

        This solution works because if we sort the intervals by their end point, it will always be optimal to use the
        minimum number of arrows to burst the intervals that end first. This is because, if we have two intervals A and
        B such that A ends before B and we use one arrow to burst A, it means that we cannot use that same arrow to
        burst B, and therefore we must use an additional arrow for B. Therefore, it is always optimal to use the minimum
        number of arrows to burst the intervals that end first.

    Time complexity: O(N logN)
    Space complexity: O(N), for sorting
    """
    points.sort(key=lambda point: point[1])
    prev_end = float('-inf')
    arrows = 0
    for start, end in points:
        if start > prev_end:
            arrows += 1
            prev_end = end
    return arrows


class Test(unittest.TestCase):
    data = [([[10, 16], [2, 8], [1, 6], [7, 12]], 2)]

    def test_find_min_arrow_shots(self):
        for test_points, result in self.data:
            self.assertEqual(result, find_min_arrow_shots_v1(test_points))
            self.assertEqual(result, find_min_arrow_shots_v2(test_points))


if __name__ == '__main__':
    unittest.main()

