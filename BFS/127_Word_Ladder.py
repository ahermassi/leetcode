""" Given two words (begin_word and end_word), and a dictionary's word list, find the length of shortest transformation
sequence from begin_word to end_word, such that:
Only one letter can be changed at a time.
Each transformed word must exist in the word list. Note that begin_word is not a transformed word. """

import string
from collections import deque, defaultdict
import unittest2 as unittest

# For both solutions, check out this article: https://leetcode.com/articles/word-ladder/


def ladder_length_v1(begin_word, end_word, word_list):
    """ We are given a begin_word and an end_word. Let these two represent start node and end node of a graph. We have
        to reach from the start node to the end node using some intermediate nodes/words. The intermediate nodes are
        determined by the word_list given to us. The only condition for every step we take on this ladder of words is
        the current word should change by just one letter.

        We will essentially be working with an undirected and unweighted graph with words as nodes and edges between
        words which differ by just one letter. The problem boils down to finding the shortest path from a start node to
        a destination node, if there exists one. Hence it can be solved using Breadth First Search approach.

        One of the most important steps here is to figure out how to find adjacent nodes i.e. words which differ
        by one letter. To efficiently find the neighboring nodes for any given word, we do some pre-processing on the
        words of the given word_list. The pre-processing involves replacing the letter of a word by a non-alphabet, say,
        *. This pre-processing helps to form generic states to represent a single letter change:

                    Dog ----> D*g <---- Dig

        Both 'Dog' and 'Dig' map to the same intermediate or generic state 'D*g'.

        Save these intermediate states in a dictionary with key as the intermediate word and value as the list of words
        which have the same intermediate word.
        The pre-processing step helps us find out the generic one letter away nodes for any word of the word list and
        hence making it easier and quicker to get the adjacent nodes. Otherwise, for every word we will have to iterate
        over the entire word list and find words that differ by one letter. That would take a lot of time. This
        pre-processing step essentially builds the adjacency list first before beginning the breadth first search
        algorithm.

        For eg. While doing BFS if we have to find the adjacent nodes for 'Dug' we can first find all the generic
        states for 'Dug':

        Dug => *ug
        Dug => D*g
        Dug => Du*

        The second transformation 'D*g' could then be mapped to 'Dog' or 'Dig', since all of them share the same
        generic state. Having a common generic transformation means two words are connected and differ by one letter.

        Start from begin_word and search the end_word using BFS. Find all the generic transformations of the
        current word and find out if any of these transformations is also a transformation of other words in the word
        list. This is achieved by checking the hash map. The list of words we get from the map are all the words which
        have a common intermediate state with the current word. This new set of words will be the adjacent nodes/words
        to current word and hence added to the queue.

        To prevent cycles, use a 'visited' set. Eventually, if we reach the desired word, its level would represent
        the shortest transformation sequence length.

        Example:
        wordList = ["hot","dot","dog","lot","log","cog"]
        intermediate_words = { *ot : hot, dot, lot
			                   h*t : hot
			                   ho* :hot
			                   d*t : dot
			                   do* : dot, dog
			                   *og : dog, log, cog
			                   d*g : dog
			                   l*t : lot
			                   lo* : lot, log
			                   l*g : log
			                   c*g: cog
			                   co* : cog
			                }
			                            hit, level = 1
								 /            |              \
					     *it                h*t                  hi*
						   |                 |                     |
			             null  	       hot ,level = 2             null
										 /   |   \
										/    |     \
				               *ot           h*t      ho*
				           /    |   \         |        |
                     hot,2   dot,3  lot,3   hot,2    hot,2

    Time complexity: O(N * M), where M is the length of words (all words have same length) and N is the total number of
    words in the input word list. Finding out all the transformations takes M iterations for each of the N words.
    Also, breadth-first search in the worst case might go to each of the N words.
    Space complexity: O(N * M), to store all M transformations for each of the N words, in the 'transformations'
    dictionary, 'visited' set is of size N, queue for BFS in worst case would need space for all N words.
    """
    word_list = set(word_list)
    if end_word not in word_list:
        return 0
    intermediate_words = defaultdict(list)  # Dictionary to hold patterns of words that can be formed, from any given
    # word, by changing one letter at a time.
    for word in word_list:
        for i in range(len(word)):
            intermediate_words[word[:i] + '*' + word[i + 1:]].append(word)
    queue = deque([(begin_word, 1)])
    visited = set()  # Visited to make sure we don't repeat processing the same word
    while queue:
        word, distance = queue.popleft()
        if word == end_word:  # We found the end word
            return distance
        n = len(word)
        for i in range(n):
            pattern = word[:i] + '*' + word[i + 1:]
            for w in intermediate_words[pattern]:  # The words which share the same intermediate state/pattern
                if w not in visited:
                    # Add to visited. There is no reason to wait to mark nodes as visited. Because this is a BFS, once
                    # a node has been seen that is the EARLIEST it could have possibly been seen so any other path to
                    # that node would either be longer or the same length as what we've already observed.
                    visited.add(w)
                    queue.append((w, distance + 1))
    return 0


def ladder_length_v2(begin_word, end_word, word_list):
    """ Same unidirectional BFS approach. However, instead of pre-processing the list of words to build the graph's
        adjacency list, we do it on the fly while processing the intermediate words in the queue. With a current word
        at hand, we try all the possible on-letter modifications of that word. If a modification results in an
        intermediate word that exists in the input list of words, we add it to the queue AND remove it from word_list.
        The shortest path will be the first one to delete 'end_word' from the dictionary. BFS will give the shortest
        path by the way it proceeds.
    """
    word_list = set(word_list)
    queue = deque([(begin_word, 1)])
    while queue:
        word, distance = queue.popleft()
        if word == end_word:
            return distance
        n = len(word)
        for i in range(n):
            for c in string.ascii_lowercase:
                intermediate_word = word[:i] + c + word[i + 1:]
                if intermediate_word in word_list:
                    queue.append((intermediate_word, distance + 1))
                    word_list.remove(intermediate_word)
    return 0


def ladder_length_v3(begin_word, end_word, word_list):
    """ Bidirectional BFS.
        We can considerably cut down the search space of the standard breadth first search algorithm if we launch two
        simultaneous BFS. One from the begin_word and one from the end_word. We progress one node at a time from both
        sides. At any point in time, if we find a common node in both the searches, we stop the search. This is known
        as bidirectional BFS and it considerably cuts down on the search space and hence reduces the time and space
        complexity.
        The motivation is that b^(d/2) + b^(d/2) is much less than b^d, where b is branch factor and d is depth.
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

    def visit_word(queue, visited, other_visited):
        word, depth = queue.popleft()
        n = len(word)
        for i in range(n):
            pattern = word[:i] + '*' + word[i + 1:]
            for w in transformations[pattern]:
                if w in other_visited:  # If the intermediate state/word has already been visited from the other
                    # parallel traversal, this means we have found the answer.
                    return depth + other_visited[w]
                if w not in visited:
                    queue.append((w, depth + 1))
                    visited[w] = depth + 1
        return None

    word_list = set(word_list)
    if end_word not in word_list:
        return 0
    transformations = defaultdict(list)
    for word in word_list:
        for i in range(len(word)):
            transformations[word[:i] + '*' + word[i + 1:]].append(word)
    queue_begin = deque([(begin_word, 1)])
    queue_end = deque([(end_word, 1)])
    visited_begin, visited_end = {begin_word: 1}, {end_word: 1}
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
