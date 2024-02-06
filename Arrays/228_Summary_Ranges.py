""" Given a sorted integer array without duplicates, return the summary of its ranges. """

import unittest2 as unittest


def summary_ranges(nums):
    """ Because the nums array is sorted, two consecutive elements in nums with a difference greater than 1 cannot
         belong to the same range. Also, if the difference between two consecutive elements in nums is 1, they should
         be put in the same range.

         We also need to know the start index of a range so that we can put it in the result list. Thus, we keep two
         indices representing the two boundaries of the current range. For each new element, we check if it extends the
         current range. If not, we put the current range into the list.

            - Create a list of strings 'ranges' that contains the final output.

            - Iterate over all the elements in nums with the pointer i = 0.

            - Each iteration of the outermost loop represents finding one range. To start, save the current range's
               beginning index i.

            - Check whether the next element in nums at index (i + 1) differs from nums[i] by 1 or more. If the next
               element differs by 1, we increase i by 1 to include the (i+1)th element in this range and move ahead to
               check the next element. We keep adding elements in this range as long as the successive elements differ
               by 1.

            - Otherwise, if the next element differs by more than 1, or we have covered all the elements in nums, we
               check whether start is equal to nums[i] or not. If start == nums[i], we only add start as a string to
               ranges as we just have a single element in this range. Otherwise, if start != nums[i], we add the string
               start->nums[i] to ranges and start a new range.

    Time complexity: O(N), we iterate over each nums element once, either including it in the current range or creating
    a new range from it, which takes O(N) time for N elements. We also add all the ranges to the ranges list. In the
    worst-case situation, N elements could be added to the list if each consecutive element in nums differs by more
    than 1, requiring O(N) time to insert all the required ranges
    Space complexity: O(1)
    """
    n, ranges = len(nums), []
    i = 0
    while i < n:
        j = i
        while j < n - 1 and nums[j + 1] == nums[j] + 1:
            j += 1
        if j != i:
            ranges.append(str(nums[i]) + '->' + str(nums[j]))
        else:
            ranges.append(str(nums[i]))
        i = j + 1
    return ranges


class Test(unittest.TestCase):
    data = [([0, 1, 2, 4, 5, 7], ['0->2', '4->5', '7']), ([0, 2, 3, 4, 6, 8, 9], ['0', '2->4', '6', '8->9'])]

    def test_summary_ranges(self):
        for test_nums, result in self.data:
            self.assertEqual(result, summary_ranges(test_nums))


if __name__ == '__main__':
    unittest.main()
