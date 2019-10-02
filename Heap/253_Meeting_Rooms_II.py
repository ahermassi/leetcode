""" Given an array of meeting time intervals consisting of start and end times [[s1,e1],[s2,e2],...] (si < ei), find
the minimum number of conference rooms required. """

from heapq import heappush, heapreplace
import unittest2 as unittest


def min_meeting_rooms_v1(intervals):
    """ We can't really process the given meetings in any random order. The most basic way of processing the meetings
        is in increasing order of their start times and this is the order we will follow. After all if you're an IT guy,
        you should allocate a room to the meeting that is scheduled for 9 a.m. in the morning before you worry about the
        5 p.m. meeting, right?
        Instead of manually iterating on every room that's been allocated and checking if the room is available or not,
        we can keep all the rooms in a min heap where the key for the min heap would be the ending time of meeting.
        So, every time we want to check if any room is free or not, simply check the topmost element of the min heap as
        that would be the room that would get free the earliest out of all the other rooms currently occupied. If the
        room we extracted from the top of the min heap isn't free, then no other room is. So, we can save time here and
        simply allocate a new room.
    Time complexity: O(N logN), There are two major portions that take up time here. One is sorting of the array that
    takes O(N logN). Then we have the min-heap. In the worst case, all N meetings will collide with each other. In any
    case we have N add operations on the heap. In the worst case we will have N extract-min operations as well. Overall
    complexity being O(N logN) since extract-min operation on a heap takes O(logN)
    Space complexity: O(N) because we construct the min-heap and that can contain NN elements in the worst case as
    described above in the time complexity
    """
    if not intervals:
        return 0
    intervals.sort()
    heap = []
    heappush(heap, intervals[0][1])
    for i in range(1, len(intervals)):
        interval = intervals[i]
        if interval[0] >= heap[0]:
            heapreplace(heap, interval[1])
        else:
            heappush(heap, interval[1])
    return len(heap)


class Test(unittest.TestCase):
    data = [([[0, 30], [5, 10], [15, 20]], 2), ([[7, 10], [2, 4]], 1)]

    def test_min_meeting_rooms(self):
        for test_intervals, result in self.data:
            self.assertEqual(result, min_meeting_rooms_v1(test_intervals))


if __name__ == '__main__':
    unittest.main()
