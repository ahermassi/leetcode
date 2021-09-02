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
        Note: We are given right-open interval range, so we consider two ranges as intersecting even if one has the
        same start as end of the other.
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

#############################################################


class TreeNode(object):
    def __init__(self, start, end):
        self.start = start
        self.end = end
        self.left = None
        self.right = None


class MyCalendarV2(object):
    """ If we maintained our events in sorted order, we could check whether an event could be booked in O(logN) time
        (where N is the number of events already booked) by binary searching for where the event should be placed.
        We would also have to insert the event in our sorted structure. We need a data structure that keeps elements
        sorted and supports fast insertion. In Python, we can build our own binary tree structure.
        We will create a binary tree. Each node represents some interval [start, end) while 'left' and 'right'
        represent nodes that are smaller or larger than the current node.
    Time complexity: O(N^2), worst case, with O(N logN) on random data. For each new event, we insert the event into
    our binary tree. As this tree may not be balanced, it may take a linear number of steps to add each event.  In
    worst cases, if the input is highly ordered, the BST is likely to turn into a list.
    Space complexity: O(N), the size of the binary tree
    """

    def __init__(self):
        self.root = None

    def insert(self, start, end, root):
        if end <= root.start:
            if not root.left:
                root.left = TreeNode(start, end)
                return True
            return self.insert(start, end, root.left)
        elif root.end <= start:
            if not root.right:
                root.right = TreeNode(start, end)
                return True
            return self.insert(start, end, root.right)
        return False

    def book(self, start, end):
        if not self.root:
            self.root = TreeNode(start, end)
            return True
        return self.insert(start, end, self.root)

#############################################################


class MyCalendarV3(object):
    """ Iterative version of the previous solution.
    Time complexity: O(N^2) worst-case, O(N logN) best-case
    Space complexity: O(N)
    """

    def __init__(self):
        self.root = None

    def book(self, start, end):
        if not self.root:
            self.root = TreeNode(start, end)
            return True
        root = self.root
        while root:
            if end <= root.start:
                if not root.left:
                    root.left = TreeNode(start, end)
                    return True
                root = root.left
            elif root.end <= start:
                if not root.right:
                    root.right = TreeNode(start, end)
                    return True
                root = root.right
            else:
                return False
