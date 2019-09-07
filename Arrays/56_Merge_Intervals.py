""" Given a collection of intervals, merge all overlapping intervals. """

import unittest2 as unittest


def merge(intervals):
    """ First, we sort the list. Then, we insert the first interval into our 'res' list and continue considering each
        interval in turn as follows: If the current interval begins after the previous interval ends, then they do NOT
        overlap and we can append the current interval to 'res'. Otherwise, they do overlap, and we merge them by
        updating the end of the previous interval if it is less than the end of the current interval.
        When the intervals are sorted, and then all mergeable intervals form contiguous blocks.
    Time complexity: O(N log N), the complexity of sorting
    Space complexity: O(N), if we can sort intervals in place, we do not need more than constant additional space.
    Otherwise, we must allocate linear space to store a copy of intervals and sort that.
    """
    intervals.sort()
    res = []
    for interval in intervals:
        if not res or interval[0] > res[-1][1]:  # If the list of merged intervals is empty or if the current
            # interval does not overlap with the previous, simply append it.
            res.append(interval)
        else:  # Otherwise, there is overlap, so we merge the current and previous intervals.
            res[-1][1] = max(res[-1][1], interval[1])
    return res


class Test(unittest.TestCase):
    data = [([[1, 3], [2, 6], [8, 10], [15, 18]], [[1, 6], [8, 10], [15, 18]]),
            ([[1, 4], [4, 5]], [[1, 5]])]

    def test_merge(self):
        for test_array, result in self.data:
            self.assertEqual(result, merge(test_array))


if __name__ == '__main__':
    unittest.main()
