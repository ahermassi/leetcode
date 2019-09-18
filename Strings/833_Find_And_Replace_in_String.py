""" See problem description on leetcode """

import unittest2 as unittest


def find_replace_string(S, indexes, sources, targets):
    """ Pretty straightforward. Scan S from left to right and run some verifications.
    Time complexity: O(N + Q), where N is the length of S and Q is the length of indexes (or sources, or targets)
    Space complexity: O(N + Q)
    """
    i, res = 0, []
    d = {index: [source, target] for index, source, target in zip(indexes, sources, targets)}
    while i < len(S):
        c = S[i]
        if i in d and S[i:i + len(d[i][0])] == d[i][0]:
            res.append(d[i][1])
            i += len(d[i][0])
        else:
            res.append(c)
            i += 1
    return ''.join(res)


class Test(unittest.TestCase):
    data = [('abcd', [0, 2], ['a', 'cd'], ['eee', 'ffff'], 'eeebffff'),
            ('abcd', [0, 2], ['ab', 'ec'], ['eee', 'ffff'], 'eeecd')]

    def test_find_replace_string(self):
        for test_string, indexes, sources, targets, result in self.data:
            self.assertEqual(result, find_replace_string(test_string, indexes, sources, targets))


if __name__ == '__main__':
    unittest.main()