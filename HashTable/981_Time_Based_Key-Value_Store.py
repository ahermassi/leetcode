""" Create a time-based key-value store class TimeMap. See description on Leetcode. """

import bisect
from collections import defaultdict
import unittest2 as unittest


class TimeMapV1(object):
    """ We can think of making some buckets for each given key, then in each bucket, we can store
         (timestamp, value) pairs in a list.

         In the problem statement, it is mentioned that "all the timestamps of set are strictly increasing", thus even
         if we use an array to store the timestamps, they will be pushed in sorted order.
    """

    def __init__(self):
        self.values = defaultdict(list)

    def set(self, key, value, timestamp):
        self.values[key].append((timestamp, value))

    def get(self, key, timestamp):
        """
        Time complexity: O(N)
        Space complexity: O(1)
        """
        values = self.values[key]
        if timestamp < values[0][0]:
            # If the timestamp we're looking for is smaller than the first stored timestamp, then it's not possible
            # to find a valid value.
            return ''
        if timestamp >= values[-1][0]:
            # If the timestamp we're looking for is greater than or equal to the last stored timestamp, then return the
            # value associated with that timestamp since the timestamps are sorted in increasing order.
            return values[-1][1]
        res = ''
        # Linearly search for the largest timestamp less than or equal to 'timestamp'
        for ts, value in values:
            if ts <= timestamp:
                res = ts
            else:
                # Break when we find a timestamp greater than the one we're searching for since all the following
                # timestamps are also greater (sorted in increasing order)
                break
        return res

# Video explanation: https://www.youtube.com/watch?v=fu2cD_6E8Hw


class TimeMapV2(object):
    """ We can apply binary search on the ordered list of timestamps during TimeMap.set() operations.
        In this implementation, we separate the values from the timestamps to simplify the binary search.
    """

    def __init__(self):
        self.store = defaultdict(list)  # Each key will have a list of values associated to it
        self.timestamps = defaultdict(list)  # Each key will have a (sorted) list of timestamps associated to it

    def set(self, key: str, value: str, timestamp: int) -> None:
        self.store[key].append(value)
        self.timestamps[key].append(timestamp)

    def get(self, key: str, timestamp: int) -> str:
        """ Use binary search to find the insertion index of the timestamp.
        Time complexity: O(logN)
        Space complexity: O(1)
        """
        timestamps = self.timestamps[key]
        if not timestamps or timestamp < timestamps[0]:
            return ''
        # Review 35- Search Insert Position
        left, right = 0, len(timestamps) - 1
        while left <= right:
            mid = (left + right) // 2
            if timestamps[mid] <= timestamp:
                left = mid + 1
            else:
                right = mid - 1
        return self.store[key][left - 1]
        # Could also be re-written as:
        # res = None
        # while left <= right:
        #     mid = (left + right) // 2
        #     if timestamps[mid] <= timestamp:
        #         res = self.store[key][mid]
        #         left = mid + 1
        #     else:
        #         right = mid - 1
        # return res


class TimeMapV3(object):
    """ This solution uses bisect() to search in the ordered list of timestamps. """

    def __init__(self):
        self.store = defaultdict(list)

    def set(self, key, value, timestamp):
        self.store[key].append((timestamp, value))

    def get(self, key, timestamp):
        """ Use bisect() to find the insertion index of the timestamps.
        Time complexity: O(logN)
        Space complexity: O(1)
        """
        if key not in self.store or timestamp < self.store[0][0]:
            return ''
        values = self.store[key]
        if timestamp >= values[-1][0]:  # This optimization results in 30 - 60ms less in execution time
            return self.store[key][-1][1]
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