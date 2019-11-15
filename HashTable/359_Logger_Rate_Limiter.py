""" Design a logger system that receive stream of messages along with its timestamps, each message should be printed
if and only if it is not printed in the last 10 seconds.
Given a message and a timestamp (in seconds granularity), return true if the message should be printed in the given
timestamp, otherwise returns false. """

from collections import deque
import unittest2 as unittest


class LoggerV1(object):
    """ Possible optimization (follow-up):
        For a Logger, probably the solution is not that practical since the hash table soon will blow up.
        We can have another thread running cron job to evict timeout entries from the hash map who existed for more
        than 10 seconds.
    """

    def __init__(self):
        """
        Initialize your data structure here.
        """
        self.log = {}

    def shouldPrintMessage(self, timestamp, message):
        """
        Returns true if the message should be printed in the given timestamp, otherwise returns false.
        If this method returns false, the message will not be printed.
        The timestamp is in seconds granularity.
        :type timestamp: int
        :type message: str
        :rtype: bool
        """
        if message not in self.log or timestamp - self.log[message] >= 10:
            self.log[message] = timestamp
            return True
        return False


class LoggerV2:
    """ The previous solution needs to keep the record of the entire messages, even when the message is rare.
        Alternatively, we can keep a queue to get rid of the old messages and set of strings to keep the recent
        messages only. With each call to shouldPrintMessage(), we iterate over the queue and evict all the messages
        whose timestamps are more than 10 seconds ago. These are old messages that are no longer looked at. This way,
        before deciding if the current message should be printed at the current timestamp, we only keep record of the
        messages that arrived less than 10 seconds ago. If the new message can still be found in the queue, we return
        False because it was printed less than 10 seconds ago. Otherwise, we add a new entry for the new timestamp/msg
        pair in the queue and store the message in the messages' set.
        Note that we don't have to use a priority queue to store the (timestamp,message) pairs because the messages are
        given in sorted order in terms of timestamp.
        This solution keeps the hash map from blowing up.
    """

    def __init__(self):
        """
        Initialize your data structure here.
        """
        self.queue = deque()
        self.messages = set()

    def shouldPrintMessage(self, timestamp: int, message: str) -> bool:
        """
        Returns true if the message should be printed in the given timestamp, otherwise returns false.
        If this method returns false, the message will not be printed.
        The timestamp is in seconds granularity.
        """
        while self.queue and timestamp - self.queue[0][0] >= 10:
            ts, msg = self.queue.popleft()
            self.messages.remove(msg)
        if message not in self.messages:
            self.messages.add(message)
            self.queue.append((timestamp, message))
            return True
        return False


class Test(unittest.TestCase):
    logger = LoggerV2()
    foo1 = logger.shouldPrintMessage(1, "foo")
    bar1 = logger.shouldPrintMessage(2, "bar")
    foo2 = logger.shouldPrintMessage(3, "foo")
    bar2 = logger.shouldPrintMessage(8, "bar")
    foo3 = logger.shouldPrintMessage(10, "foo")
    foo4 = logger.shouldPrintMessage(11, "foo")

    def test_logger(self):
        self.assertTrue(self.foo1)
        self.assertTrue(self.bar1)
        self.assertFalse(self.foo2)
        self.assertFalse(self.bar2)
        self.assertFalse(self.foo3)
        self.assertTrue(self.foo4)


if __name__ == '__main__':
    unittest.main()