""" Given a non-empty string s and a dictionary word_dict containing a list of non-empty words, add spaces in s to
construct a sentence where each word is a valid dictionary word. Return all such possible sentences.
Note:
The same word in the dictionary may be reused multiple times in the segmentation.
You may assume the dictionary does not contain duplicate words. """

from collections import Counter
import unittest2 as unittest


# Video explanation: https://www.youtube.com/watch?v=uR3RElKnrkU
# Video explanation: https://www.youtube.com/watch?v=QgLKdluDo08
def word_break_v1(s, word_dict):
    """ Top-Down Dynamic Programming.

         Initially, we might think of a brute force approach where we systematically explore all possible ways to break
         the string into words from the dictionary. This leads us to the backtracking strategy, where we recursively
         try to form words from the string and add them to a current sentence if they are in the dictionary.

         If the current prefix doesn't lead to a valid solution, we backtrack by removing the last added word and
         trying the next possible word. This ensures we explore all possible segmentations of the string.

            - At each step, we consider all possible end indices for substrings starting from the current index.

            - For each substring, we check if it exists in the dictionary.

            - If the substring is a valid word, we append it to the current sentence and recursively call the function
               with the updated index, which is the end index of the substring plus one.

            - If we reach the end of the string, it means we have found a valid segmentation, and we can add the
               current sentence to the results. However, if we encounter a substring that is not a valid word, we
               backtrack by returning from that recursive call and trying the next possible end index.

        To increase efficiency, we will convert the word dictionary into a set for constant-time lookups.

        We can improve the efficiency of the backtracking method by using memoization, which stores the results of
        sub-problems to avoid recalculating them.

    Time complexity: O(N * 2^N), where N is the length of the input string. The algorithm explores all possible ways to
    break the string into words. In the worst case, where each character can be treated as a word, the recursion tree
    has 2^N leaf nodes, resulting in an exponential time complexity. For each leaf node, O(nN) work is performed.
    Consider the input "aaaaaa", with wordDict = ["a", "aa", "aaa", "aaaa", "aaaaa", "aaaaa"]. Every possible partition
    is a valid sentence, and there are 2^N-1 such partitions. Given an array of length N, there are N+1 ways/intervals
    to partition it into two parts. Each interval has two choices - split or not. In the worse case, we will have to
    check all possibilities, which becomes O(2^(N+1)) ~= O(2^N).
    Space complexity: O(N)
    """

    def dfs(index):
        if index == n:
            return ['']
        if index in memo:
            return memo[index]
        res = []
        for i in range(index, n):
            prefix = s[index:i + 1]
            if prefix in word_dict:
                sentences = dfs(i + 1)
                for sentence in sentences:
                    if sentence == '':
                        res.append(prefix)
                    else:
                        res.append(prefix + ' ' + sentence)
        memo[index] = res
        return res

    n = len(s)
    word_dict = set(word_dict)
    memo = {}
    return dfs(0)


def word_break_v2(s, word_dict):
    """ An optimization of the previous solution. We calculate the length of the longest word in the dictionary.
         When we check for the existence of the prefixes in the dictionary, we only consider those whose length is not
         greater than the max word length.

    Time complexity: O(2^N)
    Space complexity: O(N)
    """

    def dfs(index):
        if index == n:
            return ['']
        if index in memo:
            return memo[index]
        res = []
        for i in range(index, index + max_len[0]):
            prefix = s[index:i + 1]
            if prefix in word_dict:
                sentences = dfs(i + 1)
                for sentence in sentences:
                    if sentence == '':
                        res.append(prefix)
                    else:
                        res.append(prefix + ' ' + sentence)
        memo[index] = res
        return res

    n = len(s)
    word_dict = set(word_dict)
    longest_word = max(word_dict, key=len)
    max_len = [len(longest_word)]
    memo = {}
    return dfs(0)


def word_break_v3(s, word_dict):
    """ Bottom-up dynamic programming.
        Following the same definition in the top-down approach, given an input string s = 'catsanddog', we define the
        results of breaking it into words with the function F(s).
        For any word (denoted as w) in the dictionary, if it matches with a SUFFIX of the input string, we then can
        divide the string into two parts: the prefix and the word, i.e. s = prefix + w.
        Consequently, the solution for the input string can be represented as follows:
            ∀ w ∈ dict, s = prefix + w ⟹ {F(prefix) + w} ∈⊆F(s)
        i.e. we add the matched word to the solutions from the prefix.
        We start from an empty prefix (i.e. the bottom case), to progressively extend the solutions to a larger prefix.
        Eventually, the extended prefix would grow to be the original string.
        We define the dp array as follows:

            dp[i] = solutions for the corresponding prefix s[:i], or first i characters of s

        The desired result would be the last element in the array, i.e. dp[len(s)], which corresponds to the results
        for the entire string.
        We ad an additional check at the beginning of the algorithm to see if the input string contains some characters
        that do not appear in any of the words in the dictionary. If this is the case, then we are sure that the input
        string cannot be broken down into words. With this check, we could bypass some tricky test cases, not ending up
        with the TLE error.
    """
    if set(Counter(s).keys()) > set(Counter(''.join(word_dict)).keys()):
        return []
    n, word_dict = len(s), set(word_dict)
    dp = [[]] * (n + 1)
    dp[0] = ['']
    for i in range(1, n + 1):
        res = []
        for j in range(i):
            suffix = s[j:i]
            if suffix in word_dict:  # s[:i] = s[:j] + s[j:i] = s[:j] + suffix, so we append suffix to results of s[:j]
                for subs in dp[j]:
                    res.append(subs + ' ' + suffix if subs else suffix)
        dp[i] = res
    return dp[-1]


class Test(unittest.TestCase):
    data = [('catsanddog', ['cat', 'cats', 'and', 'sand', 'dog'], ['cat sand dog', 'cats and dog']), (
        'pineapplepenapple', ['apple', 'pen', 'applepen', 'pine', 'pineapple'],
        ['pine apple pen apple', 'pine applepen apple', 'pineapple pen apple']),
            ('catsandog', ['cats', 'dog', 'sand', 'and', 'cat'], [])]

    def test_word_break(self):
        for test_string, test_word_dict, result in self.data:
            self.assertEqual(result, word_break_v1(test_string, test_word_dict))
            self.assertEqual(result, word_break_v2(test_string, test_word_dict))
            self.assertEqual(result, word_break_v3(test_string, test_word_dict))


if __name__ == '__main__':
    unittest.main()
