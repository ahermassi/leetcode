""" Given two words (beginWord and endWord), and a dictionary's word list, find the length of shortest transformation
sequence from beginWord to endWord, such that:
Only one letter can be changed at a time.
Each transformed word must exist in the word list. Note that beginWord is not a transformed word. """

from collections import deque, defaultdict
import unittest2 as unittest

# For both solutions, check out this article: https://leetcode.com/articles/word-ladder/


def ladder_length_v1(beginWord, endWord, wordList):
    """ We are given a beginWord and an endWord. Let these two represent start node and end node of a graph. We have to
        reach from the start node to the end node using some intermediate nodes/words. The intermediate nodes are
        determined by the wordList given to us. The only condition for every step we take on this ladder of words is
        the current word should change by just one letter.
        We will essentially be working with an undirected and unweighted graph with words as nodes and edges between
        words which differ by just one letter. The problem boils down to finding the shortest path from a start node to
        a destination node, if there exists one. Hence it can be solved using Breadth First Search approach.
        One of the most important steps here is to figure out how to find adjacent nodes i.e. words which differ
        by one letter. To efficiently find the neighboring nodes for any given word, we do some pre-processing on the
        words of the given wordList. The pre-processing involves replacing the letter of a word by a non-alphabet, say,
        *. This pre-processing helps to form generic states to represent a single letter change.
        For e.g. Dog ----> D*g <---- Dig
        Both Dog and Dig map to the same intermediate or generic state D*g.
        The pre-processing step helps us find out the generic one letter away nodes for any word of the word list and
        hence making it easier and quicker to get the adjacent nodes. Otherwise, for every word we will have to iterate
        over the entire word list and find words that differ by one letter. That would take a lot of time. This
        pre-processing step essentially builds the adjacency list first before beginning the breadth first search
        algorithm.
        Start from beginWord and search the endWord using BFS. To prevent cycles, use a visited set. Eventually, if we
        reach the desired word, its level would represent the shortest transformation sequence length.
    Time complexity: O(N * M), where M is the length of words (all words have same length) and N is the total number of
    words in the input word list. Finding out all the transformations takes M iterations for each of the NN words.
    Also, breadth first search in the worst case might go to each of the N words.
    Space complexity: O(N * M), to store all M transformations for each of the N words, in the 'transformations'
    dictionary, 'visited' set is of size N, queue for BFS in worst case would need space for all N words.
    """
    if endWord not in wordList:
        return 0
    transformations = defaultdict(list)  # Dictionary to hold patterns of words that can be formed, from any given
    # word, by changing one letter at a time.
    for word in wordList:
        for i in range(len(word)):
            transformations[word[:i] + '*' + word[i + 1:]].append(word)
    queue = deque([(beginWord, 1)])
    visited = set()  # Visited to make sure we don't repeat processing same word.
    while queue:
        word, depth = queue.popleft()
        for i in range(len(word)):
            pattern = word[:i] + '*' + word[i + 1:]
            for w in transformations[pattern]:  # The words which share the same intermediate state/pattern
                if w == endWord:  # End word is 1 transformation away
                    return depth + 1
                if w not in visited:
                    visited.add(w)
                    queue.append((w, depth + 1))
    return 0


def ladder_length_v2(beginWord, endWord, wordList):
    """ Bidirectional BFS.
        We can considerably cut down the search space of the standard breadth first search algorithm if we launch two
        simultaneous BFS. One from the beginWord and one from the endWord. We progress one node at a time from both
        sides and at any point in time if we find a common node in both the searches, we stop the search. This is known
        as bidirectional BFS and it considerably cuts down on the search space and hence reduces the time and space
        complexity.
        The algorithm is very similar to the standard BFS based approach we saw earlier. The only difference is we now
        do BFS starting two nodes instead of one. This also changes the termination condition of our search.
        We now have two 'visited' dictionaries to keep track of nodes visited from the search starting at the
        respective ends. If we ever find a node/word which is in the 'visited' set of the parallel search, we terminate
        our search, since we have found the meet point of this bidirectional search.
        Termination condition for bidirectional search is finding a word which has already been seen by the parallel
        search. It's more like meeting in the middle instead of going all the way through.
        The shortest transformation sequence is the sum of levels of the meet point node from both the ends. Thus, for
        every visited node we save its level as value in the 'visited' dictionary.
    Time complexity: O(N * M), where N is the number of words and M is the length of each word (same length)
    Space complexity: O(N * M)
    """

    def visit_word(queue, visited, others_visited):
        word, depth = queue.popleft()
        for i in range(len(word)):
            t = word[:i] + '*' + word[i + 1:]
            for w in transformations[t]:
                if w in others_visited:  # If the intermediate state/word has already been visited from the other
                    # parallel traversal this means we have found the answer.
                    return depth + others_visited[w]
                if w not in visited:
                    visited[w] = depth + 1
                    queue.append((w, depth + 1))
        return None

    if endWord not in wordList:
        return 0
    queue_begin = deque([(beginWord, 1)])
    queue_end = deque([(endWord, 1)])
    transformations = defaultdict(list)
    for word in wordList:
        for i in range(len(word)):
            transformations[word[:i] + '*' + word[i + 1:]].append(word)
    visited_begin = {beginWord: 1}
    visited_end = {endWord: 1}
    while queue_begin and queue_end:  # We do a bidirectional search starting one pointer from begin word and one
        # pointer from end word. Hopping one by one.
        res = visit_word(queue_begin, visited_begin, visited_end)  # One hop from begin word
        if res:
            return res
        res = visit_word(queue_end, visited_end, visited_begin)  # One hop from end word
        if res:
            return res
    return 0


class Test(unittest.TestCase):
    data = [('hit', 'cog', ['hot', 'dot', 'dog', 'lot', 'log', 'cog'], 5),
            ('hit', 'cog', ['hot', 'dot', 'dog', 'lot', 'log'], 0)]

    def test_ladder_length(self):
        for test_begin_word, test_end_word, test_word_list, result in self.data:
            self.assertEqual(result, ladder_length_v1(test_begin_word, test_end_word, test_word_list))
            self.assertEqual(result, ladder_length_v2(test_begin_word, test_end_word, test_word_list))


if __name__ == '__main__':
    unittest.main()
