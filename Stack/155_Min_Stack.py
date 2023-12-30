""" Design a stack that supports push, pop, top, and retrieving the minimum element in constant time.
push(x) -- Push element x onto stack.
pop() -- Removes the element on top of the stack.
top() -- Get the top element.
getMin() -- Retrieve the minimum element in the stack.
"""

import unittest2 as unittest


class MinStackV1(object):
    """ We're told that all the MinStack operations must run in constant time, i.e. O(1) time. For this reason, we can
         immediately rule out the use of a Binary Search Tree or Heap. While these data structures are often great for
         keeping track of a minimum, their core operations (find, add, and remove) are O(logN), which isn't good enough
         here. We will need to explore better ways.

        An important invariant of a stack is that when a new number, which we'll call x, is placed on a stack, the
        numbers below it will not change for as long as number x remains on the stack. Numbers could come and go above
        x for the duration of x's presence, but never below.

        So, whenever number x is the top of the stack, the minimum will always be the same, as it's simply the minimum
        out of x and all the numbers below it.

        Therefore, in addition to putting a number on an underlying stack inside our MinStack, we could also put its
        corresponding minimum value alongside it. Then whenever that particular number is at the top of the underlying
        stack, the getMin() operation of MinStack is as simple as retrieving its corresponding minimum value.

        Therefore, when we put a new number on the underlying stack, we need to decide whether the minimum at that
        point is the new number itself, or whether it's the minimum before. It makes sense that it would always be the
        smallest of these two values.

        The idea is to store tuples (value, min_value_till_now) in the stack. This makes getMin() an O(1) operation.

    Time complexity: O(1)
    Space complexity: O(N), worst case is that all the operations are push
    """

    def __init__(self):
        self.stack = []

    def push(self, x):
        # Each node stores the min value AT OR BELOW it
        if not self.stack:
            self.stack.append((x, x))
        else:
            # self.stack[-1][1] will always hold the min value
            self.stack.append((x, min(x, self.stack[-1][1])))

    def pop(self):
        self.stack.pop()

    def top(self):
        return self.stack[-1][0]

    def getMin(self):
        return self.stack[-1][1]


class MinStackV2:
    """ There's another, somewhat different approach to implementing a MinStack. Approach 1 required storing two values
         in each slot of the underlying stack. Sometimes though, the minimum values are very repetitive. Do we actually
         need to store the same minimum value over and over again?

         We could instead have two stacks inside our MinStack. The main stack should keep track of the order numbers
         arrived (a standard stack), and the second stack should keep track of the current minimum.

        The push method for this implementation of MinStack is straightforward. Items should always be pushed onto the
        main stack, but they should only be pushed onto the min stack if they are smaller than or equal to the
        current top of it.

        Well, that's mostly correct. There's one potential pitfall here.

        For pop() method, the value we actually need to pop is always on the top of the main stack. However, if we
        simply popped it from there, the min stack could become incorrect if its top value had been removed from the
        main stack during this pop operation.

        A logical solution would be to do the following additional check and modification to the min stack when pop()
        method is called:

                    If top of main_stack == top of min stack:
                        min_stack.pop()

        This way, the new minimum would now be the top of the min stack.

        Note that instead of only pushing numbers to min stack if they are less than the current minimum, we have to
        push them if they are less than or equal to it. This is because the current minimum value could be pushed
        (and popped) multiple times to/from the main stack.

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
        if self.stack.pop() == self.min_stack[-1]:
            self.min_stack.pop()

    def top(self) -> int:
        return self.stack[-1]

    def getMin(self) -> int:
        return self.min_stack[-1]


class MinStackV3:
    """ In the above approach, we pushed a new number onto the min_stack if, and only if, it was less than or
        equal to the current minimum. One downside of this solution is that if the same number is pushed repeatedly
        onto MinStack, and that number also happens to be the current minimum, there'll be a lot of needless repetition
        on the min_stack.

        An improvement is to put pairs onto the min_stack. The first value of the pair would be the same as before, and
        the second value would be how many times that minimum was repeated.

    Time complexity: O(1)
    Space complexity: O(N)
    """

    def __init__(self):
        self.stack = []
        self.min_stack = []

    def push(self, x: int) -> None:
        self.stack.append(x)
        if not self.min_stack or x < self.min_stack[-1][0]:  # If the min stack is empty, or this number is smaller
            # than the top of the min stack, put it on with a count of 1
            self.min_stack.append([x, 1])
        elif x == self.min_stack[-1][0]:  # If this number is equal to what's currently at the top of the min_stack,
            # then increment the count at the top by 1
            self.min_stack[-1][1] += 1

    def pop(self) -> None:
        if self.stack.pop() == self.min_stack[-1][0]:
            self.min_stack[-1][1] -= 1
            if self.min_stack[-1][1] == 0:
                self.min_stack.pop()

    def top(self) -> int:
        return self.stack[-1]

    def getMin(self) -> int:
        return self.min_stack[-1][0]


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
