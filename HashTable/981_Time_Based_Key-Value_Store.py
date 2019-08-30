""" Create a timebased key-value store class TimeMap. See description on leetcode. """

from collections import defaultdict
import unittest2 as unittest


class TimeMapV1(object):

    def __init__(self):
        """
        Initialize your data structure here.
        """
        self.data = defaultdict(list)

    def set(self, key, value, timestamp):
        """
        :type key: str
        :type value: str
        :type timestamp: int
        :rtype: None
        """
        self.data[key].append((value, timestamp))

    def get(self, key, timestamp):
        """
        Use the fact that the timestamps for all TimeMap.set operations are strictly increasing
        :type key: str
        :type timestamp: int
        :rtype: str
        """
        ans = ''
        if timestamp > self.data[key][-1][1]:  # If the timestamp we're looking for is greater than the last time
            # inserted, then return the value associated with that timestamp since the timestamps are saved in
            # increased order.
            return self.data[key][-1][0]
        for value in self.data[key]:
            if value[1] <= timestamp:
                ans = value[0]
            else:  # Break when we reach a timestamp greater than the one we're looking for since all the following
                # are also greater (timestamps are in increasing order)
                break
        return ans


class Test(unittest.TestCase):
    time_map1 = TimeMapV1()
    time_map1.set('foo', 'bar', 1)
    foo1 = time_map1.get('foo', 1)
    foo2 = time_map1.get('foo', 3)
    time_map1.set('foo', 'bar2', 4)
    foo3 = time_map1.get('foo', 4)
    foo4 = time_map1.get('foo', 5)

    def test_time_map(self):
        self.assertEqual('bar', self.foo1)
        self.assertEqual('bar', self.foo2)
        self.assertEqual('bar2', self.foo3)
        self.assertEqual('bar2', self.foo4)


if __name__ == '__main__':
    unittest.main()