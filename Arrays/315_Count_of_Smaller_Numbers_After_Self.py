""" You are given an integer array nums and you have to return a new counts array. The counts array has the property
where counts[i] is the number of smaller elements to the right of nums[i]. """

import unittest2 as unittest


# Video explanation: https://youtu.be/ffbwCfJ2Qjw?t=79

def count_smaller(nums):
    """ The smaller numbers on the right of a number are exactly those that jump from its right to its left during a
        stable sort. So we do merge sort with added tracking of those right-to-left jumps.
        The standard merge algorithm is already checking for cases which this coding problem is asking for: Numbers
        positioned to the right of the current element that are smaller than the current element.
        While merging two merged sub arrays i.e., 'left' & 'right', we check left or right element who is greater or
        smaller, then we merge. We can exploit this property by keeping a counter, 'right_numbers_moved', of the number
        of elements moved from the right sub-array to the merged area.
        Take this example: nums = [5, 2, 6, 1]. Let's do normal merge sort on this given array.
        First, just as normal merge sort, we recursively split the array and go top-down until each sub-array is of
        size 1.
        [5, 2, 6, 1]
        left=[5, 2], right=[6, 1]
        (left=[5], right=[2]) (left=[6], right=[1])
        Result count: 5(0) 2(0) 6(0) 1(0)
        If we merge up one level from the bottom:
            - 2 is smaller than, and to the right of 5 ==> increment count for 5
            - 1 is smaller than, and to the right of 6 ==> increment count for 6
        [5, 2, 6, 1]
        left=[2, 5], right=[1, 6]
        Result count: 5(1) 2(0) 6(1) 1(0)
        Now we have to merge: left=[2, 5], right=[1, 6]
        Notice that: All elements in right sub-array are originally positioned to the right of all elements of the left
        sub-array.
        Take this example: left=[9, 11, 15], right=[2, 5, 6], merged: [], right_numbers_moved=0
        - Compare 2 and 9
        - 2 is less than 9 and positioned to the right side of 9
        - DO NOT increment result count for 9
        - Increment right_numbers_moved: right_numbers_moved=1
        - Move 2 to merged area
        - Repeat for 5
            - Increment right_numbers_moved: right_numbers_moved=2
            - Move 5 to merged area
        - Repeat for 6
            - Increment right_numbers_moved: right_numbers_moved=3
            - Move 6 to merged area
        The state now is: left=[9, 11, 15], right=[], merged=[2, 5, 6], right_numbers_moved=3
        Result count: 9(0) 11(0) 15(0)
        right_numbers_moved=3 indicates there are currently 3 elements less than 9 that are to the right side of 9.
        Since right side sub-array is empty, we move all elements in left sub-array to merged area.
        right_numbers_moved= 3, so we add 3 to the result count of 9, and move 9 to the merged area.
        We repeat for elements 11 and 15.
        Finally, result count: 9(3) 11(3) 15(3)
    Time complexity: O(N logN)
    Space complexity: O(N)
    """

    def mergeSort(start, end):
        if start > end:
            return []
        if start == end:
            return [tuples[start]]
        mid = (start + end) // 2
        left = mergeSort(start, mid)
        right = mergeSort(mid + 1, end)
        n, m, merged = len(left), len(right), []
        i = j = 0
        right_numbers_moved = 0
        while i < n or j < m:  # If we used (while i < n and j < m) instead, we'd have to check for both i < n and j < m
            # at the end of the while loop, so we make the code shorter with a tweak of the first if condition
            if i == n or j < m and right[j][1] < left[i][1]:  # Instead of (if right[j][1] < left[i][1])
                # This code block is exactly what the problem is asking us for: A number from the right side of the
                # original input array that is smaller than a number from the left side.
                # right[j][1] is smaller than the element of the left sub-array at index i. Since left sub-array is
                # already sorted, right[j][1] must also be smaller than the entire remaining left sub-array.
                merged.append(right[j])
                right_numbers_moved += 1
                j += 1
            else:
                merged.append(left[i])
                res[left[i][0]] += right_numbers_moved
                i += 1
        return merged

    if not nums:
        return None
    tuples = [(i, num) for i, num in enumerate(nums)]  # Store the original index position of each value before sorting
    res = [0] * (len(nums))
    mergeSort(0, len(nums) - 1)
    return res


class Test(unittest.TestCase):
    data = [([5, 2, 6, 1], [2, 1, 1, 0])]

    def test_count_smaller(self):
        for test_nums, result in self.data:
            self.assertEqual(result, count_smaller(test_nums))


if __name__ == '__main__':
    unittest.main()
