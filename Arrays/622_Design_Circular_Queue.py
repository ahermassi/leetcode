""" Design your implementation of the circular queue. The circular queue is a linear data structure in which the
operations are performed based on FIFO (First In First Out) principle and the last position is connected back to the
first position to make a circle. It is also called "Ring Buffer". """


class MyCircularQueue:
    """ To build a circular queue, we could form a virtual ring structure with the Array, via the manipulation of index.
        Here we give a list of attributes and the thoughts behind each attribute.
            - queue: a fixed size array to hold the elements for the circular queue
            - capacity: the capacity of the circular queue, i.e. the maximum number of elements that can be hold in
              the queue
            - size: the current length of the circular queue, i.e. the number of elements in the circular queue
            - front: an integer which indicates the current head element in the circular queue
            - rear: an integer which indicates the current tail element in the circular queue
    Time complexity: O(1), all of the methods in our circular data structure is of constant time complexity
    Space complexity: O(N)
    """

    def __init__(self, k: int):
        """
        Initialize your data structure here. Set the size of the queue to be k.
        """
        self.queue = [None] * k
        self.capacity = k
        self.size = 0
        self.front = 0
        self.rear = -1  # The first legal operation will always be enQueue() after which front = rear = 0.
        # If a deQueue() is performed right after that, rear = 0, front = 1

    def enQueue(self, value: int) -> bool:
        """
        Insert an element into the circular queue. Return true if the operation is successful.
        """
        if self.isFull():
            return False
        self.rear = (self.rear + 1) % self.capacity
        self.queue[self.rear] = value
        self.size += 1
        return True

    def deQueue(self) -> bool:
        """
        Delete an element from the circular queue. Return true if the operation is successful.
        """
        if self.size == 0:
            return False
        self.front = (self.front + 1) % self.capacity
        self.size -= 1
        return True

    def Front(self) -> int:
        """
        Get the front item from the queue.
        """
        return -1 if self.isEmpty() else self.queue[self.front]

    def Rear(self) -> int:
        """
        Get the last item from the queue.
        """
        return -1 if self.isEmpty() else self.queue[self.rear]

    def isEmpty(self) -> bool:
        """
        Checks whether the circular queue is empty or not.
        """
        return self.size == 0

    def isFull(self) -> bool:
        """
        Checks whether the circular queue is full or not.
        """
        return self.size == self.capacity
