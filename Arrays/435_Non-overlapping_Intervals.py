""" Given a collection of intervals, find the minimum number of intervals you need to remove to make the rest of the
intervals non-overlapping. """

import unittest2 as unittest


# Video explanation: https://www.youtube.com/watch?v=nONCGxWoUfM

def erase_overlap_intervals_v1(intervals):
    """ The problem is the same as:

                Given a collection of intervals, find the maximum number of intervals that are
                non-overlapping.

        Sort the intervals by their start time. If two intervals overlap, the interval with the latest end time will be
        removed to have as little impact on subsequent intervals as possible.

        While considering the intervals in the ascending order of starting points, we make use of a pointer
        prev_interval_end to keep track of the interval just included in the final list. While traversing, we can
        encounter 3 possibilities:

            - The two intervals currently considered are non-overlapping: In this case, we need not remove any
               interval, and we can continue by simply assigning the prev_interval_end pointer to the later interval
               and the count of intervals removed remains unchanged.

            - The two intervals currently considered are overlapping and the end point of the later interval falls
               before the end point of the previous interval: In this case, we can simply take the later interval.
               The choice is obvious since choosing an interval of smaller width will lead to more available space
               in which more intervals can be accommodated. Hence, the prev_interval_end pointer is updated to
               current interval's end and the count of intervals removed is incremented by 1.

            - The two intervals currently considered are overlapping and the end point of the later interval falls after
               the end point of the previous interval: In this case, we can work in a greedy manner and directly remove
               the later interval. Thus, the prev_interval_end pointer remains unchanged and the count of intervals
               removed is incremented by 1.

        The heuristic is: Always keep the interval with the earliest end time. Then we can get the maximal number of
        non-overlapping intervals, thus the minimal number of intervals to remove. This is because the interval with
        the earliest end time produces the maximal capacity to hold rest intervals.

        If two intervals are overlapping, we want to remove the interval that has the longer end point -- the longer
        interval will always overlap with more or the same number of future intervals compared to the shorter one.
        By removing it, there is less of a chance that it's going to overlap with the following intervals.

    Time complexity: O(N logN)
    Space complexity: O(N), for sort
    """
    intervals.sort()
    removed = 0
    prev_interval_end = float('-inf')  # Pointer to keep track of the end time of previously processed interval
    for start, end in intervals:
        if start < prev_interval_end:  # Find overlapping interval
            prev_interval_end = min(prev_interval_end, end)  # Keep the interval with the smallest end time
            removed += 1
        else:
            prev_interval_end = end  # Update end time
    return removed


def erase_overlap_intervals_v2(intervals):
    """ Dynamic programming. TLE.
        Let dp[i] be the maximum number of valid intervals that can be included in the final list if only the intervals
        up to and including the ith interval are considered. To find dp[i+1], we can't consider the value of dp[i-1]
        only, because it could be possible that the (i-1)th or any previous interval is overlapping with the ith
        interval. Thus, we need to consider the maximum of all dp[j]'s such that j ≤ i and jth and ith intervals don't
        Therefore:
            dp[i] = max(dp[j] for 0 <= j < i such that jth and ith intervals don't overlap) + 1
        In the end, to obtain the maximum number of intervals that can be included in the final list, let's call it
        'res', we need to find the maximum value in the dp array. The final result will be the total number of input
        intervals given minus the result just obtained: len(intervals) - result
    Time complexity: O(N^2)
    Space complexity: O(N)
    """
    if not intervals:
        return 0
    n = len(intervals)
    intervals.sort()
    dp = [0] * n
    dp[0] = 1
    for i in range(1, n):
        for j in range(i):
            if intervals[i][0] >= intervals[j][1]:
                dp[i] = max(dp[i], dp[j] + 1)
    return n - max(dp)


class Test(unittest.TestCase):
    data = [([[1, 2], [2, 3], [3, 4], [1, 3]], 1), ([[1, 2], [1, 2], [1, 2]], 2), ([[1, 2], [2, 3]], 0)]

    def test_erase_overlap_intervals(self):
        for test_intervals, result in self.data:
            self.assertEqual(result, erase_overlap_intervals_v1(test_intervals))
            self.assertEqual(result, erase_overlap_intervals_v2(test_intervals))


if __name__ == '__main__':
    unittest.main()
