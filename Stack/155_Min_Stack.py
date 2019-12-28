""" Design a stack that supports push, pop, top, and retrieving the minimum element in constant time.
push(x) -- Push element x onto stack.
pop() -- Removes the element on top of the stack.
top() -- Get the top element.
getMin() -- Retrieve the minimum element in the stack.
"""

import unittest2 as unittest


class MinStackV1(object):
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


class MinStackV2:
    """ If the value x we want to push is less than or equal to the current min value, we push min to the stack and
        update min to be equal to x. This way when the pop operation could result in popping the current min value,
        we pop twice and change the current min value to the previous min value.
        Core Idea:
            1- Minimum value is always followed by the second minimum value
            2- While popping, if we pop min we also pop 2nd min so that we get the correct min value for the remaining
               stack and the remaining stack top also points to the correct value.
    """

    def __init__(self):
        """
        initialize your data structure here.
        """
        self.stack = []
        self.min = float('inf')

    def push(self, x):
        if x <= self.min:
            self.stack.append(self.min)
            self.min = x
        self.stack.append(x)

    def pop(self):
        if self.stack.pop() == self.min:
            self.min = self.stack.pop()

    def top(self):
        return self.stack[-1]

    def getMin(self):
        return self.min


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