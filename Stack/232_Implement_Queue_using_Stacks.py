""" Implement the following operations of a queue using stacks:
push(x) -- Push element x to the back of queue.
pop() -- Removes the element from in front of queue.
peek() -- Get the front element.
empty() -- Return whether the queue is empty.
You must use ONLY standard operations of a stack -- which means only push to TOP, peek/pop from TOP, size,
and is empty operations are valid. """

import unittest2 as unittest


class MyQueue1:
    """ 1st implementation
    """
    def __init__(self):
        self.stack1 = []  # This stack is used to hold actual queue elements
        self.stack2 = []  # This stack is used to copy data from and back to the queue

    def push(self, x):
        """ Stack is LIFO. To serve as a FIFO, the newest element must be pushed to the bottom of the stack.
            Transfer all stack1's elements to auxiliary stack2. Then the newly arrived element is pushed on top of
            stack1 and all stack2's elements are popped and pushed to stack1.
        Time complexity: O(N), each element, with the exception of the newly arrived, is pushed and popped twice
        Space complexity: O(N)
        """
        while self.stack1:
            self.stack2.append(self.stack1.pop())
        self.stack1.append(x)
        while self.stack2:
            self.stack1.append(self.stack2.pop())

    def pop(self):
        """ Pop an element from stack1 because stack1 stores always on its top the first inserted element in the
            queue.
        Time complexity: O(1)
        Space complexity: O(1)
        """
        return self.stack1.pop()

    def peek(self):
        return self.stack1[-1]

    def empty(self):
        return not self.stack1


class MyQueue2:
    """ 2nd implementation
        The intuition for improving the time complexity of de-queue is that after we move elements from the first
        stack to the second stack, any further de-queues are trivial, until the second stack is empty. This is true
        even if we need to enqueue, as long as we enqueue onto the first stack. When the second stack becomes empty,
        and we need to perform a de-queue, we simply repeat the process of transferring from the first stack to the
        second stack.
        In essence, we are using the first stack for enqueue and the second for de-queue.
    """
    def __init__(self):
        self.enqueue = []
        self.dequeue = []

    def push(self, x):
        """ The newly arrived element is always added on top of 'enqueue' stack.
        Time complexity: O(1)
        Space complexity: O(1)
        """
        self.enqueue.append(x)

    def pop(self):
        """ We have to remove element in front of the queue. This is the first inserted element in the 'enqueue' stack
            and is positioned at the bottom of the stack. To remove the bottom element from 'enqueue', we have to pop
            all elements from 'enqueue' and to push them on to additional 'dequeue' stack, which helps us to store the
            elements of 'enqueue' in reversed order. This way the bottom element of 'enqueue' will be positioned on top
            of 'dequeue' and we can simply pop it from 'dequeue'. Once 'dequeue' is empty, the algorithm transfers
            data from  'enqueue' to 'dequeue' again. """
        if self.dequeue:
            return self.dequeue.pop()
        while self.enqueue:
            self.dequeue.append(self.enqueue.pop())
        return self.dequeue.pop()

    def peek(self):
        if self.dequeue:
            return self.dequeue[-1]
        return self.enqueue[0]

    def empty(self):
        """ Both stacks s1 and s2 contain all stack elements, so the algorithm checks s1 and s2 size to return if the
        queue is empty. """
        return not self.enqueue and not self.dequeue


class Test(unittest.TestCase):
    myqueue1 = MyQueue1()
    myqueue1.push(1)
    myqueue1.push(2)
    i = myqueue1.pop()
    front1 = myqueue1.peek()
    is_empty1 = myqueue1.empty()
    myqueue2 = MyQueue2()
    myqueue2.push(1)
    myqueue2.push(2)
    j = myqueue2.pop()
    front2 = myqueue2.peek()
    is_empty2 = myqueue2.empty()

    def test_my_queue(self):
        self.assertEqual(1, self.i)
        self.assertEqual(2, self.front1)
        self.assertFalse(self.is_empty1)
        self.assertEqual(1, self.j)
        self.assertEqual(2, self.front2)
        self.assertFalse(self.is_empty2)


if __name__ == '__main__':
    unittest.main()
