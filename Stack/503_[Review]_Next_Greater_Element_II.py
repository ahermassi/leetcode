""" Given a circular array (the next element of the last element is the first element of the array), print the Next
Greater Number for every element. The Next Greater Number of a number x is the first greater number to its
traversing-order next in the array, which means you could search circularly to find its next greater number. If it
doesn't exist, output -1 for this number. """

import unittest2 as unittest


def next_greater_elements(nums):
    """
    Pattern: Monotonic decreasing stack — next greater element to the right,
    with a circular array.

    The reusable monotonic-stack idea is the same as the normal Next Greater
    Element problem:

        - Scan from left to right.
        - The stack contains indices of elements whose next greater element
          has not been found yet.
        - When the current value is greater than the value at the top of the
          stack, the current value is the first greater element for that
          unresolved element, so we pop it and record the answer.
        - We keep popping because one value can resolve multiple unresolved
          elements.

    The only new complication is that nums is circular.

    For example:

        nums = [5, 4, 3, 2, 1]

    For the value 2, the elements that come after it are not just:

        [1]

    Because the array wraps around, they are:

        [1, 5, 4, 3]

    A simple way to model this is to imagine that the array is duplicated:

        [5, 4, 3, 2, 1, 5, 4, 3, 2, 1]
         ----------------  ----------------
            first pass        wraparound

    Now the circular problem becomes an ordinary "look to the right" problem.
    Every original element gets a chance to see the beginning of the array
    again after reaching the end.

    We do not actually create nums + nums. Instead, we iterate 2 * n times and
    map each virtual position back into the real array with:

        index = i % n

    Example:

        nums = [5, 4, 3, 2, 1]

    During the first pass, the stack eventually contains all five indices,
    because no later value is greater:

        stack values = [5, 4, 3, 2, 1]

    When the traversal wraps around and encounters 5 again:

        5 > 1  -> resolve 1
        5 > 2  -> resolve 2
        5 > 3  -> resolve 3
        5 > 4  -> resolve 4
        5 > 5  -> false

    So the second traversal gives unresolved elements near the end of the
    original array a chance to find their next greater element near the
    beginning.

    We only push indices during the first pass.

    Why?

    The stack represents ORIGINAL elements whose next greater element is still
    unresolved. By the time the first pass finishes, every original element has
    already had its one chance to become unresolved and be pushed onto the
    stack.

    The second pass does not represent new elements. It only simulates wrapping
    around to the beginning of the same circular array so that elements still
    waiting on the stack can find an answer there.

    Therefore:

        First pass:
            - resolve previous elements when possible
            - push each original index once

        Second pass:
            - only use the repeated values to resolve elements still waiting
              on the stack
            - do not push the indices again

    This keeps the invariant especially clean: every index on the stack
    represents one original array element that is still waiting for its next
    greater element.

    Any element that is still unresolved after the full 2 * n traversal has no
    greater value anywhere in circular order, so its answer correctly remains
    -1.

    Time complexity: O(N). We process 2N positions, and every original index is
    pushed once and popped at most once. Since 2N is still O(N), the total time
    complexity is O(N).

    Space complexity: O(N). The stack can contain O(N) indices. The result
    array also contains N elements.
    """
    n = len(nums)
    stack = []
    res = [-1] * n
    for i in range(2 * n):
        index = i % n
        num = nums[index]

        # The current value resolves every smaller unresolved value.
        while stack and num > nums[stack[-1]]:
            res[stack.pop()] = num

        # Only original elements become unresolved candidates.
        # The second pass only simulates wraparound.
        if i < n:
            stack.append(index)

    return res


class Test(unittest.TestCase):
    data = [([1, 2, 1], [2, -1, 2]), ([1, 1, 1, 1], [-1, -1, -1, -1])]

    def test_next_greater_elements(self):
        for test_nums, result in self.data:
            self.assertEqual(result, next_greater_elements(test_nums))


if __name__ == '__main__':
    unittest.main()
