""" Given a non-empty string s and a dictionary word_dict containing a list of non-empty words, determine if s can be
segmented into a space-separated sequence of one or more dictionary words.
Note:
The same word in the dictionary may be reused multiple times in the segmentation.
You may assume the dictionary does not contain duplicate words. """

import unittest2 as unittest


def word_break_v1(s, word_dict):
    """ Brute force, TLE.
        The naive approach to solve this problem is to use recursion. For finding the solution, we check every possible
        prefix of that string in the dictionary of words, if it is found in the dictionary, then the recursive function
        is called for the remaining portion of that string. And, if in some function call it is found that the complete
        string is in dictionary, then it will return true.
    Time complexity: O(N ** N), Consider the worst case where ss = "\text{aaaaaaa}aaaaaaa" and every prefix of ss is
    present in the dictionary of words, then the recursion tree can grow up to N ** N
    Space complexity: O(N), the depth of the recursion tree can go up to N
    """

    def break_word(i):
        if i == n:
            return True
        for j in range(i + 1, n + 1):
            if s[i:j] in word_dict and break_word(j):
                return True
        return False

    n = len(s)
    word_dict = set(word_dict)
    return break_word(0)


class Test(unittest.TestCase):
    data = [('leetcode', ['leet', 'code'], True), ('applepenapple', ['apple', 'pen'], True),
            ('catsandog', ['cats', 'dog', 'sand', 'and', 'cat'], False)]

    def test_subsets(self):
        for test_string, test_dict, result in self.data:
            self.assertEqual(result, word_break_v1(test_string, test_dict))


if __name__ == '__main__':
    unittest.main()