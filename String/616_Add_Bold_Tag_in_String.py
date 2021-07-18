""" Given a string s and a list of strings dict, you need to add a closed pair of bold tag <b> and </b> to wrap the
substrings in s that exist in dict. If two such substrings overlap, you need to wrap them together by only one pair of
closed bold tag. Also, if two substrings wrapped by bold tags are consecutive, you need to combine them. """

import unittest2 as unittest


def add_bold_tag_v1(s, words):
    """ Let's try to learn which letters end up bold, since the resulting answer will just be the canonical one - we
        put bold tags around each group of bold letters.
        To do this, we'll check for all occurrences of each word and mark the corresponding letters bold.
        Let's work on first setting bold[i] = true if and only if the ith letter is bold. For each starting position i
        in s, for each word, if s[i:] starts with that word, we'll set the appropriate letters bold.
        Now armed with the correct bold, let's try to output the answer.

        A letter in position i is the first bold letter of the group if:
            bold[i] && (i == 0 || !bold[i-1])

        A letter in position i is the last bold letter of the group if:
            bold[i] && (i == N-1 || !bold[i+1]).

        Once we know which letters are the first and last bold letters of a group, we know where to place the '<b>' and
        '</b>' tags.
    Time complexity: O(N * W), where N is the length of s and W is the number of words
    Space complexity: O(N)
    """
    n = len(s)
    bold = [False] * n
    for i in range(n):
        for word in words:
            if s[i:].startswith(word):
                bold[i:i + len(word)] = [True] * len(word)
    res = []
    for i, c in enumerate(s):
        if bold[i] and (i == 0 or not bold[i - 1]):
            res.append('<b>')
        res.append(c)
        if bold[i] and (i == n - 1 or not bold[i + 1]):
            res.append('</b>')
    # Similar (but simpler) loop:
    # i = 0
    # while i < n:
    #     if not bold[i]:
    #         res.append(s[i])
    #         i += 1
    #     else:
    #         res.append('<b>')
    #         while i < n and bold[i]:
    #             res.append(s[i])
    #             i += 1
    #         res.append('</b>')
    return ''.join(res)


def add_bold_tag_v2(s, words):
    """ We can create a list of intervals with opening/closing positions, e.g. [open_tag_index, close_tag_index].
        After that, we merge the list of intervals similar to 56- Merge Intervals. Finally, we go over the merged
        intervals list and insert the tags into the string in the appropriate positions.
        Example: s = 'aaabbcc', dict = ['aaa, 'aab', 'bc']
        We find the start/end index of each string in dict and convert to interval to get:
        [[0, 3], [1, 4], [4, 6]]
          aaa     aab      bc
        We merge these intervals: [0,6], so we know 'aaabbc' needs to be surrounded by bold tag.
    Time complexity: O(N * W + N logN), where N is the length of s and W is the number of words
    Space complexity: O(N)
    """
    n = len(s)
    bold_intervals = []
    for i in range(n):
        for word in words:
            if s[i:].startswith(word):
                bold_intervals.append([i, i + len(word) - 1])
    merged_bold_intervals = []
    for start, end in bold_intervals:
        if not merged_bold_intervals or start > merged_bold_intervals[-1][1] + 1:
            # + 1 to account for cases [x, y], [y+1, z] -> [x, z]
            merged_bold_intervals.append([start, end])
        else:
            merged_bold_intervals[-1][1] = max(merged_bold_intervals[-1][1], end)
    res = []
    previous_tag_end = -1
    for i, (start, end) in enumerate(merged_bold_intervals):
        res.append(s[previous_tag_end + 1: start])
        res.append('<b>')
        res.append(s[start: end + 1])
        res.append('</b>')
        previous_tag_end = end
    res.append(s[previous_tag_end + 1:])
    return ''.join(res)


class Test(unittest.TestCase):
    data = [('abcxyz123', ['abc', '123'], '<b>abc</b>xyz<b>123</b>'),
            ('aaabbcc', ['aaa', 'aab', 'bc'], '<b>aaabbc</b>c')]

    def test_add_bold_tag(self):
        for test_s, test_dict, result in self.data:
            self.assertEqual(result, add_bold_tag_v1(test_s, test_dict))
            self.assertEqual(result, add_bold_tag_v2(test_s, test_dict))


if __name__ == '__main__':
    unittest.main()
