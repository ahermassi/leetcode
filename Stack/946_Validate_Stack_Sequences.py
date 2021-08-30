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
        while stack and stack[-1] == popped[i]:
            stack.pop()
            i += 1
    return not stack


def validate_stack_sequences_v2(pushed, popped):
    """ Can we do better ?
        We cannot improve the time complexity but we can improve the space complexity.
        If we observe carefully, we can notice that pushed array's content would be the same as that of the stack we
        use in approach 1.
        Ex: pushed = [1, 2, 3, 4], popped = [4, 3, 2, 1]
        In this sequence we notice that stack = [1, 2, 3, 4] when i=3 and j=0, which means that we can reuse the pushed
        array as a stack.
        However, in cases like pushed = [1, 2, 3, 4, 5], popped = [4, 5, 3, 2, 1] , where i=3 and j=0 we have to remove
        pushed[3].
        Removing from an array at index i which would take O(N) time, increasing our time complexity.
        The solution is to use partition algorithm. We maintain 2 pointers :
            i: pointer which represents the top of stack in pushed array
            j: pointer which represents the current element to be processed in popped array
        We maintain the pushed array such that:
            Anything in the range of 0 till i : valid stack elements
            Anything in the range of current element val's index till n : To be pushed elements
            Anything in the range of i till current element 'val' : Popped elements.
        The idea is to overwrite the popped elements with new elements to be pushed in the subsequent iterations.
    Time complexity: O(N)
    Space complexity: O(1)
    """
    i, j, n = 0, 0, len(pushed)
    for val in pushed:
        pushed[i] = val
        while i >= 0 and pushed[i] == popped[j]:
            i -= 1
            j += 1
        i += 1
    return i == 0


class Test(unittest.TestCase):
    data = [([1, 2, 3, 4, 5], [4, 5, 3, 2, 1], True), ([1, 2, 3, 4, 5], [4, 3, 5, 1, 2], False)]

    def test_validate_stack_sequences(self):
        for test_pushed, test_popped, result in self.data:
            self.assertEqual(result, validate_stack_sequences_v1(test_pushed, test_popped))
            self.assertEqual(result, validate_stack_sequences_v2(test_pushed, test_popped))


if __name__ == '__main__':
    unittest.main()
