""" Design a stack that supports push, pop, top, and retrieving the minimum element in constant time.
push(x) -- Push element x onto stack.
pop() -- Removes the element on top of the stack.
top() -- Get the top element.
getMin() -- Retrieve the minimum element in the stack.
"""

import unittest2 as unittest


class MinStack(object):

    """ The idea is to store tuples (value, min_value_till_now) in the stack. This makes getMin() an O(1) operation. """

    def __init__(self):
        """
        initialize your data structure here.
        """
        self.stack = []

    def push(self, x):
        """
        :type x: int
        :rtype: None
        """
        if not self.stack:
            self.stack.append((x, x))  # Notice the tuple here
        else:
            self.stack.append((x, min(x, self.stack[-1][1])))  # self.stack[-1][1] will always hold the min value

    def pop(self):
        """
        :rtype: None
        """
        self.stack.pop()

    def top(self):
        """
        :rtype: int
        """
        return self.stack[-1][0]

    def getMin(self):
        """
        :rtype: int
        """
        if not self.stack:
            return None
        return self.stack[-1][1]


class Test(unittest.TestCase):
    minStack = MinStack()
    minStack.push(-2)
    minStack.push(0)
    minStack.push(-3)
    min1 = minStack.getMin()
    minStack.pop()
    top = minStack.top()
    min2 = minStack.getMin()

    def test_is_valid(self):
        self.assertEqual(-3, self.min1)
        self.assertEqual(0, self.top)
        self.assertEqual(-2, self.min2)


if __name__ == '__main__':
    unittest.main()