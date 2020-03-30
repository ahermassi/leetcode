""" In a town, there are N people labelled from 1 to N.  There is a rumor that one of these people is secretly the
town judge.
If the town judge exists, then:
- The town judge trusts nobody.
- Everybody (except for the town judge) trusts the town judge.
- There is exactly one person that satisfies properties 1 and 2.
You are given trust, an array of pairs trust[i] = [a, b] representing that the person labelled a trusts the person
labelled b.
If the town judge exists and can be identified, return the label of the town judge.  Otherwise, return -1. """

import unittest2 as unittest


def find_judge_v1(N, trust):
    """ Consider trust as a graph, all pairs are directed edges. Each trust pair [a, b] represents a directed edge
        going from a to b. The vertex with indegree - outdegree = N - 1 is the judge.
        For this graph, the outdegree of the vertex represents the number of other people that person trusts.
        The indegree of a vertex (person) represents the number of people that trust that person.
        We can define the town judge in terms of indegree and outdegree:
            The town judge has an outdegree of 0 and an indegree of N - 1 because they trust nobody, and everybody
            trusts them (except themselves).
        Therefore, this problem simplifies to calculating the indegree and outdegree for each person and then checking
        whether or not any of them meet the criteria of the town judge.
    Time complexity O(N + T): T = len(trust). We iterate through the trust list once and through all villagers once,
    so the time complexity is linear in these. This is equivalent to |Vertices| + |Edges| in graph terms, if we
    consider each person as a vertex and each trust relationship as a directed edge.
    Space complexity: O(N), where N is the number of people
    """
    indegree, outdegree = [0] * (N + 1), [0] * (N + 1)
    for frm, to in trust:
        indegree[to] += 1
        outdegree[frm] += 1
    for i in range(1, N + 1):
        if indegree[i] == N - 1 and outdegree[i] == 0:
            return i
    return -1


def find_judge_v2(N, trust):
    """ We don't need separate arrays for indegree and outdegree. We can instead build a single array with the result
        of (indegree - outdegree) for each person. In other words, we'll +1 to their 'score' for each person they are
        trusted by, and -1 from their 'score' for each person they trust. Therefore, for a person to maximize their
        'score', they should be trusted by as many people as possible, and trust as few people as possible.
        The maximum indegree is N - 1. This represents everybody trusting the person (except for themselves). The
        minimum outdegree is 0. This represents not trusting anybody. Therefore, the maximum value for
        (indegree - outdegree) is (N - 1) - 0 = N - 1. These values also happen to be the definition of the town judge.
    Time complexity O(N + T)
    Space complexity: O(N), where N is the number of people
    """
    count = [0] * (N + 1)  # count[i] = indegree[i] - outdegree[i]
    for frm, to in trust:
        count[frm] -= 1
        count[to] += 1
    for i, val in enumerate(count):
        if val == N - 1:
            return i
    return -1


class Test(unittest.TestCase):
    data = [(2, [[1, 2]], 2), (3, [[1, 3], [2, 3]], 3), (3, [[1, 3], [2, 3], [3, 1]], -1)]

    def test_find_judge(self):
        for test_n, test_trust, result in self.data:
            self.assertEqual(result, find_judge_v1(test_n, test_trust))
            self.assertEqual(result, find_judge_v2(test_n, test_trust))


if __name__ == '__main__':
    unittest.main()
