""" In a town, there are N people labelled from 1 to N.  There is a rumor that one of these people is secretly the
town judge.
If the town judge exists, then:
The town judge trusts nobody.
Everybody (except for the town judge) trusts the town judge.
There is exactly one person that satisfies properties 1 and 2.
You are given trust, an array of pairs trust[i] = [a, b] representing that the person labelled a trusts the person
labelled b.
If the town judge exists and can be identified, return the label of the town judge.  Otherwise, return -1. """

import unittest2 as unittest


def find_judge(N, trust):
    """ Consider trust as a graph, all pairs are directed edge. The point with (in-degree - out-degree = N - 1)
        is the judge.
        Keep track of the cumulative score of each person: if person a trusts person b, we decrement a's score and
        increment b's score. The judge is the only person that ends up with a score of N-1.
    Time complexity O(N + T): T = len(trust). We iterate through the trust list once and through all villagers once,
    so the time complexity is linear in these. This is equivalent to |Vertices| + |Edges| in graph terms, if we
    consider each person as a vertex and each trust relationship as a directed edge.
    Space complexity: O(N)
    """
    if not trust:
        return N
    count = [0] * (N + 1)
    for i, j in trust:
        count[i] -= 1
        count[j] += 1
    for i, val in enumerate(count):
        if val == N - 1:
            return i
    return -1


class Test(unittest.TestCase):
    data = [(2, [[1, 2]], 2), (3, [[1, 3], [2, 3]], 3), (3, [[1, 3], [2, 3], [3, 1]], -1)]

    def test_find_judge(self):
        for test_n, test_trust, result in self.data:
            self.assertEqual(result, find_judge(test_n, test_trust))


if __name__ == '__main__':
    unittest.main()
