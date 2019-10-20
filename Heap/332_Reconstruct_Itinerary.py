""" Read description on Leetcode """

from collections import defaultdict
from heapq import heappush, heappop
import unittest2 as unittest


def find_itinerary_v1(tickets):
    """ All the airports are vertices and tickets are directed edges. Then all these tickets form a directed graph.
        Since the problem asks for lexical order smallest solution, we can put the neighbors in a min-heap. This way we
        always visit the smallest possible neighbor first in our trip.
    Time complexity: O(N logN), where N is the number of tickets
    Space complexity: O(N)
    """
    d = defaultdict(list)
    for origin, dest in tickets:
        heappush(d[origin], dest)
    stack, res = ['JFK'], []
    while stack:
        arrivals = d[stack[-1]]
        if arrivals:
            stack.append(heappop(arrivals))
        else:
            res.append(stack.pop())
    return res[::-1]


class Test(unittest.TestCase):
    data = [([['MUC', 'LHR'], ['JFK', 'MUC'], ['SFO', 'SJC'], ['LHR', 'SFO']], ['JFK', 'MUC', 'LHR', 'SFO', 'SJC']),
            ([['JFK', 'SFO'], ['JFK', 'ATL'], ['SFO', 'ATL'], ['ATL', 'JFK'], ['ATL', 'SFO']],
             ['JFK', 'ATL', 'JFK', 'SFO', 'ATL',
              'SFO'])]

    def test_find_itinerary(self):
        for test_tickets, result in self.data:
            self.assertEqual(result, find_itinerary_v1(test_tickets))


if __name__ == '__main__':
    unittest.main()
