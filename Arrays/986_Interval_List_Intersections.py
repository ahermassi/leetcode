""" Given two lists of closed intervals, each list of intervals is pairwise disjoint and in sorted order.
Return the intersection of these two interval lists. """

import unittest2 as unittest


# Great visual explanation:
# https://leetcode.com/problems/interval-list-intersections/discuss/647482/Python-Two-Pointer-Approach-%2B-Thinking-Process-Diagrams
def interval_intersection_v1(first_list, second_list):
    """ Two intervals i1 and i2 overlap if the following two conditions are met:

                    i1.start <= i2.end
                    i2.start <= i1.end

        i1: #......................#
             s1                   e1
        i2:       #.....................#
                   s2                  e2
        s1 <= e2 and s2 <= e1
        If any of the two conditions is not verified, the intervals wouldn't overlap.

        If s2 > e1:
        i1: #......................#
             s1                   e1
        i2:                            #.....................#
                                        s2                  e2

        If s1 > e2:
        i1:                                 #......................#
                                             s1                   e1
        i2:       #.....................#
                   s2                  e2

        After we make sure that there is an overlapping range, we need to figure out the start and end of the overlap.
        Think of this as trying to squeeze the overlapping range as tight as possible (pushing as far right as possible
        for start and pushing as far left as possible for end).

        Now how do we advance the pointers?

        The idea behind this is to increment the pointer based on the end values of the two intervals. Let's say the
        current interval in A has end value smaller than the end value of the current interval B:

        A: #......................#
             s1                   e1
        B:       #.....................#
                   s2                  e2

        That essentially means that we have exhausted that interval A, and we should move on to the next interval in
        that same list as A can ONLY intersect B. We can find more overlaps with B only if we advance in A's list.

        Lists are sorted. Therefore, the interval whose end came first will never be a potential candidate for
        intersection with other intervals, because if it didn't intersect with current interval of the other list, it
        won't intersect with any further interval as well, and if it did intersect with the current interval of the
        other list, it intersected all the way till its endpoint.

    Time complexity: O(N + M), where N is the length of A and M is the length of B
    Space complexity: O(1)
    """
    res = []
    n, m = len(first_list), len(second_list)
    i = j = 0
    while i < n and j < m:
        first_start, first_end = first_list[i]
        second_start, second_end = second_list[j]
        if first_start <= second_end and second_start <= first_end:
            overlap_start = max(first_start, second_start)
            overlap_end = min(first_end, second_end)
            res.append([overlap_start, overlap_end])
        # Advance the interval with smaller endpoint in hopes of finding another overlap
        if first_end < second_end:
            # If A has the smallest endpoint, it can only intersect B, so we can discard A since it cannot
            # intersect any other interval
            i += 1  #
        else:
            j += 1
    return res


def interval_intersection_v2(first_list, second_list):
    """ Same as the previous solution, but trying to find the overlap in a different way.

    Time complexity: O(N + M)
    Space complexity: O(1)
    """
    res = []
    n, m = len(first_list), len(second_list)
    i = j = 0
    while i < n and j < m:
        first_start, first_end = first_list[i]
        second_start, second_end = second_list[j]
        overlap_start = max(first_start, second_start)
        overlap_end = min(first_end, second_end)
        if overlap_start <= overlap_end:  # Find the overlap, if there is any
            res.append([overlap_start, overlap_end])
        if first_end < second_end:
            i += 1
        else:
            j += 1
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
