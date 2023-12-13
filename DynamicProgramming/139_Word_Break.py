""" Given a non-empty string s and a dictionary word_dict containing a list of non-empty words, determine if s can be
segmented into a space-separated sequence of one or more dictionary words.
Note:
The same word in the dictionary may be reused multiple times in the segmentation.
You may assume the dictionary does not contain duplicate words. """

import unittest2 as unittest


# Video explanation: https://youtu.be/Sx9NNgInc3A
def word_break_v1(s, word_dict):
    """ Brute force. TLE.

        The naive approach to solve this problem is to use recursion. To find the solution, we check every possible
        prefix of that string in the dictionary of words. If it is found in the dictionary, then the recursive function
        is called for the remaining portion of that string. And, if in some function call it is found that the complete
        string is in dictionary, then it will return true.

    Time complexity: O(2^N), given a string of length N, there are (N + 1) ways to split it into two parts; example
    s="abc", we can split it into ["",abc], [a, bc], [ab, c], [abc, ""]. At each step, we have a choice: to split or
    not to split. In the worst case, when all choices are to be checked, and that results in O(2^N). Or using the
    Master Theorem:
    T(N) = T(N-1) + T(N-2) + ... + T(0)
    T(N-1) = T(N-2) + ... + T(0)
    T(N) - T(N-1) = T(N-1)
    T(N) = 2*T(N-1)
    T(N-1) = 2*T(N-2)
    ...
    T(N) = 2 * 2 * .... 2 * T(1) {n-1} times => ~ 2^N-1 => O(2^N)
    Space complexity: O(N), the depth of the recursion tree can go up to N
    """

    def dfs(index):
        """ Return true if the substring starting at 'index' can be partitioned according to the words' dictionary. """
        if index == n:
            return True
        for i in range(index, n):  # Try all the possible chopping indices
            if s[index:i+1] in word_dict and dfs(i+1):
                # If the prefix up to index i can be found in the dictionary and the rest of the string can be
                # partitioned the same way, then we're done.
                return True
        return False

    n, word_dict = len(s), set(word_dict)
    return dfs(0)


def word_break_v2(s, word_dict):
    """ Top-Down Dynamic Programming.

         In the previous solution, we can see that many sub-problems were redundant, i.e. we were calling the recursive
         function multiple times for a particular prefix. To avoid this, we can use memoization/caching, where an array
         'memo' is used to store the results of the previously calculated sub-problems.

         Using memoization, many redundant sub-problems are avoided and recursion tree is pruned, and thus it reduces
         the time complexity by a large factor.

    Time complexity: O(N * L), where L is the average length of the words in the words' dictionary. There are N states,
    and thanks to memoization we only calculate each state once. To calculate a state, we perform some substring
    operations which costs O(L).
    Space complexity: O(N)
    """

    def dfs(index):
        if index == n:
            return True
        if index not in memo:
            for i in range(index, n):
                if s[index:i + 1] in word_dict and dfs(i + 1):
                    memo[index] = True
                    return True
        memo[index] = False
        return False

    n, word_dict, memo = len(s), set(word_dict), {}
    return dfs(0)


def word_break_v3(s, word_dict):
    """ Dynamic programming.
        dp[i] is True if s[:i] can be segmented into words from the dictionary.
        In other words:
            dp[i] = True if the first i characters of s can be partitioned according to the words in the dictionary
        The intuition behind this approach is that the given problem (s) can be divided into sub problems s1 and s2. If
        these sub problems individually satisfy the required conditions, the complete problem s also satisfies the
        same.
        For example, 'catsanddog' can be split into two substrings 'catsand', 'dog'. The sub problem 'catsand' can be
        further divided into 'cats', 'and', which individually are part of the dictionary making 'catsand' satisfy the
        condition. Going further backwards, 'catsand', 'dog' also satisfy the required criteria individually leading to
        the complete string 'catsanddog' also to satisfy the criteria.
    Time complexity: O(N^3), not O(N^2) because of the substring s[i:j] which takes O(N)
    Space complexity: ? O(N) for dp array + set of dictionary's word
    """
    n, word_dict = len(s), set(word_dict)
    dp = [False] * (n + 1)
    dp[0] = True
    for i in range(1, n + 1):
        for j in range(i):
            if dp[j] and s[j:i] in word_dict:  # The first j characters of the string can be partitioned using the
                # words in the dictionary and the rest of the string contains one of the words of the dictionary
                dp[i] = True
                break  # Break. The first i characters can be segmented. We have no more business here
    return dp[n]


def word_break_v4(s, word_dict):
    """ Dynamic programming.
        In this solution, instead of trying to find a substring that belongs to the set of dictionary words, we instead
        verify if a word of the dictionary is a substring of s starting at index (i - len(word)).
        If dp[i - len(word)] == True，it would make sure that s[:i - len(word)] can be divided using dictionary.
        Then combined with s[i - len(word) : i] == word , we can conclude that dp[:i] can also be divided.
    Time complexity: O(M * N^2), where N is the length of s and M is the number of words in the dictionary
    Space complexity: O(N), for dp array
    """
    n = len(s)
    dp = [False] * (n + 1)
    dp[0] = True
    for i in range(1, n + 1):
        for word in word_dict:
            if dp[i - len(word)] and s[i - len(word):i] == word:  # dp[i-len(word)] guarantees that dp is True right
                # before the word we're looking for, and s[i-len(word):i] == word means that we've found the word in s.
                dp[i] = True
                break
    return dp[n]


class Test(unittest.TestCase):
    data = [('leetcode', ['leet', 'code'], True), ('applepenapple', ['apple', 'pen'], True),
            ('catsandog', ['cats', 'dog', 'sand', 'and', 'cat'], False)]

    def test_word_break(self):
        for test_string, test_dict, result in self.data:
            self.assertEqual(result, word_break_v1(test_string, test_dict))
            self.assertEqual(result, word_break_v2(test_string, test_dict))
            self.assertEqual(result, word_break_v3(test_string, test_dict))
            self.assertEqual(result, word_break_v4(test_string, test_dict))


if __name__ == '__main__':
    unittest.main()
