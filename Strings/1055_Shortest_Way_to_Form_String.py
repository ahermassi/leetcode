""" From any string, we can form a sub sequence of that string by deleting some number of characters (possibly no
deletions).
Given two strings source and target, return the minimum number of sub sequences of source such that their concatenation
equals target. If the task is impossible, return -1. """

import unittest2 as unittest


def shortest_way_v1(source, target):
    """ We traverse the target string while matching source string multiple times.
        i: index for target string
        j: index for source string
        We use a set to save all the characters in source, and if there exists a character from target which doesn't
        exist in the set, we exist early and return -1.
    Time complexity: O(N * M), where N is the length of source and M is the length of target
    Space complexity: O(M)
    """
    count, n = 0, len(target)
    chars = set(source)
    for c in target:
        if c not in chars:
            return -1
    i = 0
    while i < n:
        for j, c in enumerate(source):
            if i < n and c == target[i]:
                i += 1
            j += 1
        count += 1
    return count


class Test(unittest.TestCase):
    data = [('abc', 'abcbc', 2), ('abc', 'acdbc', -1), ('xyz', 'xzyxz', 3)]

    def test_shortest_way(self):
        for test_source, test_target, result in self.data:
            self.assertEqual(result, shortest_way_v1(test_source, test_target))


if __name__ == '__main__':
    unittest.main()