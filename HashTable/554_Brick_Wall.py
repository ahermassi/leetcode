""" There is a brick wall in front of you. The wall is rectangular and has several rows of bricks. The bricks have the
same height but different width. You want to draw a vertical line from the top to the bottom and cross the least bricks.
The brick wall is represented by a list of rows. Each row is a list of integers representing the width of each brick in
this row from left to right.
If your line goes through the edge of a brick, then the brick is not considered as crossed. You need to find out how to
draw the line to cross the least bricks and return the number of crossed bricks.
You cannot draw a line just along one of the two vertical edges of the wall, in which case the line will obviously
cross no bricks. """

from collections import defaultdict
import unittest2 as unittest


def least_bricks(wall):
    """ For each potential cut position - which is at the edge of any brick, we count the number of brick edges for all
        rows. We make use of a hash map 'width' which is used to store entries in the form: (cur_width, count). Here,
        'cur_width' refers to the cumulative sum of the bricks' widths encountered in the current row, and 'count'
        refers to the number of times the corresponding sum is obtained. Thus, 'cur_width' in a way represents the
        positions of the bricks's boundaries relative to the leftmost boundary.
        Let's look at the process first. We traverse over every row of the given wall. For every brick considered, we
        find the 'cur_width' corresponding to the sum of the bricks' widths encountered so far in the current row. If
        this 'cur_width' entry doesn't exist in the hash map, we create a corresponding entry with an initial count
        of 1. If the 'cur_width' already exists as a key, we increment its corresponding count value.
        This is done based on the following observation: We will never obtain the same value of 'cur_width' twice while
        traversing over a particular row. Thus, if the 'cur_width' value is repeated while traversing over the rows,
        it means some row's brick boundary coincides with some previous row's brick boundary. This fact is accounted
        for by incrementing the corresponding count value.
        But, for every row, we consider the sum only up to the second last brick, since the last boundary isn't a valid
        boundary for the solution.
        At the end, we can obtain the maximum count value to determine the minimum number of bricks that need to be cut
        to draw a vertical line through them.
    Time complexity: O(N), where N is the total number of bricks in the wall, we traverse over the complete bricks only
    once
    Space complexity: O(M), where M refers to the width of the wall
    """
    width, max_edge_occurrence = defaultdict(int), 0
    for row in wall:
        cur_width, n = 0, len(row)
        for i in range(n - 1):
            cur_width += row[i]
            width[cur_width] += 1
            max_edge_occurrence = max(max_edge_occurrence, width[cur_width])
    return len(wall) - max_edge_occurrence


class Test(unittest.TestCase):
    data = [([[1, 2, 2, 1], [3, 1, 2], [1, 3, 2], [2, 4], [3, 1, 2], [1, 3, 1, 1]], 2)]

    def test_least_bricks(self):
        for test_wall, result in self.data:
            self.assertEqual(result, least_bricks(test_wall))


if __name__ == '__main__':
    unittest.main()
