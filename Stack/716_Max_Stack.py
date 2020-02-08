""" Design a max stack that supports push, pop, top, peekMax and popMax.
push(x) -- Push element x onto stack.
pop() -- Remove the element on top of the stack and return it.
top() -- Get the element on the top.
peekMax() -- Retrieve the maximum element in the stack.
popMax() -- Retrieve the maximum element in the stack, and remove it. If you find more than one maximum elements, only
remove the top-most one.
"""

import unittest2 as unittest


class MaxStack(object):
    """ The idea is to store tuples (value, max_value_till_now) in the stack. This makes peekMax() an O(1) operation.
        More care needs to be taken with peekMax(). After popping the element whose value is the same as max, the
        tricky part is to apply push() on the temporary stack in reversed order.
    """

    def __init__(self):
        self.stack = []

    def push(self, x):
        if not self.stack:
            self.stack.append((x, x))
        else:
            self.stack.append((x, max(x, self.stack[-1][1])))

    def pop(self):
        return self.stack.pop()[0]

    def top(self):
        return self.stack[-1][0]

    def peekMax(self):
        return self.stack[-1][1]

    def popMax(self):
        max_val = self.stack[-1][1]
        temp = []
        while self.stack[-1][0] != max_val:
            temp.append(self.stack.pop()[0])
        self.stack.pop()
        map(self.push, reversed(temp))
        return max_val


class Test(unittest.TestCase):
    maxStack = MaxStack()
    maxStack.push(5)
    maxStack.push(1)
    maxStack.push(5)
    top1 = maxStack.top()
    max1 = maxStack.popMax()
    top2 = maxStack.top()
    max2 = maxStack.peekMax()
    pop = maxStack.pop()
    top3 = maxStack.top()

    def test_max_stack(self):
        self.assertEqual(5, self.top1)
        self.assertEqual(5, self.max1)
        self.assertEqual(1, self.top2)
        self.assertEqual(5, self.max2)
        self.assertEqual(1, self.pop)
        self.assertEqual(5, self.top3)


if __name__ == '__main__':
    unittest.main()