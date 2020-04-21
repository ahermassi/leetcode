""" Given a set of points in the xy-plane, determine the minimum area of a rectangle formed from these points, with
sides parallel to the x and y axes.
If there isn't any rectangle, return 0. """

import unittest2 as unittest


def min_area_rect_v1(points):
    """ For each pair of points in the array, consider them to be the diagonal of a potential rectangle. We can check
        if all 4 points are there using a set.
        For example, if the points are (1, 1) and (5, 5), we check if we also have (1, 5) and (5, 1). If we do, we have
        a candidate rectangle.
        Put all the points in a set. For each pair of points, if the associated rectangle are 4 distinct points all in
        the set, then take the area of this rectangle as a candidate answer.
        Go through all the points in two loops (x1, y1) and (x2, y2) while checking if (x1, y2) and (x2, y1) are also
        valid points. If so, we found a rectangle.
    Time complexity: O(N^2), where N is the number of points
    Space complexity: O(N)
    """
    points_map, res = set(), float('inf')
    for x, y in points:
        points_map.add((x, y))
    for x1, y1 in points_map:
        for x2, y2 in points_map:
            if x2 > x1 and y2 > y1:  # Calculate each diagonal pair once by discarding the other two points for future
                # check, because they in turn will find current two points as their diagonal points and hence will lead
                # to the SAME rectangle. Without this condition, the area of the rectangle whose diagonal is (1, 1) and
                # (5, 5) will be calculated twice: When (x1, y1) = (1, 1) and when (x1, y1) = (5, 5)
                if (x1, y2) in points_map and (x2, y1) in points_map:
                    res = min(res, (x2 - x1) * (y2 - y1))
    return res if res != float('inf') else 0  # If there isn't any rectangle, return 0.


class Test(unittest.TestCase):
    data = [([[1, 1], [1, 3], [3, 1], [3, 3], [2, 2]], 4), ([[1, 1], [1, 3], [3, 1], [3, 3], [4, 1], [4, 3]], 2)]

    def test_min_area_rect(self):
        for test_points, result in self.data:
            self.assertEqual(result, min_area_rect_v1(test_points))


if __name__ == '__main__':
    unittest.main()
