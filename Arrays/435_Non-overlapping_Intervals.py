""" Given a collection of intervals, find the minimum number of intervals you need to remove to make the rest of the
intervals non-overlapping. """

import unittest2 as unittest


# Video explanation: https://www.youtube.com/watch?v=nONCGxWoUfM
def erase_overlap_intervals_v1(intervals):
    """ Finding the minimum number of intervals to remove is equivalent to finding the maximum number of
         non-overlapping intervals. This is the famous interval scheduling problem.

        Let's start by considering the intervals according to their start times. If two intervals i1 and i2 overlap, we
        greedily choose to remove the interval with the latest end time to minimize overlap chances with subsequent
        intervals.
        Let's call k the choice we need to make between i1.end and i2.end. We want to maximize the number of intervals
        we keep (without overlap), so we want to maximize our choices for the next intervals. Because the next interval
        must have a start time greater than or equal to k to avoid overlap, a larger value of k can never give us more
        choices than a  smaller value of k. As such, we should try to minimize k. Therefore, we should always greedily
        remove the interval with the latest end time.

        While considering the intervals in the ascending order of starting times, we make use of a pointer
        prev_interval_end to keep track of the end time of the previously processed interval. While traversing, we can
        encounter 3 possibilities:

            - The current and previous intervals are non-overlapping: In this case, we don't need to remove any
               interval, and we can continue by simply assigning prev_interval_end the end time of the current interval,
               and the count of intervals removed remains unchanged.

            - The current and previous intervals are overlapping and the end time of the current interval falls
               before the end time of the previous interval: In this case, we can simply take the current interval.
               The choice is obvious since choosing an interval of smaller width will lead to more available space
               in which more intervals can be accommodated. Hence, prev_interval_end pointer is updated to current
               interval's end time and the count of removed intervals is incremented by 1.

            - The current and previous intervals are overlapping and the end time of the current interval falls after
               the end time of the previous interval: In this case, we can work in a greedy manner and directly remove
               the current interval. Thus, prev_interval_end pointer remains unchanged and the count of removed
               intervals is incremented by 1.

        The heuristic is: Always keep the interval with the earliest end time. Then we can get the maximal number of
        non-overlapping intervals, thus the minimal number of intervals to remove. This is because the interval with
        the earliest end time produces the maximal room for accommodating future intervals.

        In other words, if two intervals are overlapping, we want to remove the interval that has the later end point
        -- the longer interval will always overlap with more or the same number of future intervals compared to the
        shorter one. By removing it, there is less of a chance that it's going to overlap with the following intervals.

    Time complexity: O(N logN)
    Space complexity: O(N), for sort
    """
    intervals.sort()
    removed = 0
    prev_interval_end = float('-inf')  # Pointer to keep track of the end time of previously processed interval
    for start, end in intervals:
        if start < prev_interval_end:  # Find overlapping interval
            prev_interval_end = min(prev_interval_end, end)  # Keep the interval with the earliest end time
            removed += 1
        else:
            prev_interval_end = end  # Update end time
    return removed


def erase_overlap_intervals_v2(intervals):
    """ The previous approach was based on choosing intervals greedily based on the starting times. In this approach, we
        choose greedily based on the end times.

         For this, we sort the given intervals based on the end time. Then, we traverse the sorted intervals. We can
         encounter 2 possibilities:

            - The current and previous intervals are non-overlapping: In this case, we don't need to remove any
               interval, and we can continue by simply assigning prev_interval_end the end time of the current interval.

            - The current and previous intervals are overlapping and the starting time of the current interval falls
               before the ending time of the previous interval: In this case, it is obvious that the current interval
               completely subsumes the previous interval (current interval starts before previous interval and ends
               after it, since intervals are sorted by end time). Hence, it is advantageous to remove the current
               interval so that we can get more room to accommodate future intervals. Thus, the current interval is
               removed and prev_interval_end is unchanged.

        Intuition: If we choose the interval that ends early, we'll have more room left to accommodate more intervals.
        If we have two overlapping intervals A and B, we can only keep one. The question is, which one should we keep?
        To avoid overlap, we should always greedily choose to keep the interval with an earlier end time. This way, we
        have higher chance of placing other intervals after it. So, we decided to sort by end time.

    Time complexity: O(N logN)
    Space complexity: O(N)
    """
    intervals.sort(key=lambda interval: interval[1])
    removed = 0
    prev_interval_end = float('-inf')
    for start, end in intervals:
        if start < prev_interval_end:
            removed += 1
            # We don't update prev_interval_end, because 'end' is greater than 'prev_interval_end' (intervals are
            # sorted by end time)
        else:
            # We can safely take this interval because it won't cause an overlap. We should update prev_interval_end
            # since this interval is now the most recent interval we are keeping.
            prev_interval_end = end
    return removed


def erase_overlap_intervals_v3(intervals):
    """ Dynamic Programming. TLE.

        Let dp[i] be the maximum number of valid intervals that can be included in the final list if only the intervals
        up to and including the ith interval are considered.

        To find dp[i+1], we can't consider the value of dp[i-1] only, because it could be possible that the (i-1)th or
        any previous interval is overlapping with the ith interval. Thus, we need to consider the maximum of all
        dp[j]'s such that j < i and jth and ith intervals don't overlap. Therefore:

                    dp[i] = max(dp[j] for 0 <= j < i such that jth and ith intervals don't overlap) + 1

        In the end, to obtain the maximum number of intervals that can be included in the final list, let's call it
        'res', we need to find the maximum value in the dp array. The final result will be the total number of input
        intervals given minus the result just obtained: len(intervals) - result

    Time complexity: O(N^2)
    Space complexity: O(N)
    """
    intervals.sort()
    n = len(intervals)
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
            self.assertEqual(result, erase_overlap_intervals_v3(test_intervals))


if __name__ == '__main__':
    unittest.main()
