""" Implement the following operations of a queue using stacks:
push(x) -- Push element x to the back of queue.
pop() -- Removes the element from in front of queue.
peek() -- Get the front element.
empty() -- Return whether the queue is empty.
You must use ONLY standard operations of a stack -- which means only push to TOP, peek/pop from TOP, size,
and is empty operations are valid. """

import unittest2 as unittest


class MyQueue:
    """ 1st implementation
    Time complexity: O(N) push, O(1) pop
    """
    def __init__(self):
        self.s1 = []  # This stack is used to hold actual queue elements
        self.s2 = []  # This stack is used to copy data from and back to the queue

    def push(self, x):
        """ Stack is LIFO. To serve as a FIFO, the newest element must be pushed to the bottom of the
        stack. Transfer all s1 elements to auxiliary stack s2. Then the newly arrived element is
        pushed on top of s2 and all its elements are popped and pushed to s1. """
        while self.s1:
            self.s2.append(self.s1.pop())
        self.s1.append(x)
        while self.s2:
            self.s1.append(self.s2.pop())

    def pop(self):
        return self.s1.pop()

    def peek(self):
        return self.s1[-1]

    def empty(self):
        return not self.s1


class Test(unittest.TestCase):
    myqueue = MyQueue()
    myqueue.push(1)
    myqueue.push(2)
    i = myqueue.pop()
    front = myqueue.peek()
    is_empty = myqueue.empty()

    def test_my_queue(self):
        self.assertEqual(1, self.i)
        self.assertEqual(2, self.front)
        self.assertFalse(self.is_empty)


if __name__ == '__main__':
    unittest.main()
