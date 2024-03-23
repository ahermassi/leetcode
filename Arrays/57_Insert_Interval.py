""" You are given an array of non-overlapping intervals where intervals[i] = [starti, endi] represent the  start and the
end of the ith interval and intervals is sorted in ascending order by starti. You are also given an interval
newInterval = [start, end] that represents the start and end of another interval.

Insert newInterval into intervals such that intervals is still sorted in ascending order by starti and intervals still
does not have any overlapping intervals (merge overlapping intervals if necessary).

Return intervals after the insertion. """


def insert_v1(intervals, new_interval):
    """ The most intuitive approach is to insert newInterval into the original list keeping the start value of intervals
         in ascending order. This can be done using linear search, we can iterate over the intervals in the list, and
         the newInterval should be inserted just before the interval having a greater start value. This way, we can
         produce the list of intervals in ascending order of their start value and merge them using the algorithm in
         56- Merge Intervals.

        However, we can use a straightforward one-pass strategy which could be implemented in three steps:

            - Add to the output all the intervals that start before newInterval
            - Add to the output newInterval and merge it with the last added one if there is an overlap
            - Add the remaining intervals one by one, and merge with the last added interval if there is an overlap

        Basically, the same approach as 56- Merge Intervals, with an additional care to add the new interval in its
        proper position in order to not destroy the well-sorted input.

    Time complexity: O(N)
    Space complexity: O(N)
    """
    n, res = len(intervals), []
    start, end = new_interval
    i = 0
    # Add all the intervals that start before newInterval
    while i < n and intervals[i][0] < start:
        res.append(intervals[i])
        i += 1
    # Add newInterval. If there is no overlap, just add the interval as-is. Otherwise, merge it with the last interval.
    if not res or start > res[-1][1]:
        res.append(new_interval)
    else:
        res[-1][1] = max(res[-1][1], end)
    # Add the remaining intervals and merge if needed
    while i < n:
        if intervals[i][0] > res[-1][1]:
            res.append(intervals[i])
        else:
            res[-1][1] = max(res[-1][1], intervals[i][1])
        i += 1
    return res


# Video explanation: https://www.youtube.com/watch?v=A8NUOmlwOlM
def insert_v2(intervals, new_interval):
    """ Similar to the previous solution, but this time instead of starting by adding all the intervals that start
         before newInterval (curInterval.start < newInterval.start), we actually begin by adding the intervals that end
         before newInterval starts (curInterval.end < newInterval.start).

         Then, we merge all the intervals that overlap with newInterval.

         Finally, we add all the intervals that are to the right of newInterval.

         Example: intervals = [[1,2],[3,5],[6,7],[8,10],[12,16]], newInterval = [4,8]
         Interval = [1,2] ends before [4,8] starts, so we just add it to the output.
         Interval = [3,5], overlap, newInterval = [min(3, 4), max(5, 8) = [3,8]
         Interval = [6,7], overlap, newInterval = [min(3, 6), max(8, 7] = [3,8]
         Interval = [8,10], overlap, newInterval = [min(3, 8), max(8, 10)] = [3,10]
         Interval = [12,16], starts after newInterval ends, so no overlap.
         Outside the loop we combine res = [1,2], newInterval = [3,10], and intervals[4:] = [12,16]
         --> res = [[1,2], [3,10], [12,16]]

    Time complexity: O(N)
    Space complexity: O(N)
    """
    n, res = len(intervals), []
    start, end = new_interval
    i = 0
    while i < n and intervals[i][1] < start:
        res.append(intervals[i])
        i += 1
    while i < n and intervals[i][0] <= end:
        # Merge overlapping intervals. We're mutating newInterval to represent the overall merged interval of
        # intervals that overlap with newInterval
        start = min(start, intervals[i][0])
        end = max(end, intervals[i][1])
        i += 1
    # Add the union of previous intervals that overlapped with newInterval. Notice that if no interval overlaps with
    # newInterval, [start, end] is the same as newInterval.
    res.append([start, end])
    res.extend(intervals[i:])  # Add all the remaining intervals
    return res


def insert_v3(intervals, new_interval):
    """ We can combine the loops of the previous solution into one single for loop. Same logic, though.

    Time complexity: O(N)
    Space complexity: O(N)
    """
    n, res = len(intervals), []
    start, end = new_interval
    for i, interval in enumerate(intervals):
        if interval[1] < start:
            # Current interval starts first and doesn't overlap with newInterval
            res.append(interval)
        elif interval[0] <= end:
            # Overlap. Merge current interval and newInterval
            start = min(start, interval[0])
            end = max(end, interval[1])
        else:
            res.append([start, end])
            return res + intervals[i:]
    # If we reach this statement, newInterval overlapped with a bunch of other intervals but there was no interval X
    # that started after the end of the merged intervals (X[0] > end)
    res.append([start, end])
    return res