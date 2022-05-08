""" You are given an array of non-overlapping intervals where intervals[i] = [starti, endi] represent the  start and the
end of the ith interval and intervals is sorted in ascending order by starti. You are also given an interval
newInterval = [start, end] that represents the start and end of another interval.

Insert newInterval into intervals such that intervals is still sorted in ascending order by starti and intervals still
does not have any overlapping intervals (merge overlapping intervals if necessary).

Return intervals after the insertion. """


def insert(intervals, new_interval):
    """ The standard solution consists of two parts:
            -Figure out how to sort the input data. That could be done directly by a sorting or indirectly by a heap usage.
            -Parse the sorted input to have a solution.
        In case of a sorted input, we don't need the first part

        The straightforward one-pass strategy could be implemented in three steps:

            - Add to the output all the intervals starting before newInterval
            - Add to the output newInterval, and merge it with the last added interval if newInterval starts before the
               last added interval ends
            - Add the next intervals one by one, and merge with the last added interval if the current interval starts
               before the last added interval ends

        Basically, the same strategy as 56- Merge Intervals, with an additional care to add the new interval in its
        proper position in order not to destroy the well-sorted input.

    Time complexity: O(N)
    Space complexity: O(N)
    """
    n, res = len(intervals), []
    i = 0
    # Add all intervals starting before newInterval
    while i < n and intervals[i][0] < new_interval[0]:
        res.append(intervals[i])
        i += 1
    # Add newInterval. If there is no overlap, just add the interval. Otherwise, merge with the last interval.
    if not res or new_interval[0] > res[-1][1]:
        res.append(new_interval)
    else:
        res[-1][1] = max(res[-1][1], new_interval[1])
    # Add next intervals, and merge if needed
    while i < n:
        if intervals[i][0] > res[-1][1]:
            res.append(intervals[i])
        else:
            res[-1][1] = max(res[-1][1], intervals[i][1])
        i += 1
    return res
