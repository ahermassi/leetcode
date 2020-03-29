""" Given a circular array (the next element of the last element is the first element of the array), print the Next
Greater Number for every element. The Next Greater Number of a number x is the first greater number to its
traversing-order next in the array, which means you could search circularly to find its next greater number. If it
doesn't exist, output -1 for this number. """

import unittest2 as unittest


def next_greater_elements_v1(nums):
    """ Similar to 496- Next Greater Element I.
        We can traverse circularly in the nums array by making use of the %(modulus) operator. For every element
        nums[i], we start searching in the num array(of length n) from the index ((i+1) % n) and look at the next
        (circularly) (n - 1) elements. For nums[i], we do so by scanning over nums[j], such that
        (i+1) % n ≤ j ≤ (i+n-1) % n, and we look for the first greater element found.
    Time complexity: O(N^2)
    Space complexity: O(1)
    """
    n = len(nums)
    res = [-1] * n
    for i in range(n):
        for j in range(1, n):  # We examine the remaining (n - 1) elements by wrapping around using %
            if nums[(i + j) % n] > nums[i]:
                res[i] = nums[(i + j) % n]
                break
    return res


def next_greater_elements_v2(nums):
    """ The approach is same as Next Greater Element I. The only difference here is that we use stack to keep the
        indices of the decreasing sub-sequence. We store the indices instead of the elements since there could be
        duplicates in the array. This time, we need to traverse the whole array twice since it is circular, so even
        the very first elements can be potential next greater for the later ones.
        We start traversing the array from left towards the right. For an element nums[i] encountered, we pop all the
        elements stack[top] from the stack such that nums[stack[top]] < nums[i]. We continue the popping till we
        encounter a stack[top] satisfying nums[stack[top]] >= nums[i]. Now, it is obvious that the current stack[top]
        only can act as the next greater element for nums[i] (right now, considering only the elements lying to the
        left of nums[i]).
        If no element remains on the top of the stack, it means no larger element than nums[i] exists to its left.
        Along with this, we also push the index of the element just encountered (nums[i]), i.e. i over the top of the
        stack, so that nums[i] (or stack[top]) now acts as the next greater element for the elements lying to its left.
        We go through two such passes over the complete array. This is done so as to complete a circular traversal
        over the array.
    Time complexity: O(N)
    Space complexity: O(N)
    """
    n, greater, stack = len(nums), {}, []
    for i in range(2 * n):
        num = nums[i % n]
        while stack and nums[stack[-1]] < num:
            greater[stack.pop()] = num
        stack.append(i % n)
    return [greater.get(i, -1) for i in range(n)]


class Test(unittest.TestCase):
    data = [([1, 2, 1], [2, -1, 2]), ([1, 1, 1, 1], [-1, -1, -1, -1])]

    def test_next_greater_elements(self):
        for test_nums, result in self.data:
            self.assertEqual(result, next_greater_elements_v1(test_nums))
            self.assertEqual(result, next_greater_elements_v2(test_nums))


if __name__ == '__main__':
    unittest.main()
