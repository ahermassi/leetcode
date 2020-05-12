""" Given an array A of integers, a ramp is a tuple (i, j) for which i < j and A[i] <= A[j].  The width of such a ramp
is j - i.
Find the maximum width of a ramp in A.  If one doesn't exist, return 0. """

import unittest2 as unittest


def max_width_ramp_v1(A):
    """ For every index i such as A[i] = v, let's write the indices i in sorted order of their values v.
        For [7, 2, 5, 4], indices array would be [1, 3, 2, 0]. Now these indices are in increasing order of elements.
        Then, whenever we read an index i, we know there was a ramp of width (i - min(previously_read_indices)). We can
        keep track of the minimum of all indices previously read as 'min_index'.
    Time complexity: O(N logN)
    Space complexity: O(N)
    """
    indices = list(range(len(A)))
    indices.sort(key=lambda i: A[i])
    min_index, res = float('inf'), 0
    for cur_index in indices:
        res = max(res, cur_index - min_index)
        min_index = min(min_index, cur_index)
    return res


def max_width_ramp_v2(A):
    """ Keep a stack of decreasing order elements. The stack contains the indices of the elements. The indices
        stored in the stack are increasing, while the elements corresponding to these indices are decreasing. It is
        guaranteed to include A[0], as well as the minimum of A.
        In the second for loop, the indices are looped in decreasing order. Whenever an element corresponding to a
        stack entry is <= A[i], it is popped and the differences in indices are calculated. Since i is the largest
        index with A[i] >= this element (hence i - stack[-1] being the largest), popping it wouldn't cause any problems.
        Those smaller and EARLIER elements stored in the stack will give rise to a bigger width. On the other hand, it
        is certain that some element not included in the stack is the largest element in max-width ramp.
        The stack will only be popped if the last (smallest in A) element is <= A[i], which is guaranteed to be the
        max-width ramp among the ramps with A[stack[-1]] being the smaller element. Removing it would reduce the
        workload and not cause harm. The trick here is: Now we can pop that element out of the stack. Why?
        Let’s say we are right now at index i of the array and stack’s top is at index j. So ramp is j..i. As we are
        iterating backwards in the array, the next possible right end of the ramp will be (i - 1). Even if it forms a
        ramp with j, its length would be shorter than our current ramp (i.e. i - j). So, no point in keeping j in the
        stack.
        Bottom line:
            For each element A[i], we need to go back left to find the farthest element that is <= A[i]
        Why descending order stack? Because for each element we need to look back for a smaller or equal value, and a
        descending order stack can guarantee that the top element is always smaller then or equal to current element.
    Time complexity: O(N)
    Space complexity: O(N)
    """
    stack, n, res = [], len(A), 0
    for i, num in enumerate(A):
        if not stack or num < A[stack[-1]]:
            stack.append(i)
    for i in reversed(range(n)):
        while stack and A[i] >= A[stack[-1]]:
            res = max(res, i - stack.pop())  # If we discover that the current index i could form a ramp with a min
            # index j, we know j couldn't form a better solution since i is going backwards, so we pop j
    return res


class Test(unittest.TestCase):
    data = [([6, 0, 8, 2, 1, 5], 4), ([9, 8, 1, 0, 1, 9, 4, 0, 4, 1], 7)]

    def test_max_width_ramp(self):
        for test_A, result in self.data:
            self.assertEqual(result, max_width_ramp_v1(test_A))
            self.assertEqual(result, max_width_ramp_v2(test_A))


if __name__ == '__main__':
    unittest.main()
