""" Given an array with n objects colored red, unclassified or blue, sort them in-place so that objects of the same color
are adjacent, with the colors in the order red, unclassified and blue.
Here, we will use the integers 0, 1, and 2 to represent the color red, unclassified, and blue respectively. """

from collections import defaultdict
import unittest2 as unittest


def sort_colors_v1(nums):
    """ A rather straightforward solution is a two-pass algorithm using counting sort.
        First, iterate the array counting number of 0's, 1's, and 2's, then overwrite array with total number of 0's,
        then 1's and followed by 2's.
    Time complexity: O(N)
    Space complexity: O(N)
    """
    counter = defaultdict(int)
    for num in nums:
        counter[num] += 1
    nums[:] = [0] * counter[0] + [1] * counter[1] + [2] * counter[2]


def sort_colors_v2(nums):
    """ The problem is known as Dutch National Flag Problem and first was proposed by Dijkstra.
        Let's use here three pointers to track the rightmost boundary of zeros, the leftmost boundary of twos, and the
        current element under the consideration.
        The idea of solution is to move curr pointer along the array.
        If nums[curr] = 0, swap it with nums[left] and move both left and curr pointer forward.
        If nums[curr] = 1, the element is already in correct place, so we don't have to swap, just move the curr
        pointer forward.
        If nums[curr] = 2, swap it with nums[right] and move right pointer backwards.
        We don't increment curr pointer after swapping the value with nums[right] because we know that nums[cur] == 2
        but we don't know the value of nums[right]. After swapping, we need to take another look at this position
        again, e.g. the number we swapped might be 0, wo we have to check it once again.
        For example, suppose we have nums like this:
            0, 0, 1(left), 1, 2(curr), 1, 0(right), 2, 2
            nums[curr] is 2 --> so we swap it with nums[right], and we get:
            0, 0, 1(left), 1, 0(curr), 1, 2(right), 2, 2
            We have to handle that 0(nums[curr]).
        Note that the invariant we have to maintain is:
            nums[:left] are 0s
            nums[left:right+1] are 1s
            nums[right+1:] are 2s
    Time complexity: O(N)
    Space complexity: O(1)
    """
    left, curr, right = 0, 0, len(nums) - 1
    # For all idx < left : nums[idx] == 0
    # For all idx > right : nums[idx] == 2
    # curr is an index of element under consideration
    while curr <= right:
        num = nums[curr]
        if num == 0:
            nums[left], nums[curr] = nums[curr], nums[left]
            left += 1
            curr += 1
        elif num == 1:
            curr += 1
        else:
            nums[right], nums[curr] = nums[curr], nums[right]
            right -= 1


def sort_colors_v3(nums):
    """ Same as previous solution but with more meaningful variable names.
        We iterate through elements in 'unclassified' zone, and move elements into one of 'red' or 'blue' groups
        according to the relative order between the incoming unclassified element and 0/1/2.
    Time complexity: O(N)
    Space complexity: O(1)
    """
    red, unclassified, blue = 0, 0, len(nums) - 1
    while unclassified <= blue:  # Keep iterating as long as there is an unclassified element
        num = nums[unclassified]
        if num == 0:
            nums[red], nums[unclassified] = nums[unclassified], nums[red]
            red += 1
            unclassified += 1
        elif num == 1:
            unclassified += 1
        else:
            nums[unclassified], nums[blue] = nums[blue], nums[unclassified]
            blue -= 1


class Test(unittest.TestCase):
    data = [([2, 0, 2, 1, 1, 0], [0, 0, 1, 1, 2, 2])]

    def test_sort_colors(self):
        for test_array, result in self.data:
            sort_colors_v1(test_array)
            self.assertEqual(result, test_array)


if __name__ == '__main__':
    unittest.main()

