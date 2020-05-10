""" Given two sequences pushed and popped with distinct values, return true if and only if this could have been the
result of a sequence of push and pop operations on an initially empty stack. """

import unittest2 as unittest


def validate_stack_sequences_v1(pushed, popped):
    """ Try to simulate the result. If it is possible, the final stack should be empty at the end.
        At every pushed value, append to the stack, keeping an index to traverse the popped stack. If we find out that
        the top of the stack equals a pop candidate, keep popping from the stack. At the end, we expect a completely
        empty stack if this was a valid combination of inputs.
        We have to push the items in order, so when do we pop them?
        If the stack has say, 2 at the top, then if we have to pop that value next, we must do it now. That's because
        any subsequent push will make the top of the stack different from 2, and we will never be able to pop again.
    Time complexity: O(N)
    Space complexity: O(N)
    """
    i, n = 0, len(pushed)
    stack = []
    for val in pushed:
        stack.append(val)
        while stack and popped[i] == stack[-1]:
            stack.pop()
            i += 1
    return not stack


class Test(unittest.TestCase):
    data = [([1, 2, 3, 4, 5], [4, 5, 3, 2, 1], True), ([1, 2, 3, 4, 5], [4, 3, 5, 1, 2], False)]

    def test_validate_stack_sequences(self):
        for test_pushed, test_popped, result in self.data:
            self.assertEqual(result, validate_stack_sequences_v1(test_pushed, test_popped))


if __name__ == '__main__':
    unittest.main()
