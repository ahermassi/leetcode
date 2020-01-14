""" Given an array of meeting time intervals consisting of start and end times [[s1,e1],[s2,e2],...] (si < ei),
determine if a person could attend all meetings. """

import unittest2 as unittest


def can_attend_meetings(intervals):
    """ The idea is to sort the meetings by starting time. Then, go through the meetings one by one and make sure that
        each meeting ends before the next one starts.
    Time complexity: O(N logN)
    Space complexity: O(N) for Timsort
    """
    intervals.sort()
    n = len(intervals)
    for i in range(n - 1):
        if intervals[i][-1] > intervals[i + 1][0]:
            return False
    return True


class Test(unittest.TestCase):
    data = [([[0, 30], [5, 10], [15, 20]], False), ([[7, 10], [2, 4]], True)]

    def test_can_attend_meetings(self):
        for test_intervals, result in self.data:
            self.assertEqual(result, can_attend_meetings(test_intervals))


if __name__ == '__main__':
    unittest.main()
