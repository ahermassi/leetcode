""" Given a nested list of integers, implement an iterator to flatten it.
Each element is either an integer, or a list -- whose elements may also be integers or other lists. """


# """
# This is the interface that allows for creating nested lists.
# You should not implement it, or speculate about its implementation
# """
# class NestedInteger(object):
#    def isInteger(self):
#        """
#        @return True if this NestedInteger holds a single integer, rather than a nested list.
#        :rtype bool
#        """
#
#    def getInteger(self):
#        """
#        @return the single integer that this NestedInteger holds, if it holds a single integer
#        Return None if this NestedInteger holds a nested list
#        :rtype int
#        """
#
#    def getList(self):
#        """
#        @return the nested list that this NestedInteger holds, if it holds a nested list
#        Return None if this NestedInteger holds a single integer
#        :rtype List[NestedInteger]
#        """

class NestedIteratorV1(object):
    """ In the constructor, we push all the nestedList into the stack from back to front, so when we pop the stack, it
        returns the very first element. Second, in the hasNext() function, we peek the first element currently in the
        stack, and if it is an Integer, we will return true and pop the element. If it is a list, we will further
        flatten it.
        While this solution can pass test cases, it is 'wrong' in real world situations because hasNext() changes the
        state. It can also be wrong if the first call is next() without calling hasNext(). We can avoid it by adding
        the check if hasNext() inside next() function.
    """

    def __init__(self, nestedList):
        self.stack = nestedList[::-1]  # Store the nested list elements in reversed order to allow faster access
        # to stack top

    def next(self):
        return self.stack.pop().getInteger()

    def hasNext(self):
        while self.stack and not self.stack[-1].isInteger():
            for element in reversed(self.stack.pop().getList()):
                self.stack.append(element)
        return self.stack


class NestedIteratorV2(object):
    """ hasNext() doesn't change the state. We separate the list flattening from hasNext().
        It is cleaner if hasNext() simply returns false if the stack is empty, otherwise true.
        For the test case '[[]]', hasNext() will return true since the stack is not empty (empty nested list is still a
        nested list), but actually there is no 'next integer' in this list. It's impossible for next() to return a
        valid value since it can only return an int. So we should first flatten the list and then check if the stack is
        really empty. The best way is to advance to the next actual Integer BEFORE we call next(), then hasNext() is
        just checking if the pointer is at an integer.
        Notice that the stack is shared between calls. This means that next() will find an integer and return it, while
        still preserving the state of the stack. We can then call next() again to get the next integer, and so forth.
        The loop condition checks if the top of the stack is still a list. The loop body should push the contents of
        the list onto the stack (in reverse). Eventually, there will be an integer on the top of the stack, OR the
        stack will be empty. Being able to get the next integer to the top of the stack allows the next() and hasNext()
        methods to access it.
    """
    def __init__(self, nestedList):
        """
        Time complexity: O(N + L), the worst-case occurs when the initial input nestedList consists entirely of
        integers and empty lists (everything is in the top-level). In this case, every item is reversed and stored,
        giving a total time complexity of O(N + L).
        Space complexity: O(N + L), in the worst case, where the top list contains N integers, or L empty lists, it
        will cost O(N + L) space.
        """
        self.stack = nestedList[::-1]
        self.advanceToNextInteger()

    def next(self):
        """
        Time complexity: O(1) or O(L/N), all of this method is O(1), except for possibly the call to
        advanceToNextInteger(), giving us a time complexity the same as advanceToNextInteger().
        """
        res = self.stack.pop().getInteger()
        self.advanceToNextInteger()
        return res

    def hasNext(self):
        """
        Time complexity: O(1)
        """
        return self.stack

    def advanceToNextInteger(self):
        """
        Time complexity: O(1) or O(L/N), if the top of the stack is an integer, then this function does nothing, taking
        O(1) time. Otherwise, it needs to process the stack until an integer is on top. The best way of analyzing the
        time complexity is to look at the total cost across all calls to advanceToNextInteger() and then divide by the
        number of calls made. Once the iterator is exhausted, advanceToNextInteger() must have seen every integer at
        least once, costing O(N) time. Additionally, it has seen every list (except the first) on the stack at least
        once also, so this costs O(L) time. Adding these together, we get O(N + L) time.
        The amortized time of a single advanceToNextInteger() is the total cost, O(N + L), divided by the number of
        times it's called. In order to get all integers, we need to have called it N times. This gives us an amortized
        time complexity of O((N + L) / N) = O(1 + L/N) = O(L/N).
        """
        # While the stack contains a nested list at the top...
        while self.stack and not self.stack[-1].isInteger():
            # Unpack the list at the top by putting its items onto the stack in reverse order.
            for element in reversed(self.stack.pop().getList()):
                self.stack.append(element)


# Your NestedIterator object will be instantiated and called as such:
# i, v = NestedIterator(nestedList), []
# while i.hasNext(): v.append(i.next())
