""" Given a collection of intervals, find the minimum number of intervals you need to remove to make the rest of the
intervals non-overlapping. """

import unittest2 as unittest


def erase_overlap_intervals_v1(intervals):
    """ The problem is similar to: Given a collection of intervals, find the maximum number of intervals that are
        non-overlapping.
        Sort the intervals by their start time. If two intervals overlap, the interval with latest end time will be
        removed so as to have as little impact on subsequent intervals as possible.
        The heuristic is: always pick the interval with the earliest end time. Then we can get the maximal number of
        non-overlapping intervals, thus the minimal number of intervals to remove. This is because the interval with
        the earliest end time produces the maximal capacity to hold rest intervals.
        If two intervals are overlapping, we want to remove the interval that has the longer end point -- the longer
        interval will always overlap with more or the same number of future intervals compared to the shorter one.
    Time complexity: O(N logN)
    Space complexity: O(N), for Timsort
    """
    if not intervals:
        return 0
    intervals.sort()
    n, removed = len(intervals), 0
    pre_end = intervals[0][1]  # Pointer to keep track of the end time of previously examined interval
    for i in range(1, n):
        cur_start, cur_end = intervals[i]
        if cur_start < pre_end:  # Find overlapping interval
            removed += 1
            pre_end = min(pre_end, cur_end)  # Remove the interval with larger end time
        else:
            pre_end = cur_end  # Update end time
    return removed


class Test(unittest.TestCase):
    data = [([[1, 2], [2, 3], [3, 4], [1, 3]], 1), ([[1, 2], [1, 2], [1, 2]], 2), ([[1, 2], [2, 3]], 0)]

    def test_erase_overlap_intervals(self):
        for test_intervals, result in self.data:
            self.assertEqual(result, erase_overlap_intervals_v1(test_intervals))


if __name__ == '__main__':
    unittest.main()
