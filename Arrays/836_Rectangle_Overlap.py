""" A rectangle is represented as a list [x1, y1, x2, y2], where (x1, y1) are the coordinates of its bottom-left
corner, and (x2, y2) are the coordinates of its top-right corner.
Two rectangles overlap if the area of their intersection is positive.  To be clear, two rectangles that only touch at
the corner or edges do not overlap.
Given two (axis-aligned) rectangles, return whether they overlap. """

import unittest2 as unittest


def is_rectangle_overlap_v1(rec1, rec2):
    """ Focus on conditions under which it can be guaranteed that the rectangles do NOT intersect. If the rectangles do
        not overlap, then rec1 must either be higher, lower, to the left, or to the right of rec2.
        The answer for whether they don't overlap is LEFT OR RIGHT OR UP OR DOWN, where LEFT is a boolean that
        represents whether rec1 is to the left of rec2. The answer for whether they do overlap is the negation of this.
    Time complexity: O(1)
    Space complexity: O(1)
    """
    left1, bottom1, right1, top1 = rec1
    left2, bottom2, right2, top2 = rec2
    return not (right1 <= left2 or left1 >= right2 or bottom1 >= top2 or top1 <= bottom2)


class Test(unittest.TestCase):
    data = [([0, 0, 2, 2], [1, 1, 3, 3], True), ([0, 0, 1, 1], [1, 0, 2, 1], False)]

    def test_is_rectangle_overlap(self):
        for test_rec1, test_rec2, result in self.data:
            self.assertEqual(result, is_rectangle_overlap_v1(test_rec1, test_rec2))
            # self.assertEqual(result, is_rectangle_overlap_v2(test_rec1, test_rec2))


if __name__ == '__main__':
    unittest.main()
