""" Given a list of words, each word consists of English lowercase letters.
Let's say word1 is a predecessor of word2 if and only if we can add exactly one letter anywhere in word1 to make it
equal to word2.  For example, "abc" is a predecessor of "abac".
A word chain is a sequence of words [word_1, word_2, ..., word_k] with k >= 1, where word_1 is a predecessor of word_2,
word_2 is a predecessor of word_3, and so on.
Return the longest possible length of a word chain with words chosen from the given list of words. """

import unittest2 as unittest


def longest_str_chain_v1(words):
    """ Instead of adding a character, try deleting a character to form a chain in reverse.
        Let dp[word] be the longest string chain that ends at 'word'. This information is used for optimally compute
        the best chain length that ends with a longer word.
        Sort the words by word's length. For each word, loop on all possible previous words with 1 letter missing.
        If we have seen this previous word, update the longest chain for the current word:
            dp[word] = max(dp[word], dp[word_missing_one_character] + 1)
        Finally return the longest word chain.
        For example, when we want to compute the best chain length that ends with word 'abc', it is:
            max (dp['ab'], dp['ac'], dp['bc'])
    Time complexity: O(N logN + N * S^2), where N is the number of words and S is the length of longest word (16)
    Space complexity: O(N + S), for Timsort, hash map, and the substring 'prev'
    """
    words.sort(key=len)
    dp = {word: 1 for word in words}
    for word in words:
        n = len(word)
        for i in range(n):
            prev = word[:i] + word[i + 1:]
            if prev in dp:
                dp[word] = max(dp[word], dp[prev] + 1)
    return max(dp.values())


class Test(unittest.TestCase):
    data = [(['a', 'b', 'ba', 'bca', 'bda', 'bdca'], 4)]

    def test_longest_str_chain(self):
        for test_words, result in self.data:
            self.assertEqual(result, longest_str_chain_v1(test_words))


if __name__ == '__main__':
    unittest.main()
