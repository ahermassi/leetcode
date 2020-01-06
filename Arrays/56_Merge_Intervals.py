""" Given a collection of intervals, merge all overlapping intervals. """

import unittest2 as unittest


def merge(intervals):
    """ Two intervals i1 and i2 overlap if the following requirements are satisfied:
            Requirement 1: i2.start <= i1.end
            Requirement 2: i1.start <= i2.end
        i1: #......................#
             s1                   e1
        i2:       #.....................#
                   s2                  e2
        s2 <= e1 and s1 <= e2
        If any of the 2 conditions is not verified, the intervals wouldn't overlap.
        If s2 > e1:
        i1: #......................#
             s1                   e1
        i2:                            #.....................#
                                        s2                  e2
        If s1 > e2:
        i1:                                 #......................#
                                             s1                   e1
        i2:       #.....................#
                   s2                  e2
        We pre-process the list by sorting intervals by start. This way, requirement 2 i1.start <= i2.start < i2.end is
        promised. We only have to compare i1.end with i2.start to see if requirement 1 is satisfied.
        First, we sort the list. Then, we insert the first interval into our 'res' list and continue considering each
        interval in turn as follows: If the current interval begins after the previous interval ends, then they do NOT
        overlap and we can append the current interval to 'res'. Otherwise, they do overlap, and we merge them by
        updating the end of the previous interval if it is less than the end of the current interval.
        When the intervals are sorted, all mergeable intervals form contiguous blocks.
    Time complexity: O(N logN), the complexity of sorting
    Space complexity: O(N), if we can sort intervals in place, we do not need more than constant additional space.
    Otherwise, we must allocate linear space to store a copy of intervals and sort that.
    """
    intervals.sort()
    res = []
    for interval in intervals:
        if res and interval[0] <= res[-1][1]:  # If the list of merged intervals is not empty and if the current
            # interval overlaps with the previous, merge the current and previous intervals.
            res[-1][1] = max(res[-1][1], interval[1])
        else:  # Otherwise, simply append the current interval
            res.append(interval)
    return res

# There seems to be a follow-up at Facebook to implement the algorithm with no sorting, using a BST.
# https://leetcode.com/problems/merge-intervals/discuss/21451/Share-my-BST-interval-tree-solution-C%2B%2B-No-sorting!
# https://leetcode.com/problems/merge-intervals/discuss/355318/Fully-Explained-and-Clean-Interval-Tree-for-Facebook-Follow-Up-No-Sorting
# https://leetcode.com/articles/merge-intervals/


class Test(unittest.TestCase):
    data = [([[1, 3], [2, 6], [8, 10], [15, 18]], [[1, 6], [8, 10], [15, 18]]),
            ([[1, 4], [4, 5]], [[1, 5]])]

    def test_merge(self):
        for test_array, result in self.data:
            self.assertEqual(result, merge(test_array))


if __name__ == '__main__':
    unittest.main()
