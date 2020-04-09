""" Design a hit counter which counts the number of hits received in the past 5 minutes.
Each function accepts a timestamp parameter (in seconds granularity) and you may assume that calls are being made to
the system in chronological order (ie, the timestamp is monotonically increasing). You may assume that the earliest
timestamp starts at 1.
It is possible that several hits arrive roughly at the same time. """


class HitCounter:
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
