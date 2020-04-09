""" Design a hit counter which counts the number of hits received in the past 5 minutes.
Each function accepts a timestamp parameter (in seconds granularity) and you may assume that calls are being made to
the system in chronological order (ie, the timestamp is monotonically increasing). You may assume that the earliest
timestamp starts at 1.
It is possible that several hits arrive roughly at the same time. """


class HitCounterV1:
    """ We store all the incoming timestamps in an array. When get_hits(timestamp) is called, and since the timestamps
        array is sorted, we look for the first entry x such that timestamp - x < 300. Therefore, the size of the
        sub-array starting from and including x is the result.
    Time complexity: O(1) hit(), O(N) get_hits() where N is the number of all timestamps
    Space complexity: O(N)
    """

    def __init__(self):
        """
        Initialize your data structure here.
        """
        self.times = []

    def hit(self, timestamp: int) -> None:
        """
        Record a hit.
        @param timestamp - The current timestamp (in seconds granularity).
        """
        self.times.append(timestamp)

    def get_hits(self, timestamp: int) -> int:
        """
        Return the number of hits in the past 5 minutes.
        @param timestamp - The current timestamp (in seconds granularity).
        """
        times, n = self.times, len(self.times)
        if not times:
            return 0
        if timestamp - times[0] < 300:
            return n
        if timestamp - times[-1] >= 300:
            return 0
        i = 0
        while i < n and timestamp - times[i] >= 300:
            i += 1
        return n - i

# Follow up: What if the number of hits per second could be very large? Does your design scale?


class HitCounterV2:
    """ If huge amount of hits happen at the same timestamp, the previous solution will take too much memory since each
        element in the timestamps array is a single hit.
        The idea of this solution is using buckets: 1 bucket for every second because we only need to keep the recent
        hits info for LAST 300 SECONDS. Each index i of the 'times' array has a pair (time, hits), where 'times' is the
        timestamp when hit(time) was called, and 'hits' is the number of times hit(time) was called. 'times' array is
        wrapped around using modulo operation.
        When hit(timestamp) is called, we get the index where the hit should be stored in 'times' array and fetch the
        timestamp 'time' and number of hits 'hits' associated to that index. If time != timestamp, it means 'time' was
        saved 300s or 600s... ago and the entry needs to be reset to (timestamp, 1).
    Time complexity: O(1) for both functions
    Space complexity: O(300) = O(1)
    """

    def __init__(self):
        """
        Initialize your data structure here.
        """
        self.times = [(0, 0)] * 300

    def hit(self, timestamp: int) -> None:
        """
        Record a hit.
        @param timestamp - The current timestamp (in seconds granularity).
        """
        times = self.times
        index = timestamp % 300  # 'times' stores hits information for last 300 seconds only making the slots reusable
        time, hits = times[index]
        if time != timestamp:  # The time saved in this slot was hit more than 300 seconds ago, so recycle the slot
            times[index] = (timestamp, 1)
        else:
            times[index] = (time, hits + 1)

    def get_hits(self, timestamp: int) -> int:
        """
        Return the number of hits in the past 5 minutes.
        @param timestamp - The current timestamp (in seconds granularity).
        """
        res = 0
        for time, hits in self.times:
            if timestamp - time < 300:
                res += hits
        return res
