""" Design your implementation of the circular double-ended queue (deque).

Implement the MyCircularDeque class:

MyCircularDeque(int k) Initializes the deque with a maximum size of k.
boolean insertFront() Adds an item at the front of Deque. Returns true if the operation is successful, or false otherwise.
boolean insertLast() Adds an item at the rear of Deque. Returns true if the operation is successful, or false otherwise.
boolean deleteFront() Deletes an item from the front of Deque. Returns true if the operation is successful, or false otherwise.
boolean deleteLast() Deletes an item from the rear of Deque. Returns true if the operation is successful, or false otherwise.
int getFront() Returns the front item from the Deque. Returns -1 if the deque is empty.
int getRear() Returns the last item from Deque. Returns -1 if the deque is empty.
boolean isEmpty() Returns true if the deque is empty, or false otherwise.
boolean isFull() Returns true if the deque is full, or false otherwise. """


class MyCircularDequeV1(object):
    """ Array implementation. Similar to 622- Design Circular Queue.
        To build a circular deque, we could form a virtual ring structure with the array via the manipulation of index.
        Here we give a list of attributes and the thoughts behind each attribute.
            - queue: a fixed size array to hold the elements for the circular deque
            - capacity: the capacity of the circular deque, i.e. the maximum number of elements that can be hold in
              the queue
            - size: the current length of the circular deque, i.e. the number of elements in the circular deque
            - front: an integer which indicates the current head element in the circular deque
            - rear: an integer which indicates the current tail element in the circular deque
        We use the modulo operation to create our own "warp-around" effect. For example, if self.capacity is 10, and
        self.front is 0, which means self.queue[0] is occupied and is the front, then an insertFront operation will put
        a new element on self.queue[9], so the new self.front will be (self.front - 1) % self.capacity, which is 9.
        Same logic applies ot insertLast (advance 'rear'), deleteFront (advance 'front'), and deleteLast
        (retreat 'rear').
        The best way to conceive of how an array deque works is by visualizing it as a circle created by connecting the
        ends of the array. In a non-empty array deque, the content is specified by elements in positions 'front' to
        'rear' going clockwise.
    """

    def __init__(self, k):
        """ Initialize your data structure here. Set the size of the deque to be k. """
        self.queue = [0] * k
        self.front = 0
        self.rear = k - 1
        self.capacity = k
        self.size = 0

    def insertFront(self, value):
        """ Adds an item at the front of Deque. Return true if the operation is successful. """
        if self.isFull():
            return False
        self.front = (self.front - 1) % self.capacity
        self.queue[self.front] = value
        self.size += 1
        return True

    def insertLast(self, value):
        """ Adds an item at the rear of Deque. Return true if the operation is successful. """
        if self.isFull():
            return False
        self.rear = (self.rear + 1) % self.capacity
        self.queue[self.rear] = value
        self.size += 1
        return True

    def deleteFront(self):
        """ Deletes an item from the front of Deque. Return true if the operation is successful. """
        if self.isEmpty():
            return False
        self.queue[self.front] = 0
        self.front = (self.front + 1) % self.capacity
        self.size -= 1
        return True

    def deleteLast(self):
        """ Deletes an item from the rear of Deque. Return true if the operation is successful. """
        if self.isEmpty():
            return False
        self.queue[self.rear] = 0
        self.rear = (self.rear - 1) % self.capacity
        self.size -= 1
        return True

    def getFront(self):
        """ Get the front item from the deque. """
        if self.isEmpty():
            return -1
        return self.queue[self.front]

    def getRear(self):
        """ Get the last item from the deque. """
        if self.isEmpty():
            return -1
        return self.queue[self.rear]

    def isEmpty(self):
        """ Checks whether the circular deque is empty or not. """
        return self.size == 0

    def isFull(self):
        """ Checks whether the circular deque is full or not. """
        return self.size == self.capacity
