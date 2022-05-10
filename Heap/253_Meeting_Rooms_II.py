""" Given an array of meeting time intervals consisting of start and end times [[s1,e1],[s2,e2],...] (si < ei), find
the minimum number of conference rooms required. """

from heapq import heappush, heappop
import unittest2 as unittest


# More details: https://leetcode.com/articles/meeting-rooms-ii/

def min_meeting_rooms_v1(intervals):
    """ In the worst case, we can assign a new room to all the meetings but that is not really optimal, right? Unless
        of course they all collide with each other.

        We need to be able to find out efficiently if a room is available for the current meeting and assign a new room
        only if none of the assigned rooms is currently free.

        We can't really process the given meetings in any random order. The most basic way of processing the meetings
        is in increasing order of their start times and this is the order we will follow. After all, if you're an IT guy
        you should allocate a room to the meeting that is scheduled for 9 a.m. before you worry about the 5 p.m.
        meeting, right?

        Sorting part is easy, but for every meeting how do we find out efficiently if a room is available? At any point
        in time we have multiple rooms that can be occupied, and we don't really care which room is free as long as we
        find one when required for a new meeting.

        A naive way to check if a room is available is to iterate on all the rooms and see if one is available when we
        have a new meeting at hand.

        Instead of manually iterating on every room that's been allocated and checking if the room is available, we can
        keep all the rooms in a min heap where the key for the min heap would be the ending time of meeting.

        So, every time we want to check if ANY room is free or not, simply check the topmost element of the min heap as
        that would be the room that would get free the EARLIEST out of all the other rooms currently occupied. If the
        topmost room of the min heap isn't free, then no other room can be. So, we can save time here and simply
        allocate a new room.

        If the room is free, then we extract the topmost element and add it back with the ending time of the current
        meeting we are processing. If not, then we allocate a new room and add it to the heap.

        After processing all the meetings, the size of the heap will tell us the number of rooms allocated. This will
        be the minimum number of rooms needed to accommodate all the meetings.

        If we look at these events in a timeline one after the other (like stream data), then this solution is a greedy
        solution. The heap stores all conflicting events, which must be resolved by independent rooms. The heap's head
        is the event that has the earliest end/finish time. All other events collide with each other mutually in the
        heap.

        When a new event comes (this is the reason that we need to sort by start time), we greedily choose the event A
        that finished the earliest (this is the reason we use min heap on end time). If the new event does not
        collide with A, then the new event can reuse A's room by simply EXTENDING A's room to the new event's end time.
        If the new event collides with A, then it must collide with all events in the heap, so a new room must be
        created.

        The reason for correctness is the invariant:

                Heap size is always the minimum number of rooms we need so far

        If the new event collides with everyone, then a new room must be created; if the new event does not collide
        with someone, then it must not collide with the earliest finishing one, so greedily choose that one and reuse
        that room. Hence, the invariant is maintained.

    Time complexity: O(N logN), there are two major portions that take up time here: One is sorting of the array that
    takes O(N logN). Then we have the min-heap. In the worst case, all N meetings will collide with each other. In any
    case we have N add operations on the heap. In the worst case we will have N extract-min operations as well. Overall
    complexity being O(N logN) since extract-min operation on a heap takes O(logN)
    Space complexity: O(N), we construct the min-heap and that can contain N elements in the worst case as described
    above in the time complexity
    """
    intervals.sort()
    earliest_ending = []
    for start, end in intervals:
        if earliest_ending and start >= earliest_ending[0]:
            # If the room due to free up the earliest is free, assign that room to this meeting
            heappop(earliest_ending)
        # If a new room is to be assigned, we also add it to the heap. If an old room is reused, then we also have to
        # add to the heap the updated end time (after removing the room inside the previous if statement)
        heappush(earliest_ending, end)
        # That's similar to the following:
        # if earliest_ending and start >= earliest_ending[0]:
        #     heappop(earliest_ending)
        #     heappush(earliest_ending, end)
        # else:
        #     heappush(earliest_ending, end)
    return len(earliest_ending)


def min_meeting_rooms_v2(intervals):
    """ The meeting timings given to us define a chronological order of events throughout the day. We are given the
        start and end timings for the meetings which can help us define this ordering.

        Arranging the meetings according to their start times helps us know the natural order of meetings throughout
        the day. However, simply knowing when a meeting starts doesn't tell us much about its duration.

        We also need the meetings sorted by their ending times because an ending event essentially tells us that there
        MUST have been a corresponding starting event and more importantly, an ending event tells us that a previously
        occupied room has now become free.

        A meeting is defined by its start and end times. However, for this specific solution, we need to treat the
        start and end times INDIVIDUALLY. This might not make sense right away because a meeting is defined by its
        start and end times. If we separate the two and treat them individually, then the identity of a meeting goes
        away. This is fine because:

                When we encounter an ending event, that means that some meeting that started earlier has ended
                now. We are not really concerned with which meeting has ended. All we need is that SOME meeting
                ended thus making a room available.

        Separate out the start times and the end times in their separate arrays.

        Sort the start times and the end times separately. Note that this will mess up the original correspondence of
        start times and end times. They will be treated individually now.

        We consider two pointers: 'start_pointer' and 'end_pointer'. The start pointer simply iterates over all the
        meetings and the end pointer helps us track if a meeting has ended and if we can reuse a room.

        When considering a specific meeting pointed to by 'start_pointer', we check if this start timing is greater
        than the meeting pointed to by 'end_pointer'. If this is the case, then that would mean some meeting has ended
        by the time the meeting at 'start_pointer' had to start. So we can reuse one of the rooms. Otherwise, we have
        to allocate a new room. If a meeting has indeed ended i.e. if start[start_pointer] >= end[end_pointer], then we
        increment 'end_pointer'.

        Repeat this process until 'start_pointer' processes all the meetings.

        Why does this work?

        This is an interval partitioning problem. We can have two correct heuristics that 1) We process intervals
        ordered by starting time and assign each interval to a 'current vacant' room, and 2) We only check the room
        with the earliest ending time for global vacancy. If there is no vacant room, we create one.

        Since we iterate intervals by starting time, there is no better choice than the current interval as the
        remaining intervals would all request one more room if current one does. And we also need to track the ending
        time since we need to determine whether there exists a vacant room at a specific time. We only track the
        earliest ending time as we only check this room for vacancy. If this room is not vacant, there is no need to
        check the rest, and we just create one more room.

        Whenever there is a start meeting, we need to add one room. But before adding rooms, we check to see if ANY
        previous meeting ended, which is why we check start with the first end. When the start is bigger than end, it
        means at this time one of the previous meeting ended, and we can take and reuse that room. Then, the next
        meeting needs to compare with the second end because the first end's room is already taken.
        The reason why we sort end points is that we have to find the meeting room which will end earliest for reuse.
        So as long as we have a meeting whose start time is earlier than the earliest ending meeting finish time, we
        add a new room.

    Time complexity: O(N logN), for the sort
    Space complexity: O(N), we create two separate arrays of size N, one for recording the start times and one
    for the end times
    """
    n = len(intervals)
    start_timings = sorted([i[0] for i in intervals])
    end_timings = sorted(i[1] for i in intervals)
    used_rooms = 0
    start_pointer = end_pointer = 0
    while start_pointer < n:  # Until all the meetings have been processed
        # If the earliest ending meeting hasn't ended by the time the meeting at 'start_pointer' starts
        if start_timings[start_pointer] < end_timings[end_pointer]:
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
