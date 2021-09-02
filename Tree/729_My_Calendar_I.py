""" You are implementing a program to use as your calendar. We can add a new event if adding the event will not cause
a double booking.

A double booking happens when two events have some non-empty intersection (i.e., some moment is common to both events.).

The event can be represented as a pair of integers start and end that represents a booking on the half-open interval
[start, end), the range of real numbers x such that start <= x < end.

Implement the MyCalendar class:

MyCalendar() Initializes the calendar object.
boolean book(int start, int end) Returns true if the event can be added to the calendar successfully without causing
a double booking. Otherwise, return false and do not add the event to the calendar. """


class MyCalendarV1(object):
    """ When booking a new event [start, end), check if every current event conflicts with the new event. If none of
        them does, we can book the event.
        We maintain a list of interval events (not necessarily sorted). Evidently, two events [s1, e1) and [s2, e2) do
        not conflict if and only if one of them starts after the other one ends: either s1 >= e2 OR s2 >= e1 .
        By De Morgan's laws, this means the events conflict when s1 < e2 AND s2 < e1.
    Time complexity: O(N^2), where N is the number of events booked. For each new event, we process every previous
    event to decide whether the new event can be booked. This leads to   Σ   i = N * (N-1) / 2 = O(N^2)
    Space complexity: O(N), the size of the calendar                   i=0..N
    """

    def __init__(self):
        self.previous_events = []

    def book(self, start, end):
        for prev_start, prev_end in self.previous_events:
            if start < prev_end and prev_start < end:
                return False
        self.previous_events.append((start, end))
        return True
