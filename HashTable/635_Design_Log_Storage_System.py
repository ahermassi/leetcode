""" See description on Leetcode """


class LogSystemV1(object):
    """ Because the number of operations is very small, we do not need a complicated structure to store the logs: a
        simple list will do.
        Let's focus on the retrieve function. For each granularity, we should consider all timestamps to be truncated
        to that granularity. For example, if the granularity is 'Day', we should truncate the timestamp
        '2017:07:02:08:30:12' to be '2017:07:02'. Now for each log, if the truncated timetuple is between 'start' and
        'end', then we should add the id of that log to our answer.
    Time complexity: O(1) for put(), O(N) for retrieve()
    Space complexity: O(N)
    """

    def __init__(self):
        self.granularity = {'Year': 4, 'Month': 7, 'Day': 10, 'Hour': 13, 'Minute': 16, 'Second': 19}
        self.logs = []

    def put(self, id, timestamp):
        self.logs.append((id, timestamp))

    def retrieve(self, s, e, gra):
        index = self.granularity[gra]
        s, e, res = s[:index], e[:index], []
        for id, timestamp in self.logs:
            if s <= timestamp[:index] <= e:
                res.append(id)
        return res


class LogSystemV2(object):
    """ Using the same idea of truncating/pruning the timestamp as per granularity, but converting the timestamp to a
        tuple by splitting at ':' before storing/comparing (For Year, prune the timestamp tuple from index 1 and
        onwards, for Month prune from index 2 and onwards, etc).
    Time complexity: O(1) for put(), O(N) for retrieve()
    """

    def __init__(self):
        self.granularity = {'Year': 1, 'Month': 2, 'Day': 3, 'Hour': 4, 'Minute': 5, 'Second': 6}
        self.logs = {}

    def put(self, id: int, timestamp: str):
        self.logs[id] = tuple(timestamp.split(':'))

    def retrieve(self, s: str, e: str, gra: str):
        index, res = self.granularity[gra], []
        start, end = tuple(s.split(':')[:index]), tuple(e.split(':')[:index])
        for key, value in self.logs.items():
            if start <= value[:index] <= end:
                res.append(key)
        return res
