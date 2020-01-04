""" Given an array of meeting time intervals consisting of start and end times [[s1,e1],[s2,e2],...] (si < ei), find
the minimum number of conference rooms required. """

from heapq import heappush, heappop
import unittest2 as unittest


# More details: https://leetcode.com/articles/meeting-rooms-ii/

def min_meeting_rooms_v1(intervals):
    """ In the worst case we can assign a new room to all of the meetings but that is not really optimal right? Unless
        of course they all collide with each other. We need to be able to find out efficiently if a room is available
        or not for the current meeting and assign a new room only if none of the assigned rooms is currently free.
        We can't really process the given meetings in any random order. The most basic way of processing the meetings
        is in increasing order of their start times and this is the order we will follow. After all if you're an IT guy,
        you should allocate a room to the meeting that is scheduled for 9 a.m. in the morning before you worry about the
        5 p.m. meeting, right?
        Instead of manually iterating on every room that's been allocated and checking if the room is available or not,
        we can keep all the rooms in a min heap where the key for the min heap would be the ending time of meeting.
        So, every time we want to check if any room is free or not, simply check the topmost element of the min heap as
        that would be the room that would get free the earliest out of all the other rooms currently occupied. If the
        room we extracted from the top of the min heap isn't free, then no other room is. So, we can save time here and
        simply allocate a new room.
        After processing all the meetings, the size of the heap will tell us the number of rooms allocated. This will
        be the minimum number of rooms needed to accommodate all the meetings.
        The reason for correctness is the invariant: heap size is always the minimum number of rooms we need so far.
        If the new event collides with everyone, then a new room must be created; if the new event does not collide
        with someone, then it must not collide with the earliest finish one, so greedily choose that one and re-use
        that room. So the invariant is maintained.
    Time complexity: O(N logN), There are two major portions that take up time here. One is sorting of the array that
    takes O(N logN). Then we have the min-heap. In the worst case, all N meetings will collide with each other. In any
    case we have N add operations on the heap. In the worst case we will have N extract-min operations as well. Overall
    complexity being O(N logN) since extract-min operation on a heap takes O(logN)
    Space complexity: O(N) because we construct the min-heap and that can contain N elements in the worst case as
    described above in the time complexity
    """
    if not intervals:
        return 0
    intervals.sort()
    heap = []
    heappush(heap, intervals[0][1])  # Add the first meeting. We have to give a new room to the first meeting
    for i in range(1, len(intervals)):
        interval = intervals[i]
        if interval[0] >= heap[0]:  # If the room due to free up the earliest is free, assign that room to this meeting
            heappop(heap)
            heappush(heap, interval[1])
        else:
            heappush(heap, interval[1])  # If a new room is to be assigned, then also we add to the heap
    return len(heap)


def min_meeting_rooms_v2(intervals):
    """ A meeting is defined by its start and end times. However, for this specific solution, we need to treat the
        start and end times individually. This might not make sense right away because a meeting is defined by its
        start and end times. If we separate the two and treat them individually, then the identity of a meeting goes
        away. This is fine because:
            When we encounter an ending event, that means that some meeting that started earlier has ended now. We are
            not really concerned with which meeting has ended. All we need is that SOME meeting ended thus making a
            room available.
        Separate out the start times and the end times in their separate arrays.
        Sort the start times and the end times separately. Note that this will mess up the original correspondence of
        start times and end times. They will be treated individually now.
        We consider two pointers: s_ptr and e_ptr which refer to start pointer and end pointer. The start pointer
        simply iterates over all the meetings and the end pointer helps us track if a meeting has ended and if we can
        reuse a room.
        When considering a specific meeting pointed to by s_ptr, we check if this start timing is greater than the
        meeting pointed to by e_ptr. If this is the case then that would mean some meeting has ended by the time the
        meeting at s_ptr had to start. So we can reuse one of the rooms. Otherwise, we have to allocate a new room.
        If a meeting has indeed ended i.e. if start[s_ptr] >= end[e_ptr], then we increment e_ptr.
        Repeat this process until s_ptr processes all of the meetings.
    Time complexity: O(N logN) for Timsort
    Space complexity: O(N) because we create two separate arrays of size N, one for recording the start times and one
    for the end times
    """
    if not intervals:
        return 0
    n, used_rooms = len(intervals), 0
    start_timings = sorted([i[0] for i in intervals])
    end_timings = sorted(i[1] for i in intervals)
    start_pointer = end_pointer = 0  # The two pointers in the algorithm: e_ptr and s_ptr
    while start_pointer < n:  # Until all the meetings have been processed
        if start_timings[start_pointer] < end_timings[end_pointer]:  # If the earliest ending meeting hasn't ended by
            # the time the meeting at 'start_pointer' starts
            used_rooms += 1  # Allocate a new room for the current meeting
        else:  # If there is a meeting that has ended by the time the meeting at 'start_pointer' starts
            end_pointer += 1  # Use that same room and increment 'end_pointer'
        start_pointer += 1
    return used_rooms


class Test(unittest.TestCase):
    data = [([[0, 30], [5, 10], [15, 20]], 2), ([[7, 10], [2, 4]], 1)]

    def test_min_meeting_rooms(self):
        for test_intervals, result in self.data:
            self.assertEqual(result, min_meeting_rooms_v1(test_intervals))
            self.assertEqual(result, min_meeting_rooms_v2(test_intervals))


if __name__ == '__main__':
    unittest.main()
