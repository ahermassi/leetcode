""" Design a stack that supports push, pop, top, and retrieving the minimum element in constant time.
push(x) -- Push element x onto stack.
pop() -- Removes the element on top of the stack.
top() -- Get the top element.
getMin() -- Retrieve the minimum element in the stack.
"""

import unittest2 as unittest


class MinStackV1(object):
    """ An important invariant of a Stack is that when a new number, which we'll call x, is placed on a Stack, the
        numbers below it will not change for as long as number x remains on the Stack. So, whenever number x is the top
        of the Stack, the minimum will always be the same, as it's simply the minimum out of x and all the numbers
        below it. Therefore, in addition to putting a number on an underlying Stack inside our MinStack, we could also
        put its corresponding minimum value alongside it.
        Therefore, when we put a new number on the underlying Stack, we need to decide whether the minimum at that
        point is the new number itself, or whether it's the minimum before. It makes sense that it would always be the
        smallest of these two values.
        The idea is to store tuples (value, min_value_till_now) in the stack. This makes getMin() an O(1) operation.
    Time complexity: O(N), for all operations, where N is the total number of operations performed
    Space complexity: O(N), worst case is that all the operations are push
    """

    def __init__(self):
        self.stack = []

    def push(self, x):
        if not self.stack:
            self.stack.append((x, x))
        else:
            self.stack.append((x, min(x, self.stack[-1][1])))  # self.stack[-1][1] will always hold the min value

    def pop(self):
        self.stack.pop()

    def top(self):
        return self.stack[-1][0]

    def getMin(self):
        return self.stack[-1][1] if self.stack else None


class MinStackV2:
    """ There's another, somewhat different approach to implementing a MinStack. Approach 1 required storing two values
        in each slot of the underlying Stack. Sometimes though, the minimum values are very repetitive. We could
        instead have two Stacks inside our MinStack. The main Stack should keep track of the order numbers arrived
        (a standard Stack), and the second Stack should keep track of the current minimum.
        The push method for this implementation of MinStack is straightforward. Items should always be pushed onto the
        main Stack, but they should only be pushed onto the min-tracker Stack if they are smaller than or equal to the
        current top of it.
    Time complexity: O(1)
    Space complexity: O(N)
    """

    def __init__(self):
        self.stack = []
        self.min_stack = []

    def push(self, x: int) -> None:
        self.stack.append(x)
        if not self.min_stack or x <= self.min_stack[-1]:
            self.min_stack.append(x)

    def pop(self) -> None:
        val = self.stack.pop()
        if val == self.min_stack[-1]:
            self.min_stack.pop()

    def top(self) -> int:
        return self.stack[-1]

    def getMin(self) -> int:
        return self.min_stack[-1]


class Test(unittest.TestCase):
    minStack = MinStackV2()
    minStack.push(-2)
    minStack.push(0)
    minStack.push(-3)
    min1 = minStack.getMin()
    minStack.pop()
    top = minStack.top()
    min2 = minStack.getMin()

    def test_min_stack(self):
        self.assertEqual(-3, self.min1)
        self.assertEqual(0, self.top)
        self.assertEqual(-2, self.min2)


if __name__ == '__main__':
    unittest.main()
