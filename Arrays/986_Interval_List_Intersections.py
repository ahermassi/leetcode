""" Given two lists of closed intervals, each list of intervals is pairwise disjoint and in sorted order.
Return the intersection of these two interval lists. """

import unittest2 as unittest


# Great visual explanation:
# https://leetcode.com/problems/interval-list-intersections/discuss/647482/Python-Two-Pointer-Approach-%2B-Thinking-Process-Diagrams

def interval_intersection_v1(first_list, second_list):
    """ There is guaranteed to be a overlap interval if:
            A[i].start <= B[j].end AND B[j].start <= A[i].end
        After we have made sure that there is an overlapping range, we need to figure out the start and end of the
        overlapping range. Think of this as trying to squeeze the overlapping range as tight as possible (pushing as
        far right as possible for start and pushing as far left as possible for end).
        Now how do we increment the pointers?
        The idea behind this is to increment the pointer based on the end values of the two intervals. Let's say the
        current interval in A has end value smaller than the end value of the current interval B. That essentially
        means that we have exhausted that interval A and we should move on to the next interval in that same list.
    Time complexity: O(N + M), where N is the length of A and M is the length of B
    Space complexity: O(1)
    """
    res = []
    n, m = len(first_list), len(second_list)
    i = j = 0
    while i < n and j < m:
        first_start, first_end = first_list[i]
        second_start, second_end = second_list[j]
        if first_start <= second_end and second_start <= first_end:  # Criss-cross lock
            overlap_start = max(first_start, second_start)
            overlap_end = min(first_end, second_end)
            res.append([overlap_start, overlap_end])
        # Advance the interval with smaller endpoint in hopes of finding another overlap
        if first_end < second_end:  # If A has the smallest endpoint, it can only intersect B ..
            i += 1  # .. so we can discard A since it cannot intersect anything else
        else:  # If B has the smallest endpoint, it can only intersect A ..
            j += 1  # .. so we can discard B since it cannot intersect anything else
    return res


def interval_intersection_v2(A, B):
    n, m = len(A), len(B)
    i, j, res = 0, 0, []
    while i < n and j < m:
        a, b = A[i], B[j]
        max_start, min_end = max(a[0], b[0]), min(a[1], b[1])  # Find the overlap, if there is any
        if max_start <= min_end:
            res.append([max_start, min_end])
        # Remove the interval with the smallest endpoint
        if a[1] < b[1]:  # If 'a' has the smallest endpoint, it can only intersect b ..
            i += 1  # .. so we can discard 'a' since it cannot intersect anything else
        else:  # If 'b' has the smallest endpoint, it can only intersect a ..
            j += 1  # .. so we can discard 'b' since it cannot intersect anything else
    return res


class Test(unittest.TestCase):
    data = [([[0, 2], [5, 10], [13, 23], [24, 25]], [[1, 5], [8, 12], [15, 24], [25, 26]],
             [[1, 2], [5, 5], [8, 10], [15, 23], [24, 24], [25, 25]])]

    def test_interval_intersection(self):
        for test_a, test_b, result in self.data:
            self.assertEqual(result, interval_intersection_v1(test_a, test_b))
            self.assertEqual(result, interval_intersection_v2(test_a, test_b))


if __name__ == '__main__':
    unittest.main()
