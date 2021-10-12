""" A Range Module is a module that tracks ranges of numbers. Design a data structure to track the ranges represented
as half-open intervals and query about them.

A half-open interval [left, right) denotes all the real numbers x where left <= x < right.

Implement the RangeModule class:

RangeModule() Initializes the object of the data structure.
void addRange(int left, int right) Adds the half-open interval [left, right), tracking every real number in that
interval. Adding an interval that partially overlaps with currently tracked numbers should add any numbers in the
interval [left, right) that are not already tracked.
boolean queryRange(int left, int right) Returns true if every real number in the interval [left, right) is currently
being tracked, and false otherwise.
void removeRange(int left, int right) Stops tracking every real number currently being tracked in the half-open
interval [left, right). """

from bisect import bisect_left, bisect_right


class RangeModule(object):
    """ Typically, problems like these require us to use a data structure like TreeMap (from Java), but for those of us
        using python there is no such builtin data structure.

        The only thing we should understand clearly before understanding this solution is how bisect_left and
        bisect_right work in python. bisect_left gives the position of the first index where the element can be
        inserted, and bisect_right gives the position of the last index where the element can be inserted.
        Note that if the item we are trying to search for is not present in the array, both bisect_left and
        bisect_right will return the same result.

        Example : bisect_left([1,2,3], 2) = 1 ; bisect_right([1,2,3], 2) = 2
                  bisect_left([1,2,4], 3) = 2 ; bisect_right([1,2,4], 3) = 2

        Now coming to the problem at hand, we internally represent the covered ranges by a single array 'ranges'.
        Think of this as a number line in which the EVEN indices represent the beginning of a range and ODD indices
        represent the end of the range. By definition of the range, we should maintain an even number of elements in
        the array 'ranges'.

        For e.g : ranges = [10, 15, 20, 25] means the covered ranges are [10, 15) and [20, 25)

        Add a range [left, right):
        If we want to add a range, we look at the bisect_left of left and bisect_right of right in 'ranges'. We need
        to do this because the opening of the range (i.e left) has to precede any other range which is closing at the
        same point. Similarly for the closing of the range i.e right, we have to keep in mind any other ranges opening
        at that point.

        In the example above of ranges = [10, 15, 20, 25], let's say we want to add range [14, 22), then 'ranges'
        should look as follows: ranges = [10, 25].

        For this to happen, we rely on i = bisect_left(ranges, left) and j = bisect_right(ranges, right).

        What does it mean if i is odd ? That means that preceding element is at an even index and the opening of the
        range we're trying to add is part of some other range. Similarly, if j is odd, that also means it is part of
        some other range and we need not create a new entry for it.

        What does it mean if i is even ? This means that this point does not interfere with any existing range and is
        currently outside the range of start and end indices being tracked, so we have to create a new entry for it.
        Similar thing holds true for j, it would mean that we would have overwrite an exiting range.

        We then use python array slicing to overwrite the tracking array 'ranges' with the left and right values placed
        in the correct index.

        Odd positions lie between ranges. The way to think about this is that ranges are pairs. If we need to insert
        in an odd place, it always lies within an EXISTING range. Think about it as if it lies within a range, it is
        consumed/superseded by that range, hence we do not need to add that.

        Let's say we have ranges = [1,3,9,11], which denotes intervals [1,3), [9,11). Say we want to add [4,6) to the
        ranges; bisect_left([1,3,9,11], 4) will return 2, which is an even index. This means 4 does not overlap with
        any of the intervals [1,3) and [9,11). Therefore, we would need to add the interval to the final result.
        On the other hand, if we were to add the interval [3, 6), bisect_left([1,3,9,11), 3) will return 1, which means
         3 is overlapping with an existing interval and we do not have to add it to the final result.

        Remove a range [left, right):
        The intuition behind removeRange(left, right) is similar to addRange(left, right), but the only difference is
        that we have to perform the operation when either i or j is odd instead of even. This is because while
        removing, if i is even, this means that it does not interfere with any existing range and we do not need to
        perform any action (except possibly collapsing the ranges). Similar logic holds true for j as well. However,
        if the index is odd, it means that it is currently inside the range of start and end indexes being tracked.

        Query a range [left, right):
        While querying for a range, we similarly get i and j values and we check for two conditions:
        (i) Both i and j are same. i.e there is no range boundary in between left and right. if there is a range
        boundary, that means at least some part of the range is not covered.
        (ii) They should be odd. This means that a range has been opened by preceding an even index and yet to be
        closed by the element at the i (or j)'th position.
        If both (i) and (ii) are met, then we can say that the range is completely covered.
        We use i = bisect_right(ranges, left) and j = bisect_left(ranges, right) because we want to be as conservative
        as possible.
        For e.g if ranges = [10,15], and we are querying for [15, 20), then bisect_left(ranges, left) would give us 1,
        which means that there is some part of the interval covered, but 15 is not covered by the range.

        Example: ranges = [1, 3, 9, 11]
            addRange():
            [4, 6)
            bisect_left(4) = 2
            bisect_right(6) = 2
            subrange = [4, 6]
            --> ranges[2:2] = [4, 6]
            --> ranges = [1, 3, 4, 6, 9, 11]

            [2, 5)
            bisect_left(2) = 1
            bisect_right(5) = 2
            subrange = [5]
            --> range[1:2] = [5]
            --> ranges = [1, 5, 9, 11]

            [3, 10)
            bisect_left(3) = 1
            bisect_right(10) = 3
            subrange = []
            --> ranges[1:3] = []
            --> ranges = [1, 11]

            removeRange():
            [4, 6)
            bisect_left(4) = 2
            bisect_right(6) = 2
            subrange = []
            --> ranges[2:2] = []
            --> ranges = [1, 3, 9, 11]

            [2, 5)
            bisect_left(2) = 1
            bisect_right(5) = 2
            subrange = [2]
            --> ranges[1:2] = [2]
            --> ranges = [1, 2, 9, 11]

            [3, 10)
            bisect_left(3) = 1
            bisect_right(10) = 3
            subrange = [1, 3]
            --> ranges[1:3] = [3, 10]
            --> ranges = [1, 3, 10, 11]

    """

    def __init__(self):
        self.ranges = []

    def addRange(self, left, right):
        """
        Time complexity: O(N), where N is the number of disjoint intervals currently stored. Slice overwriting
        dominates binary search
        Space complexity: O(N)
        """
        subrange = []
        start = bisect_left(self.ranges, left)
        end = bisect_right(self.ranges, right)
        if start % 2 == 0:  # Start boundary is not already contained in an interval
            subrange.append(left)
        if end % 2 == 0:  # End boundary is not already contained in an interval
            subrange.append(right)
        self.ranges[start:end] = subrange

    def removeRange(self, left, right):
        """
        Time complexity: O(N), slice overwriting dominates binary search
        Space complexity: O(N)
        """
        subrange = []
        start = bisect_left(self.ranges, left)
        end = bisect_right(self.ranges, right)
        if start % 2 == 1:
            subrange.append(left)
        if end % 2 == 1:
            subrange.append(right)
        self.ranges[start:end] = subrange

    def queryRange(self, left, right):
        """
        Time complexity: O(logN)
        Space complexity: O(1)
        """
        start = bisect_right(self.ranges, left)
        end = bisect_left(self.ranges, right)
        return start == end and start % 2 == 1

