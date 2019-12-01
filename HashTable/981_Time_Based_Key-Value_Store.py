""" Create a timebased key-value store class TimeMap. See description on leetcode. """

import bisect
from collections import defaultdict
import unittest2 as unittest


class TimeMapV1(object):

    def __init__(self):
        """ Initialize your data structure here. """
        self.data = defaultdict(list)

    def set(self, key, value, timestamp):
        self.data[key].append((value, timestamp))

    def get(self, key, timestamp):
        """ Use the fact that the timestamps for all TimeMap.set operations are strictly increasing.
        Time complexity: O(N)
        Space complexity: O(1)
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


class TimeMapV2(object):
    """ This solution uses bisect() to search in the ordered list of timestamps. """

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
        self.data[key].append((timestamp, value))  # Note how timestamp comes before value as it is the basis of search

    def get(self, key, timestamp):
        """
        :type key: str
        :type timestamp: int
        :rtype: str
        """
        if key not in self.data:
            return ''
        if timestamp > self.data[key][-1][0]:  # This optimization results in 30 - 60ms less in execution time
            return self.data[key][-1][1]
        values = self.data[key]
        idx = bisect.bisect(values, (timestamp, chr(127)))  # chr(127) is the char #127 in ASCII table. It is larger
        # than all the commonly used characters. It is helpful because, in tuple comparison, python will compare
        # element by element, and in case of equal timestamps it returns the index after the last found tuple.
        return values[idx - 1][1] if idx else ''  # If idx is 0, then all timestamps are greater than 'timestamp'


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