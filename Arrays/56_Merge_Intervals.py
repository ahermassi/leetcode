""" Given a collection of intervals, merge all overlapping intervals. """

import unittest2 as unittest


def merge(intervals):
    """ If we sort the intervals by their start value, then each set of intervals that can be merged will appear as a
         contiguous "run" in the sorted list.

        Two intervals i1 and i2 overlap if the following two conditions are met:

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

        We pre-process the list by sorting intervals by start. This way, requirement #1 i1.start <= i2.start < i2.end is
        met. We only have to compare i1.end with i2.start to see if requirement #2 is satisfied.

        First, we sort the list. Then, we consider each interval in turn as follows:

            - If the current interval begins after the previous interval ends, then they do NOT overlap, and we can
               append the current interval to 'merged'.

            - Otherwise, they do overlap, and we merge them by updating the end of the previous interval if it is less
               than the end of the current interval.

        When the intervals are sorted, all mergeable intervals form contiguous blocks.

    Time complexity: O(N logN), the complexity of sorting
    Space complexity: O(N), if we can sort intervals in place, we do not need more than constant additional space.
    Otherwise, we must allocate linear space to store a copy of intervals and sort that.
    """
    intervals.sort()
    merged = []
    for start, end in intervals:
        # If the list of merged intervals is empty or if the current interval does not overlap with the previous,
        # simply append it
        if not merged or start > merged[-1][1]:
            merged.append([start, end])
        else:
            # Otherwise, there is an overlap, so we merge the current and previous intervals
            merged[-1][1] = max(merged[-1][1], end)
    return merged

# There seems to be a follow-up at Facebook to implement the algorithm with no sorting, using a BST.
# https://leetcode.com/problems/merge-intervals/discuss/21451/Share-my-BST-interval-tree-solution-C%2B%2B-No-sorting!
# https://leetcode.com/problems/merge-intervals/discuss/355318/Fully-Explained-and-Clean-Interval-Tree-for-Facebook-Follow-Up-No-Sorting
# https://leetcode.com/articles/merge-intervals/


class Test(unittest.TestCase):
    data = [([[1, 3], [2, 6], [8, 10], [15, 18]], [[1, 6], [8, 10], [15, 18]]),
            ([[1, 4], [4, 5]], [[1, 5]])]

    def test_merge(self):
        for test_array, result in self.data:
            self.assertEqual(result, merge(test_array))


if __name__ == '__main__':
    unittest.main()
