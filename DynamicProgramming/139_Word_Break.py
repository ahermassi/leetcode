""" Given a non-empty string s and a dictionary word_dict containing a list of non-empty words, determine if s can be
segmented into a space-separated sequence of one or more dictionary words.
Note:
The same word in the dictionary may be reused multiple times in the segmentation.
You may assume the dictionary does not contain duplicate words. """

import unittest2 as unittest


def word_break_v1(s, word_dict):
    """ Brute force, top-down recursion. TLE.
        The naive approach to solve this problem is to use recursion. To find the solution, we check every possible
        prefix of that string in the dictionary of words. If it is found in the dictionary, then the recursive function
        is called for the remaining portion of that string. And, if in some function call it is found that the complete
        string is in dictionary, then it will return true.
    Time complexity: O(2^N), Consider the worst case where s = 'aaaaaaa' and every prefix of s is present in the
    dictionary of words, then the recursion tree can grow up to 2^N
    Space complexity: O(N), the depth of the recursion tree can go up to N
    """

    def dfs(index):
        """ dfs(index) returns True if the substring starting at 'index' can be partitioned according to the
            dictionary's words.
        """
        if index == n:
            return True
        for j in range(index, n):  # Try all the possible chopping indices
            if s[index:j+1] in word_dict and dfs(j+1):  # If the substring up to index j can be found in the
                # dictionary and the rest of the string can be partitioned the same way, then we're done.
                return True
        return False

    n = len(s)
    word_dict = set(word_dict)
    return dfs(0)


def word_break_v2(s, word_dict):
    """ In the previous approach, we can see that many sub problems were redundant, i.e we were calling the recursive
        function multiple times for a particular string. To avoid this, we can use memoization method, where an array
        memo is used to store the results of the sub problems. Now, when the function is called again for a particular
        string, value will be fetched and returned using the memo array, if its value has been already evaluated.
        With memoization many redundant sub problems are avoided and recursion tree is pruned and thus it reduces the
        time complexity by a large factor.
    Time complexity: O(N^2)
    Space complexity: O(N)
    """

    def dfs(index):
        if index == n:
            return True
        if index in memo:
            return memo[index]
        for j in range(index, n):
            if s[index:j+1] in word_dict and dfs(j+1):
                memo[index] = True
                return True
        memo[index] = False
        return False

    n = len(s)
    word_dict, memo = set(word_dict), {}
    return dfs(0)


def word_break_v3(s, word_dict):
    """ Dynamic programming.
        dp[i] is True if s[:i] can be segmented into words from the dictionary.
        In other words: dp[i] = True means the first i characters of s can be partitioned according the words in the
        dictionary.
        The intuition behind this approach is that the given problem (s) can be divided into sub problems s1 and s2. If
        these sub problems individually satisfy the required conditions, the complete problem s also satisfies the
        same.
        For example, 'catsanddog' can be split into two substrings 'catsand', 'dog'. The sub problem 'catsand' can be
        further divided into 'cats','and', which individually are part of the dictionary making 'catsand' satisfy the
        condition. Going further backwards, 'catsand', 'dog' also satisfy the required criteria individually leading to
        the complete string 'catsanddog' also to satisfy the criteria.
    Time complexity: O(N^3), not O(N^2) because of the substring s[i:j] which takes O(N)
    Space complexity: ? O(N) for dp array + set of dictionary's word
    """
    n = len(s)
    dp = [False] * (n + 1)
    word_dict = set(word_dict)
    dp[0] = True
    for i in range(n):  # This could be 'for i in range(n+1)', but when i = n (last iteration) 'if dp[i]' afterwards
        # will mean 'if the first n characters verify the property' and the rest of the block would be meaningless and
        # never executed
        if dp[i]:  # If the first i characters of the string can be partitioned using the words in the dictionary
            for j in range(i + 1, n + 1):
                if s[i:j] in word_dict:  # See if the rest of the string contains one of the words of the dictionary
                    dp[j] = True  # Since the first i characters and the characters from (i+1) to j (exclusive) verify
                    # the property, then the first j characters verify the property as well
    return dp[n]


class Test(unittest.TestCase):
    data = [('leetcode', ['leet', 'code'], True), ('applepenapple', ['apple', 'pen'], True),
            ('catsandog', ['cats', 'dog', 'sand', 'and', 'cat'], False)]

    def test_word_break(self):
        for test_string, test_dict, result in self.data:
            self.assertEqual(result, word_break_v1(test_string, test_dict))
            self.assertEqual(result, word_break_v2(test_string, test_dict))
            self.assertEqual(result, word_break_v3(test_string, test_dict))


if __name__ == '__main__':
    unittest.main()
