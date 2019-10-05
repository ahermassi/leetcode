""" Given a non-empty string s and a dictionary word_dict containing a list of non-empty words, determine if s can be
segmented into a space-separated sequence of one or more dictionary words.
Note:
The same word in the dictionary may be reused multiple times in the segmentation.
You may assume the dictionary does not contain duplicate words. """

from collections import defaultdict
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
        for j in range(i + 1, n + 1):  # We go up to n + 1 to guarantee that the entire string is processed
            if s[i:j] in word_dict and break_word(j):
                return True
        return False

    n = len(s)
    word_dict = set(word_dict)
    return break_word(0)


def word_break_v2(s, word_dict):
    """ In the previous approach we can see that many sub problems were redundant, i.e we were calling the recursive
        function multiple times for a particular string. To avoid this we can use memoization method, where an array
        memo is used to store the result of the sub problems. Now, when the function is called again for a particular
        string, value will be fetched and returned using the memo array, if its value has been already evaluated.
        With memoization many redundant sub problems are avoided and recursion tree is pruned and thus it reduces the
        time complexity by a large factor.
    Time complexity: O(N ** 2)
    Space complexity: O(N)
    """

    def break_word(i):
        if i == n:
            return True
        if i in memo:
            return memo[i]
        for j in range(i + 1, n + 1):
            if s[i:j] in word_dict and break_word(j):
                memo[i] = True
                return True
        memo[i] = False
        return False

    n = len(s)
    word_dict, memo = set(word_dict), defaultdict(bool)
    return break_word(0)


def word_break_v3(s, word_dict):
    """ Dynamic programming approach.
        The intuition behind this approach is that the given problem (s) can be divided into sub problems s1 and s2. If
        these sub problems individually satisfy the required conditions, the complete problem, s also satisfies the
        same. e.g. 'catsanddog' can be split into two substrings 'catsand', 'dog'. The sub problem 'catsand' can be
        further divided into 'cats','and', which individually are a part of the dictionary making 'catsand' satisfy the
        condition. Going further backwards, 'catsand', 'dog' also satisfy the required criteria individually leading to
        the complete string 'catsanddog' also to satisfy the criteria.
    Time complexity: O(N ** 2)
    Space complexity: O(N) for dp array
    """
    dp = [False] * (len(s) + 1)
    dp[0] = True
    for i in range(len(s)):
        if dp[i]:
            for j in range(i + 1, len(s) + 1):
                if s[i:j] in word_dict:
                    dp[j] = True
    return dp[-1]


class Test(unittest.TestCase):
    data = [('leetcode', ['leet', 'code'], True), ('applepenapple', ['apple', 'pen'], True),
            ('catsandog', ['cats', 'dog', 'sand', 'and', 'cat'], False)]

    def test_subsets(self):
        for test_string, test_dict, result in self.data:
            self.assertEqual(result, word_break_v1(test_string, test_dict))
            self.assertEqual(result, word_break_v2(test_string, test_dict))
            self.assertEqual(result, word_break_v3(test_string, test_dict))


if __name__ == '__main__':
    unittest.main()
