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
    """ If we could maintain two heaps in the following way:
            A max-heap to store the smaller half of the input numbers
            A min-heap to store the larger half of the input numbers
        This gives access to median values in the input: they comprise the top of the heaps!
        If the following conditions are met:
            1- Both the heaps are balanced (or nearly balanced)
            2- The max-heap contains all the smaller numbers while the min-heap contains all the larger numbers
        Then we can say that:
            1- All the numbers in the max-heap are smaller or equal to the top element of the min-heap (let's call it x)
            2- All the numbers in the min-heap are larger or equal to the top element of the max-heap (let's call it y)
        Then x and/or y are smaller than (or equal to) almost half of the elements and larger than (or equal to) the
        other half. That is the definition of median elements.
        The sizes of two heaps need to be balanced each time when a new number is inserted so that their size will not
        be different by more than 1. Therefore each time when findMedian() is called, we check if two heaps have the
        same size. If they do, we should return the average of the two top values of heaps. Otherwise, we return the
        top of the heap which has one more element.
        This leads us to a huge point of pain in this approach: balancing the two heaps.
        The max-heap 'smaller' is allowed to store, at worst, one more element more than the min-heap 'larger'.
        This gives us the nice property that when the heaps are perfectly balanced, the median can be derived from the
        tops of both heaps. Otherwise, the top of the max-heap 'smaller' holds the legitimate median.
        When adding a new number 'num':
            - Add 'num' to max-heap 'smaller'. Since 'smaller' received a new element, we must do a balancing step for
              'larger'. So remove the largest element from 'smaller' and offer it to 'larger'.
            - The min-heap 'larger' might end holding more elements than the max-heap 'smaller' after the balancing
              operation. We fix that by removing the smallest element from 'larger' and offering it to 'smaller'.
              This step ensures that we do not disturb the nice little size property we just mentioned.
        A little example will clear this up! Say we take input from the stream [41, 35, 62, 5, 97, 108]. The run-though
        of the algorithm looks like this:
        Adding number 41
        MaxHeap lo: [41]
        MinHeap hi: []
        Median is 41
        =======================
        Adding number 35
        MaxHeap lo: [35]
        MinHeap hi: [41]
        Median is 38
        =======================
        Adding number 62
        MaxHeap lo: [41, 35]
        MinHeap hi: [62]
        Median is 41
        =======================
        Adding number 4
        MaxHeap lo: [35, 4]
        MinHeap hi: [41, 62]
        Median is 38
        =======================
        Adding number 97
        MaxHeap lo: [41, 35, 4]
        MinHeap hi: [62, 97]
        Median is 41
        =======================
        Adding number 108
        MaxHeap lo: [41, 35, 4]
        MinHeap hi: [62, 97, 108]
        Median is 51.5
    Time complexity: O(logN) for addNum(), O(1) for findMedian()
    Space complexity: O(N)
    """

    def __init__(self):
        self.small = []
        self.large = []

    def addNum(self, num: int) -> None:
        heappush(self.small, -num)
        heappush(self.large, -heappop(self.small))
        if len(self.small) < len(self.large):
            heappush(self.small, -heappop(self.large))

    def findMedian(self) -> float:
        n, m = len(self.small), len(self.large)
        return (-self.small[0] + self.large[0]) / 2.0 if n == m else -self.small[0]
