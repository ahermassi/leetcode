""" Create a time-based key-value store class TimeMap. See description on Leetcode. """

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
        if timestamp < self.data[key][0][1]:  # If the timestamp we're looking for is smaller than the first timestamp
            # inserted, then it's not possible to find a valid value.
            return ''
        if timestamp >= self.data[key][-1][1]:  # If the timestamp we're looking for is greater than or equal to  the
            # last time inserted, then return the value associated with that timestamp since the timestamps are saved
            # in increased order.
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
        self.data[key].append((timestamp, value))  # Note how timestamp comes before value as it is the basis of search

    def get(self, key, timestamp):
        """ Use binary search to find the insertion index of the timestamps.
        Time complexity: O(logN)
        Space complexity: O(1)
        """
        if key not in self.data:
            return ''
        values = self.data[key]
        if timestamp < values[0][0]:
            return ''
        if timestamp >= values[-1][0]:  # This optimization results in 30 - 60ms less in execution time
            return self.data[key][-1][1]
        idx = bisect.bisect(values, (timestamp, chr(127)))  # chr(127) is the char #127 in ASCII table. It is larger
        # than all the commonly used characters. It is helpful because, in tuple comparison, Python will compare
        # element by element, and in case of equal timestamps it returns the index after the last found tuple.
        # Example: values = self.data[key] = [(1, 'a'),(1, 'b'),(2, 'c')] and we do get(key, 1).
        # bisect(values, (timestamp, chr(127))) will try to find the insertion index of timestamp = 1 in values as
        # to keep the list sorted. Since all elements of the list are tuples, we need to provide a tuple comparison
        # basis. (timestamp, chr(127)) means if timestamps are equal, compare based on the string 'value'. chr(127) is
        # larger than all the common ASCII characters, so this guarantees that, in case of timestamp equality, bisect
        # returns the index just after the last tuple, which is a requirement of the problem.
        # In this example, bisect will return index 2, so we need to return values[index-1][1].
        return values[idx - 1][1]


class TimeMapV3(object):
    """ In this implementation, we separate the values from the timestamps to simplify the binary search. """
    def __init__(self):
        """
        Initialize your data structure here.
        """
        self.timestamps = defaultdict(list)  # Each key will have a (sorted) list of timestamps associated to it
        self.values = defaultdict(list)  # Each key will have a list of values associated to it

    def set(self, key: str, value: str, timestamp: int) -> None:
        self.timestamps[key].append(timestamp)
        self.values[key].append(value)

    def get(self, key: str, timestamp: int) -> str:
        """ Use binary search to find the insertion index of the timestamps.
        Time complexity: O(logN)
        Space complexity: O(1)
        """
        timestamps = self.timestamps[key]
        values = self.values[key]
        if timestamp < timestamps[0]:
            return ''
        if timestamp >= timestamps[-1]:
            return values[-1]
        index = bisect.bisect_right(timestamps, timestamp) - 1
        return values[index]


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