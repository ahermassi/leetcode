""" Design a logger system that receive stream of messages along with its timestamps, each message should be printed
if and only if it is not printed in the last 10 seconds.
Given a message and a timestamp (in seconds granularity), return true if the message should be printed in the given
timestamp, otherwise returns false. """

from collections import deque
import unittest2 as unittest


class LoggerV1(object):
    """ It is imperative to clarify the conditions of the problem, since it was not explicit in the problem
        description. Here is one important note:
            It is possible that several messages arrive roughly at the same time.
        We could interpret that the input messages are in chronological order, i.e. the timestamps of the messages are
        monotonically increasing, though not strictly. This constraint is critical, since it would simplify the task.
        The idea is that we keep a hashtable with the message as key, and its timestamp as the value. The hashtable
        keeps all the unique messages along with the latest timestamp that the message was printed.
        At the arrival of a new message, the message is eligible to be printed with either of the two conditions as
        follows:
            1- We have never seen the message before
            2- We have seen the message before, and it was printed more than 10 seconds ago.
        In both of the above cases, we would then update the entry that is associated with the message in the hashtable,
        with the latest timestamp.
        Possible optimization (follow-up):
        For a Logger, probably the solution is not that practical since the hash table soon will blow up.
        We can have another thread running cron job to evict timeout entries from the hash map who existed for more
        than 10 seconds.
    Time complexity: O(1), the lookup and update of the hashtable takes a constant time
    Space complexity: O(N), where N is the size of all incoming messages. Over the time, the hashtable would have an
    entry for each unique message that has appeared.
    """

    def __init__(self):
        """
        Initialize your data structure here.
        """
        self.log = {}

    def should_print_message(self, timestamp, message):
        """
        Returns true if the message should be printed in the given timestamp, otherwise returns false.
        If this method returns false, the message will not be printed.
        The timestamp is in seconds granularity.
        """
        if message not in self.log or timestamp - self.log[message] >= 10:
            self.log[message] = timestamp
            return True
        return False


class LoggerV2:
    """ The previous solution needs to keep the record of the entire messages, even when the message is rare.
        Alternatively, we can keep a queue to get rid of the old messages and set of strings to keep the recent
        messages only. With each call to should_print_message(), we iterate over the queue and evict all the messages
        whose timestamps are more than 10 seconds ago. These are old messages that are no longer looked at. This way,
        before deciding if the current message should be printed at the current timestamp, we only keep record of the
        messages that arrived less than 10 seconds ago. For example, the arrival of the message with the timestamp 18
        would invalidate both the messages with the timestamp of 5 and 7 which go beyond the time window of 10 seconds.
        If the new message can still be found in the messages set, we return False because it was printed less than 10
        seconds ago. Otherwise, we add a new entry for the new (timestamp, message) pair in the queue and store the
        message in the messages' set.
        Note that we don't have to use a priority queue to store the (timestamp, message) pairs because the messages are
        given in sorted order in terms of timestamp.
        This solution keeps the hash map from blowing up.
    Time complexity: O(N), where N is the size of the queue. In the worst case, all the messages in the queue become
    obsolete. As a result, we need clean them up.
    Space complexity: O(N), we keep the incoming messages in both the queue and set
    """

    def __init__(self):
        """
        Initialize your data structure here.
        """
        self.queue = deque()
        self.messages = set()

    def should_print_message(self, timestamp: int, message: str) -> bool:
        """
        Returns true if the message should be printed in the given timestamp, otherwise returns false.
        If this method returns false, the message will not be printed.
        The timestamp is in seconds granularity.
        """
        while self.queue and timestamp - self.queue[0][0] >= 10:
            _, msg = self.queue.popleft()
            self.messages.remove(msg)
        if message not in self.messages:
            self.messages.add(message)
            self.queue.append((timestamp, message))
            return True
        return False


class Test(unittest.TestCase):
    logger = LoggerV2()
    foo1 = logger.should_print_message(1, "foo")
    bar1 = logger.should_print_message(2, "bar")
    foo2 = logger.should_print_message(3, "foo")
    bar2 = logger.should_print_message(8, "bar")
    foo3 = logger.should_print_message(10, "foo")
    foo4 = logger.should_print_message(11, "foo")

    def test_logger(self):
        self.assertTrue(self.foo1)
        self.assertTrue(self.bar1)
        self.assertFalse(self.foo2)
        self.assertFalse(self.bar2)
        self.assertFalse(self.foo3)
        self.assertTrue(self.foo4)


if __name__ == '__main__':
    unittest.main()