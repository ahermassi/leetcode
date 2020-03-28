""" You are given two arrays (without duplicates) nums1 and nums2 where nums1’s elements are subset of nums2. Find
all the next greater numbers for nums1's elements in the corresponding places of nums2.
Example:
Input: nums1 = [4,1,2], nums2 = [1,3,4,2].
Output: [-1,3,-1] """

import unittest2 as unittest


def next_greater_element_v1(nums1, nums2):
    """ We pick up every element of the nums1 array(say nums1[i]) and then search for its own occurrence in the nums2
        array. Instead of searching for the occurrence of nums1[i] linearly in the nums2 array, we can make use of a
        hash map to store the elements of nums2 in the form of (element,index). By doing this, we can find nums1[i]'s
        index in nums2 array directly and then continue to search for the next larger element in a linear fashion.
    Time complexity: O(N * M), where N is the length of nums1 and M is the length of nums2
    Space complexity: O(M)
    """
    index = {num: i for i, num in enumerate(nums2)}
    n, res = len(nums2), []
    for num in nums1:
        next_greater = index[num]
        for j in range(next_greater + 1, n):
            if nums2[j] > num:
                next_greater = j
                break
        res.append(-1 if next_greater == index[num] else nums2[next_greater])
    return res


def next_greater_element_v2(nums1, nums2):
    """ We iterate over the nums2 array from left to right. We push every element nums2[i] to the stack if it is less
        than the element on the top of the stack. No entry is made in map for nums2[i] right now because the elements
′       encountered so far are coming in a descending order.
        If we encounter an element nums2[i] such that nums2[i] > stack[-1], we keep on popping all the elements from
        the stack until we encounter stack[k] such that stack[k] > nums[i]. For every element popped out of the stack
        stack[j], we put the popped element along with its next greater number into the map, in the form
        (stack[j], nums[i]). Now, it is obvious that the next greater element for all elements stack[j], such that
        k < j ≤ top is nums[i] (since this larger element caused all the stack[j]'s to be popped out).
        Thus, an element is popped out of the stack whenever a next greater element is found for it. Therefore, the
        elements remaining in the stack are the ones for which no next greater element exists in the nums2 array.
        Summary:
        We use a stack to keep a decreasing sub-sequence. Whenever we see a number x greater than the top of the stack,
        we pop all elements less than x and for all the popped ones, their next greater element is x.
        For example num2 = [9, 8, 7, 3, 2, 1, 6]. The stack will first contain [9, 8, 7, 3, 2, 1] and then we see 6
        which is greater than 1, so we pop 1, 2, and 3 whose next greater element should be 6.
    Time complexity: O(N + M),
    Space complexity: O(N + M)
    """
    greater, stack = {}, []
    for num in nums2:
        while stack and stack[-1] < num:
            greater[stack.pop()] = num
        stack.append(num)
    return [greater.get(num, -1) for num in nums1]


class Test(unittest.TestCase):
    data = [([4, 1, 2], [1, 3, 4, 2], [-1, 3, -1]),
            ([2, 4], [1, 2, 3, 4], [3, -1])
            ]

    def test_next_greater_element(self):
        for nums1, nums2, result in self.data:
            self.assertEqual(result, next_greater_element_v1(nums1, nums2))
            self.assertEqual(result, next_greater_element_v2(nums1, nums2))


if __name__ == '__main__':
    unittest.main()
