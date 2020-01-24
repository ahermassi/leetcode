""" Given two lists of closed intervals, each list of intervals is pairwise disjoint and in sorted order.
Return the intersection of these two interval lists. """

import unittest2 as unittest


def interval_intersection(A, B):
    """ There is guaranteed to be a overlap interval if:
        A[i].start <= B[j].end AND B[j].start <= A[i].end
        If overlap: overlap interval = bigger start index + smaller end index; increment the index of the lesser
        interval.
    Time complexity: O(N + M), where N is the length of A and M is the length of B
    Space complexity: O(1)
    """
    n, m = len(A), len(B)
    i, j, res = 0, 0, []
    while i < n and j < m:
        a, b = A[i], B[j]
        if a[1] < b[0]:  # a ended before b even started
            i += 1
        elif b[1] < a[0]:  # b ended before a even started
            j += 1
        else:  # a.start <= b.end AND b.start <= b.end
            res.append([max(a[0], b[0]), min(a[1], b[1])])
            # Advance the interval with smaller endpoint in hopes of finding another overlap
            if a[1] < b[1]:
                i += 1
            else:
                j += 1
    return res


class Test(unittest.TestCase):
    data = [([[0, 2], [5, 10], [13, 23], [24, 25]], [[1, 5], [8, 12], [15, 24], [25, 26]],
             [[1, 2], [5, 5], [8, 10], [15, 23], [24, 24], [25, 25]])]

    def test_interval_intersection(self):
        for test_a, test_b, result in self.data:
            self.assertEqual(result, interval_intersection(test_a, test_b))


if __name__ == '__main__':
    unittest.main()
