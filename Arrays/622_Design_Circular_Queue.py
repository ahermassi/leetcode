""" Design your implementation of the circular queue. The circular queue is a linear data structure in which the
operations are performed based on FIFO (First In First Out) principle and the last position is connected back to the
first position to make a circle. It is also called "Ring Buffer". """


class MyCircularQueueV1:
    """ Array implementation.
        To build a circular queue, we could form a virtual ring structure using an array, via the manipulation of index.
        Here we give a list of attributes and the thoughts behind each attribute.
            - queue: a fixed size array to hold the elements for the circular queue
            - capacity: the capacity of the circular queue, i.e. the maximum number of elements that can be held in
              the queue
            - size: the current length of the circular queue, i.e. the number of elements in the circular queue
            - front: an integer which indicates the current head element in the circular queue
            - tail: an integer which indicates the current tail element in the circular queue
        On every enqueueing operation, we increment the tail pointer since the queue will get bigger, and store the
        value.
        On every dequeuing operation, we increment the front pointer since the queue will get smaller conceptually,
        i.e. we narrow the gap between front and tail.
        Given a fixed size array, any of the elements could be considered as a head in a queue. As long as we know the
        size of the queue, we then can derive the following formula:

            (tail - front) % capacity = (size − 1) % capacity

        Both pointers will keep rotating in the queue.
        Example: capacity = 5, size = 3, X: occupied, -: empty

        0   1   2   3   4           0   1   2   3   4               0   1   2   3   4
        X   X   X   -   -           -   X   X   X   -               X   -   -   X   X
      front    tail                   front    tail                tail        front
      (2-0) % 5 = (3-1) % 5         (3-1) % 5 = (3-1) % 5          (0-3) % 5 = 2 = (3-1) % 5


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
        self.tail = -1  # The first legal operation will always be enQueue() after which front = rear = 0.
        # If a deQueue() is performed right after that, rear = 0, front = 1

    def enQueue(self, value: int) -> bool:
        """
        Insert an element into the circular queue. Return true if the operation is successful.
        """
        if self.isFull():
            return False
        self.tail = (self.tail + 1) % self.capacity
        self.queue[self.tail] = value
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
        return -1 if self.isEmpty() else self.queue[self.tail]

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


class ListNode:
    def __init__(self, val):
        self.val = val
        self.next = None


class MyCircularQueueV2:
    """ Linked list implementation.
        Different than a fixed size Array, a linked list could be more memory efficient, since it does not pre-allocate
        memory for unused capacity.
    Time complexity: O(1), all of the methods in our circular data structure is of constant time complexity
    Space complexity: O(N)
    """

    def __init__(self, k: int):
        """
        Initialize your data structure here. Set the size of the queue to be k.
        """
        self.head = None
        self.tail = None
        self.size = 0
        self.capacity = k

    def enQueue(self, value: int) -> bool:
        """
        Insert an element into the circular queue. Return true if the operation is successful.
        """
        if self.isFull():
            return False
        if self.isEmpty():
            node = ListNode(value)
            self.head = self.tail = node
        else:
            self.tail.next = ListNode(value)
            self.tail = self.tail.next
        self.size += 1
        return True

    def deQueue(self) -> bool:
        """
        Delete an element from the circular queue. Return true if the operation is successful.
        """
        if self.isEmpty():
            return False
        self.head = self.head.next
        self.size -= 1
        return True

    def Front(self) -> int:
        """
        Get the front item from the queue.
        """
        return -1 if self.isEmpty() else self.head.val

    def Rear(self) -> int:
        """
        Get the last item from the queue.
        """
        return -1 if self.isEmpty() else self.tail.val

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
