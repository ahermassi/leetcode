""" Median is the middle value in an ordered integer list. If the size of the list is even, there is no middle value.
So the median is the mean of the two middle value.
For example,
[2,3,4], the median is 3
[2,3], the median is (2 + 3) / 2 = 2.5
Design a data structure that supports the following two operations:
void addNum(int num) - Add a integer number from the data stream to the data structure.
double findMedian() - Return the median of all elements so far. """

from heapq import heappush, heappop


class MedianFinder:
    """ There are some valuable insights that could help us to tackle this problem. Concretely, we can infer two things:

        If we could maintain direct access to median elements at all times, then finding the median would take a constant
        amount of time.
        If we could find a reasonably fast way of adding numbers to our containers, additional penalties incurred could
        be lessened.

        But perhaps the most important insight, which is not readily observable, is the fact that we only need a
        consistent way to access the median elements. Keeping the entire input sorted is not a requirement.
        Well, if only there were a data structure which could handle our needs.

        Heaps are a natural ingredient for this dish! Adding elements to them takes logarithmic order of time. They also
        give direct access to the maximal/minimal elements in a group.

        If we could maintain two heaps in the following way:

            A max-heap to store the smaller half of the input numbers
            A min-heap to store the larger half of the input numbers

        This gives access to median values in the input: They comprise the top of the heaps!
        If the following conditions are met:

            1- Both the heaps are balanced (or nearly balanced)
            2- The max-heap contains all the smaller numbers while the min-heap contains all the larger numbers

        Then we can say that:

            1- All the numbers in the max-heap are smaller or equal to the top element of the min-heap (let's call it x)
            2- All the numbers in the min-heap are larger or equal to the top element of the max-heap (let's call it y)

        Then x and/or y are smaller than (or equal to) almost half of the elements and larger than (or equal to) the
        other half. That is the definition of median elements.

        The sizes of two heaps need to be balanced each time when a new number is inserted so that their size will not
        be different by more than 1. Therefore, each time when findMedian() is called, we check if two heaps have the
        same size. If they do, we should return the average of the two top values of heaps. Otherwise, we return the
        top of the heap which has one more element.

        This leads us to a huge point of pain in this approach: balancing the two heaps.
        The max-heap 'smaller' is allowed to store, at worst, one more element more than the min-heap 'larger'.
        This gives us the nice property that when the heaps are perfectly balanced, the median can be derived from the
        tops of both heaps. Otherwise, the top of the max-heap 'smaller' holds the legitimate median.

        When adding a new number 'num':
            - Add 'num' to max-heap 'smaller'. Now with this insertion, 'smaller'' may contain a large element which
               should belong to 'larger' heap. So we need to balance by removing the highest element from 'smaller'
               and offer it to 'larger'.
            - The min-heap 'larger' might end holding more elements than the max-heap 'smaller' after the balancing
              operation. We fix that by removing the smallest element from 'larger' and offering it to 'smaller'.
              This step ensures that we do not disturb the nice little size property we just mentioned.

        A little example will clear this up! Say we take input from the stream [41, 35, 62, 5, 97, 108]. The run-though
        of the algorithm looks like this:

        Adding number 41
        MaxHeap smaller: [41]
        MinHeap larger: []
        Median is 41
        =======================
        Adding number 35
        MaxHeap smaller: [35]
        MinHeap larger: [41]
        Median is 38
        =======================
        Adding number 62
        MaxHeap smaller: [41, 35]
        MinHeap larger: [62]
        Median is 41
        =======================
        Adding number 4
        MaxHeap smaller: [35, 4]
        MinHeap larger: [41, 62]
        Median is 38
        =======================
        Adding number 97
        MaxHeap smaller: [41, 35, 4]
        MinHeap larger: [62, 97]
        Median is 41
        =======================
        Adding number 108
        MaxHeap smaller: [41, 35, 4]
        MinHeap larger: [62, 97, 108]
        Median is 51.5

    Time complexity: O(logN) for addNum(), O(1) for findMedian()
    Space complexity: O(N)
    """

    def __init__(self):
        self.smaller = []
        self.larger = []

    def addNum(self, num: int) -> None:
        heappush(self.smaller, -num)
        # This last insertion might've disrupted the algorithm's invariant: All 'smaller' heap elements are less
        # than or equal to 'larger' heap elements. Try to balance out.
        heappush(self.larger, -heappop(self.smaller))
        if len(self.smaller) < len(self.larger):
            heappush(self.smaller, -heappop(self.larger))

    def findMedian(self) -> float:
        if len(self.smaller) == len(self.larger):
            return (-self.smaller[0] + self.larger[0]) / 2.0
        return  -self.smaller[0]


# Follow up: If all integer numbers from the stream are between 0 and 100, how would you optimize it?
# We can maintain an integer array of length 100 to store the count of each number along with a total count. Then, we
# can iterate over the array to find the middle value to get our median.
# Time complexity: addNum() is O(1), findMedian() is O(1) since array has fixed size
