""" Given an array of integers, 1 ≤ a[i] ≤ n (n = size of array), some elements appear twice and others appear once.
Find all the elements that appear twice in this array.
Could you do it without extra space and in O(n) runtime? """

import unittest2 as unittest


def find_duplicates(nums):
    """ A key piece of information in the problem statement is the following:
            The integers in the input array arr satisfy 1 ≤ arr[i] ≤ n, where n is the size of array
        This presents us with two key insights:
            1- All the integers present in the array are positive, i.e. arr[i] > 0 for any valid index i.
            2- The decrement of any integer present in the array must be an accessible index in the array, i.e. for any
               integer x in the array, x-1 is a valid index, and thus, arr[x-1] is a valid reference to an element in
               the array. All elements in the array are integers that lie in the range [1, n]. Thus, their decrements
               are integers that lie in the range [0, n-1] which is precisely the set of valid indices for an array of
               length n.
        Iterate over the array, and for every element x in the array negate the value at index (abs(x) - 1).
        The negation operation effectively marks the value abs(x) as seen/visited. If the value at position
        (abs(x) - 1) is already negative, it means that abs(x) must have seen previously in the array. Therefore,
        we add abs(x) to the result.
        Make sure to use the (abs(x) - 1) to select the index implied by x. That is because the position of x might
        have been marked negative in a previous iteration.
        Example: nums = [4, 3, 2, 7, 8, 2, 3, 1]
        num =  4,  index = |4|  - 1  =  3, nums[3] = 7  > 0  --> nums = [4, 3, 2, -7, 8, 2, 3, 1],    res = []
        num =  3,  index = |3|  - 1  =  2, nums[2] = 2  > 0  --> nums = [4, 3, -2, -7, 8, 2, 3, 1],   res = []
        num = -2,  index = |-2| - 1  =  1, nums[1] = 3  > 0  --> nums = [4, -3, -2, -7, 8, 2, 3, 1],  res = []
        num = -7,  index = |-7| - 1  =  6, nums[6] = 3  > 0  --> nums = [4, -3, -2, -7, 8, 2, -3, 1], res = []
        num =  8,  index = |8|  - 1  =  7, nums[7] = 1  > 0  --> nums = [4, -3, -2, -7, 8, 2, 3, -1], res = []
        num =  2,  index = |2|  - 1  =  1, nums[1] = -3 < 0  --> nums = [4, 3, -2, -7, 8, 2, 3, 1],   res = [2]
        num =  3,  index = |3|  - 1  =  2, nums[2] = -2 < 0  --> nums = [4, -3, -2, -7, 8, 2, 3, 1],  res = [2, 3]
        num =  1,  index = |1|  - 1  =  0, nums[0] = 4  > 0  --> nums = [-4, -3, -2, -7, 8, 2, 3, 1], res = [2, 3]
    Time complexity: O(N)
    Space complexity: O(1)
    """
    res = []
    for num in nums:
        index = abs(num) - 1
        if nums[index] < 0:
            res.append(abs(num))
        nums[index] *= -1
    return res

# Other solutions include:

# Sort and Compare Adjacent Elements:
# After sorting the list of elements, all elements of equivalent value get placed together. Thus, when we sort the
# array, equivalent elements form contiguous blocks.
# Time complexity: O(N logN)
# Space complexity: O(N)

# Store Seen Elements in a Set / Map:
# We store all elements that we've seen till now in a map / set. When we visit an element, we query the map / set to
# figure out if we've seen this element before.
# Time complexity: O(N)
# Space complexity: O(N)


class Test(unittest.TestCase):
    data = [([4, 3, 2, 7, 8, 2, 3, 1], [2, 3])]

    def test_find_duplicates(self):
        for test_nums, result in self.data:
            self.assertEqual(result, find_duplicates(test_nums))


if __name__ == '__main__':
    unittest.main()
