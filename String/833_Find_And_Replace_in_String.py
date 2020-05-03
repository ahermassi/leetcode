""" See problem description on leetcode """

import unittest2 as unittest


def find_replace_string_v1(S, indexes, sources, targets):
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
            i += len(d[i][0])  # We skip as many characters we replaced because that entire substring no longer exists
        else:  # No characters to replace at the current index, so append the original character
            res.append(c)
            i += 1
    return ''.join(res)


def find_replace_string_v2(S, indexes, sources, targets):
    """ Make a list of characters out of the string. When an index and a source match in the original string, replace
        the character at that list index with the ENTIRE target string and remove the following characters that occur
        in the original string from the list (up to the source length).
    Time complexity: O(N + Q), where N is the length of S and Q is the length of indexes (or sources, or targets)
    Space complexity: O(N + Q)
    """
    res = list(S)
    for index, source, target in zip(indexes, sources, targets):
        if S[index:index + len(source)] == source:
            res[index] = target
            for i in range(index + 1, index + len(source)):
                res[i] = ''
    return ''.join(res)


def find_replace_string_v3(S, indexes, sources, targets):
    """ This solution looks like an in-place replacement, but in fact a new string is created with each replacement.
        We do it from right to left so the new replacement can’t override the indices that come after in the string.
    Time complexity: TODO
    Space complexity: TODO
    """
    for index, source, target in sorted(zip(indexes, sources, targets), reverse=True):
        S = S[:index] + target + S[index + len(source):] if S[index:index + len(source)] == source else S
    return S


class Test(unittest.TestCase):
    data = [('abcd', [0, 2], ['a', 'cd'], ['eee', 'ffff'], 'eeebffff'),
            ('abcd', [0, 2], ['ab', 'ec'], ['eee', 'ffff'], 'eeecd')]

    def test_find_replace_string(self):
        for test_string, indexes, sources, targets, result in self.data:
            self.assertEqual(result, find_replace_string_v1(test_string, indexes, sources, targets))
            self.assertEqual(result, find_replace_string_v2(test_string, indexes, sources, targets))
            self.assertEqual(result, find_replace_string_v3(test_string, indexes, sources, targets))


if __name__ == '__main__':
    unittest.main()