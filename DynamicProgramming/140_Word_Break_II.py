""" Given a non-empty string s and a dictionary wordDict containing a list of non-empty words, add spaces in s to
construct a sentence where each word is a valid dictionary word. Return all such possible sentences.
Note:
The same word in the dictionary may be reused multiple times in the segmentation.
You may assume the dictionary does not contain duplicate words. """

import unittest2 as unittest


# Great explanation: https://www.youtube.com/watch?v=uR3RElKnrkU

def word_break_v1(s, word_dict):
    """ Top-down dynamic programming.
        Given an input string s = 'catsanddog', we define the results of breaking it into words with the function F(s).
        For any word (denoted as w) in the dictionary, if it matches with a prefix of the input string, we then can
        divide the string into two parts: the word and the suffix, i.e. s = w + suffix
        Consequently, the solution for the input string can be represented as follows:
            ∀ w ∈ dict, s = w + suffix ⟹ {w + F(suffix)} ∈⊆F(s)
        i.e. we add the matched word to the solutions from the suffix.
        For example, the word 'cat' matches with a prefix of the string. As a result, we can divide the string into
        s = 'cat'+ 'sanddog’.
        For the suffix 'sanddog', we could obtain the results by recursively applying our function, i.e.
        F('sanddog')={'sand dog'}. By adding the prefix word to the solutions of the postfix, we then obtain one of
        the solutions for the original string, i.e. 'cat sand dog' ∈ F(s).
        The above approach can be considered as a top-down DP. The reason lies in the part that we adopt the
        laissez-faire strategy, i.e. we simply take a first step, while assuming the subsequent steps will figure out
        on their own.
        In our case, we first find a match to a prefix of the string, while assuming that we would eventually obtain
        the results for the corresponding suffix.
        Following the above intuition, it seems intuitive to implement the solution with recursion.
        We define a recursive function called dfs(s) which generates the results for the input string.
        First of all, as the base case of the recursion, when the input string is empty, the recursion would terminate.
        As the main body of the function, we run an iteration over all the words of the dictionary. If the
        corresponding word happens to match a prefix in the string, we then invoke recursively the function on the
        suffix (rest of string).
        At the end of the iteration, we keep the results in the hash map named memo with each valid substring as its
        key and the list of words that compose the prefix of as the value. For instance, for the substring 'dogo', its
        corresponding entry in the hash map would be memo['dogo'] = ['do', 'go'].
        Finally, as the result, we return the entry of memo with the input string as the key.
    """

    def dfs(s):  # dfs(s) returns a list containing all sentences derived from s
        if not s:
            return ['']
        if s not in memo:
            res = []
            for word in word_dict:
                if s.startswith(word):
                    rest_of_string = dfs(s[len(word):])  # Move forward to break the suffix into words
                    for subs in rest_of_string:
                        res.append(word + ' ' + subs if subs else word)  # Account for subs = '' when suffix is empty
            memo[s] = res

        return memo[s]

    memo = {}  # Map a string to its corresponding words break
    return dfs(s)


def word_break_v2(s, word_dict):
    """ The dictionary of words can be really huge, which will make the previous solution implausible. So it's better
        to solve this problem in a formal way.
        The logic is still the same, but we run an iteration over all the prefixes of the input string instead of words
        of the dictionary. If the corresponding prefix happens to match a word in the dictionary, we then invoke
        recursively the function on the suffix.
    """

    def dfs(s):
        if not s:
            return ['']
        if s not in memo:
            n, res = len(s), []
            for i in range(n + 1):  # When i=n (last iteration), prefix=s[:n] which matches the entire string s
                prefix, suffix = s[:i], s[i:]
                if prefix in word_dict:
                    rest_of_string = dfs(suffix)
                    for subs in rest_of_string:
                        res.append(prefix + ' ' + subs if subs else prefix)
            memo[s] = res
        return memo[s]

    word_dict = set(word_dict)
    memo = {}
    return dfs(s)


class Test(unittest.TestCase):
    data = [('catsanddog', ['cat', 'cats', 'and', 'sand', 'dog'], ['cat sand dog', 'cats and dog']), (
        'pineapplepenapple', ['apple', 'pen', 'applepen', 'pine', 'pineapple'],
        ['pine apple pen apple', 'pine applepen apple', 'pineapple pen apple']),
            ('catsandog', ['cats', 'dog', 'sand', 'and', 'cat'], [])]

    def test_word_break(self):
        for test_string, test_word_dict, result in self.data:
            self.assertEqual(result, word_break_v1(test_string, test_word_dict))
            self.assertEqual(result, word_break_v2(test_string, test_word_dict))


if __name__ == '__main__':
    unittest.main()
