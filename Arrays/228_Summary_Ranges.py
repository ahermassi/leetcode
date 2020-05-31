""" Given a sorted integer array without duplicates, return the summary of its ranges. """

import unittest2 as unittest


def summary_ranges(nums):
    """ A range covers consecutive elements. If two adjacent elements have difference larger than 11, the two elements
        does not belong to the same range.
        To summarize the ranges, we need to know how to separate them. The array is sorted and without duplicates.
        In such array, two adjacent elements have difference either 1 or larger than 1. If the difference is 1, they
        should be put in the same range; otherwise, separate ranges.
        We also need to know the start index of a range so that we can put it in the result list. Thus, we keep two
        indices 'start' and 'end' representing the two boundaries of current range. For each new element, we check if
        it extends the current range. If not, we put the current range into the list.
    Time complexity: O(N)
    Space complexity: O(1)
    """
    n, res, start = len(nums), [], 0
    while start < n:
        end = start
        while end < n - 1 and nums[end + 1] == nums[end] + 1:
            end += 1
        if end != start:
            res.append(str(nums[start]) + '->' + str(nums[end]))
        else:
            res.append(str(nums[start]))
        start = end + 1
    return res


class Test(unittest.TestCase):
    data = [([0, 1, 2, 4, 5, 7], ['0->2', '4->5', '7']), ([0, 2, 3, 4, 6, 8, 9], ['0', '2->4', '6', '8->9'])]

    def test_summary_ranges(self):
        for test_nums, result in self.data:
            self.assertEqual(result, summary_ranges(test_nums))


if __name__ == '__main__':
    unittest.main()
