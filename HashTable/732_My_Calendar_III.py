""" A k-booking happens when k events have some non-empty intersection (i.e., there is some time that is common to all
k events.)

You are given some events [start, end), after each given event, return an integer k representing the maximum k-booking
between all the previous events.

Implement the MyCalendarThree class:

MyCalendarThree() Initializes the object.
int book(int start, int end) Returns an integer k representing the largest integer such that there exists a k-booking
in the calendar. """

from collections import defaultdict


class MyCalendarThree:
    """ The problem asks us to return an integer k representing the largest integer such that there exists a k-booking
        in the calendar, i.e., the GLOBAL maximum number of overlaps. A k-booking happens when there is some time that
        is common to k events.

        We can log the start and end of each event on the 'timeline' hash map. Each start adds a new ongoing event at
        that time, and each end terminates an ongoing event. Then we can scan the timeline in a chronological order
        to figure out the maximum number of ongoing events at any time.

    Time complexity: O(N^2 logN), where N is the number of events booked. For each new event, we sort 'timeline' in
    O(N logN) time which dominates the O(N) traversal, so O(N * (N logN)) = O(N^2 logN)
    Space complexity: O(N)
    """

    def __init__(self):
        self.timeline = defaultdict(int)

    def book(self, start: int, end: int) -> int:
        self.timeline[start] += 1
        self.timeline[end] -= 1
        res = ongoing = 0
        for timestamp in sorted(self.timeline.keys()):
            ongoing += self.timeline[timestamp]
            res = max(res, ongoing)
        return res
