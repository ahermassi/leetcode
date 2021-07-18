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
    """
    def __init__(self, nestedList):
        self.stack = nestedList[::-1]
        self.advanceToNextInteger()

    def next(self):
        res = self.stack.pop().getInteger()
        self.advanceToNextInteger()
        return res

    def hasNext(self):
        return self.stack

    def advanceToNextInteger(self):
        while self.stack:
            top = self.stack[-1]
            if not top.isInteger():
                self.stack.extend([val for val in self.stack.pop().getList()[::-1]])  # Flatten


# Your NestedIterator object will be instantiated and called as such:
# i, v = NestedIterator(nestedList), []
# while i.hasNext(): v.append(i.next())
