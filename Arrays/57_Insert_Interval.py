""" You are given an array of non-overlapping intervals where intervals[i] = [starti, endi] represent the  start and the
end of the ith interval and intervals is sorted in ascending order by starti. You are also given an interval
newInterval = [start, end] that represents the start and end of another interval.

Insert newInterval into intervals such that intervals is still sorted in ascending order by starti and intervals still
does not have any overlapping intervals (merge overlapping intervals if necessary).

Return intervals after the insertion. """


def insert_v1(intervals, new_interval):
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


# Video explanation: https://www.youtube.com/watch?v=A8NUOmlwOlM

def insert_v2(intervals, new_interval):
    """ First, add all intervals that are to the left of newInterval. These are the intervals that end before
         newInterval starts.

         Second, merge all intervals that overlapping with newInterval.

         Finally, add all intervals that are to the right of newInterval.

        Example: intervals = [[1,2],[3,5],[6,7],[8,10],[12,16]], newInterval = [4,8]

        Interval [1,2] is before [4,8], that is interval.end < newInterval.start, so we just add it to our res.

        Interval [3,5] overlap, newInterval = [min(3, 4), max(5, 8) = [3,8]

        Interval [6,7]: overlap, newInterval = [min(3, 6), max(8, 7] = [3,8]

        Interval [8,10]: overlap, newInterval = [min(3, 8), max(8, 10)] = [3,10]

        Interval [12,16]: starts after our newInterval ends, so no overlap.

        Outside the loop we combine res = [1,2], newInterval = [3,10], and intervals[4:] = [12,16]:
        res = [[1,2], [3,10], [12,16]]

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
    res.append([start, end])  # Add the union of previous intervals that overlapped with newInterval. Notice that if
    # no interval overlaps with newInterval, [start, end] is the same as newInterval
    res.extend(intervals[i:])  # Add all the rest
    return res
