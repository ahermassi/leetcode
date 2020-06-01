""" Given an Iterator class interface with methods: next() and hasNext(), design and implement a PeekingIterator that
support the peek() operation -- it essentially peek() at the element that will be returned by the next call to next().
"""

# Excellent read: https://leetcode.com/articles/peeking-iterator/


class PeekingIteratorV1:
    """ Store the next value outside the iterator. When next() is called, return the stored value and populate with
        next value from the iterator.
    Time complexity: O(1), all methods. The actual operations from .next() are impossible for us to analyze as they
    depend on the given Iterator. By design, they are none of our concern. Our addition to the time is only O(1) though.
    Space complexity: O(1), all methods. Like with time complexity, the Iterator itself is probably using memory in its
    own implementation. But again, this is not our concern. Our implementation only uses a few variables, so it is O(1).
    """
    def __init__(self, iterator):
        """ Initialize your data structure here. """
        self.iterator = iterator
        self.nextElement = self.iterator.next()

    def peek(self):
        """ Returns the next element in the iteration without advancing the iterator. """
        return self.nextElement

    def next(self):
        """ Firstly, we need to check if we have a value already stored in the 'nextElement' variable. If we do, we
            need to return it and also advance the iterator and store the next value again. """
        val = self.nextElement
        self.nextElement = self.iterator.next() if self.iterator.hasNext() else None
        return val

    def hasNext(self):
        """ If there's a value waiting in 'nextElement', we should return true. """
        return self.nextElement is not None


# Follow up: How would you extend your design to be generic and work with all types, not just integer?


class PeekingIteratorV2:
    """ For the most part, our code would work fine if we replaced integers with another data type (e.g. strings).
        There is one case where this does not work, and that's if the underlying Iterator might return null/None from
        .next() as an actual value. If our code is using None to represent an exhausted Iterator, then the conditionals
        in PeekingIterator will not behave as expected on these values coming out of the underlying Iterator.
        We can solve it by using a boolean variable 'noNextElement' to state whether or not there's a next value or the
        Iterator is exhausted, instead of trying to infer this information based on null status of value variables.
    """
    def __init__(self, iterator):
        self.iterator = iterator
        self.nextElement = self.iterator.next()
        self.noNextElement = False

    def peek(self):
        return self.nextElement

    def next(self):
        val = self.nextElement
        if self.iterator.hasNext():
            self.nextElement = self.iterator.next()
        else:
            self.noNextElement = True
        return val

    def hasNext(self):
        return not self.noNextElement
