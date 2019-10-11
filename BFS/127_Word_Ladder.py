""" Given two words (beginWord and endWord), and a dictionary's word list, find the length of shortest transformation
sequence from beginWord to endWord, such that:
Only one letter can be changed at a time.
Each transformed word must exist in the word list. Note that beginWord is not a transformed word. """

from collections import deque, defaultdict
import unittest2 as unittest

# For both solutions, check out this article: https://leetcode.com/articles/word-ladder/


def ladder_length_v1(beginWord, endWord, wordList):
    """ BFS. One of the most important steps here is to figure out how to find adjacent nodes i.e. words which differ
        by one letter. To efficiently find the neighboring nodes for any given word we do some pre-processing on the
        words of the given wordList. The pre-processing involves replacing the letter of a word by a non-alphabet
        say, *. This pre-processing helps to form generic states to represent a single letter change.
        For e.g. Dog ----> D*g <---- Dig
        Both Dog and Dig map to the same intermediate or generic state D*g.
        Start from beginWord and search the endWord using BFS.
    Time complexity: O(N * M**2) where N is the number of words and M is the length of each word (same length)
    Space complexity: O(N * M), O(N * M) for patterns dictionary, O(N) for queue and visited set, so overall O(N * M)
    """
    if endWord not in wordList:
        return 0
    queue = deque([(beginWord, 1)])
    patterns = defaultdict(list)  # Dictionary to hold combination of words that can be formed, from any given word,
    # by changing one letter at a time.
    for word in wordList:
        for i in range(len(word)):
            patterns[word[:i] + '*' + word[i + 1:]].append(word)
    visited = set()  # Visited to make sure we don't repeat processing same word.
    while queue:
        word, depth = queue.popleft()
        for i in range(len(word)):
            pattern = word[:i] + '*' + word[i + 1:]
            for w in patterns[pattern]:  # The words which share the same intermediate state/pattern
                if w == endWord:
                    return depth + 1
                if w not in visited:
                    queue.append((w, depth + 1))
                    visited.add(w)
    return 0


class Test(unittest.TestCase):
    data = [('hit', 'cog', ['hot', 'dot', 'dog', 'lot', 'log', 'cog'], 5),
            ('hit', 'cog', ['hot', 'dot', 'dog', 'lot', 'log'], 0)]

    def test_max_product(self):
        for test_begin_word, test_end_word, test_word_list, result in self.data:
            self.assertEqual(result, ladder_length_v1(test_begin_word, test_end_word, test_word_list))


if __name__ == '__main__':
    unittest.main()
