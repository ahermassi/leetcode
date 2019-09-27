""" See description on Leetcode """


class LogSystem(object):
    """ Because the number of operations is very small, we do not need a complicated structure to store the logs: a
        simple list will do.
        Let's focus on the retrieve function. For each granularity, we should consider all timestamps to be truncated
        to that granularity. For example, if the granularity is 'Day', we should truncate the timestamp
        '2017:07:02:08:30:12' to be '2017:07:02'. Now for each log, if the truncated timetuple cur is between start and
        end, then we should add the id of that log into our answer.
    Time complexity: O(1) for put(), O(N) for retrieve()
    """

    def __init__(self):
        self.d = {'Year': 4, 'Month': 7, 'Day': 10, 'Hour': 13, 'Minute': 16, 'Second': 19}
        self.logs = []

    def put(self, id, timestamp):
        """
        :type id: int
        :type timestamp: str
        :rtype: None
        """
        self.logs.append((id, timestamp))

    def retrieve(self, s, e, gra):
        """
        :type s: str
        :type e: str
        :type gra: str
        :rtype: List[int]
        """
        idx = self.d[gra]
        s, e, res = s[:idx], e[:idx], []
        for id, timestamp in self.logs:
            if s <= timestamp[:idx] <= e:
                res.append(id)
        return res
