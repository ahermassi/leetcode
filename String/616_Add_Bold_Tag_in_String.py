""" Given a string s and a list of strings dict, you need to add a closed pair of bold tag <b> and </b> to wrap the
substrings in s that exist in dict. If two such substrings overlap, you need to wrap them together by only one pair of
closed bold tag. Also, if two substrings wrapped by bold tags are consecutive, you need to combine them. """

import unittest2 as unittest


def add_bold_tag_v1(s, dict):
    """ Let's try to learn which letters end up bold, since the resulting answer will just be the canonical one - we
        put bold tags around each group of bold letters.
        To do this, we'll check for all occurrences of each word and mark the corresponding letters bold.
        Let's work on first setting bold[i] = true if and only if the ith letter is bold. For each starting position i
        in S, for each word, if S[i:] starts with that word, we'll set the appropriate letters bold.
        Now armed with the correct bold, let's try to output the answer. A letter in position i is the first bold
        letter of the group if bold[i] && (i == 0 || !bold[i-1]), and is the last bold letter if
        bold[i] && (i == N-1 || !bold[i+1]).
        Once we know which letters are the first and last bold letters of a group, we know where to put the '<b>' and
        '</b>' tags.
    Time complexity:
    Space complexity:
    """
    n = len(s)
    bold = [False] * n
    for i in range(n):
        for word in dict:
            if s[i:].startswith(word):
                bold[i:i + len(word)] = [True] * len(word)
    res = []
    for i, c in enumerate(s):
        if bold[i] and (not i or not bold[i - 1]):
            res.append('<b>')
        res.append(c)
        if bold[i] and (i == n - 1 or not bold[i + 1]):
            res.append('</b>')
    return ''.join(res)


class Test(unittest.TestCase):
    data = [('abcxyz123', ['abc', '123'], '<b>abc</b>xyz<b>123</b>'),
            ('aaabbcc', ['aaa', 'aab', 'bc'], '<b>aaabbc</b>c')]

    def test_add_bold_tag(self):
        for test_s, test_dict, result in self.data:
            self.assertEqual(result, add_bold_tag_v1(test_s, test_dict))


if __name__ == '__main__':
    unittest.main()
