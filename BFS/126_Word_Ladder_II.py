""" A transformation sequence from word beginWord to word endWord using a dictionary wordList is a sequence of words
beginWord -> s1 -> s2 -> ... -> sk such that:

Every adjacent pair of words differs by a single letter.
Every si for 1 <= i <= k is in wordList. Note that beginWord does not need to be in wordList.
sk == endWord

Given two words, beginWord and endWord, and a dictionary wordList, return all the shortest transformation sequences
from beginWord to endWord, or an empty list if no such sequence exists. Each sequence should be returned as a list of
the words [beginWord, s1, s2, ..., sk]. """

import string
from collections import deque


def findLadders(begin_word, end_word, word_list):
    """ This problem is an extension of the problem 127- Word Ladder, where we only need to find the minimum number of
        words in the transformation from beginWord to endWord. Here, we need to find all the transformations that exist
        between beginWord and endWord that are the minimum length. We can use BFS to find the minimum number of words
        in the transformation. However, finding all such transformations is tricky because the number of
        transformations may be enormous.

        The problem can be correlated with the graph data structure. We can represent the words as the vertices and an
        edge can be used to connect two words which differ by a single letter. Now, the task is to find all of the
        shortest paths from beginWord to endWord.

        The naive way to do this is to use backtracking. We will start from beginWord, then traverse all the adjacent
        words until we reach the endWord. When we reach the endWord, we can compare the path length and find all the
        paths that have the minimum path length. This method, however, is extremely inefficient because the number of
        paths between two vertices can be enormous.

        Let's try to optimize our approach. Somehow, we need to reduce the number of traversed paths. Let's say the
        number of shortest paths that exist between beginWord and endWord is x and the number of paths that we must
        traverse to find these shortest paths is y. The closer the value y gets to the value x, the more efficient our
        approach will be.

        If we draw the graph that represents the connectivity among words, we can notice that while backtracking on
        this graph, we will also cover the edges upwards from words already explored. The key observation here is that
        going back in the upward direction will never lead us to the shortest path. We should always traverse the edges
        in the direction of beginWord to endWord.

        Think of the previous graph as a bunch of layers and observe that once we reach a particular layer we don't
        want the future words to have the connection back to this layer. We will build our DAG using BFS. We will then
        add all the directed edges (intermediate words) from the words present in the current layer, and once all words
        in this layer have been traversed, we will remove them from the wordList. This way we will avoid adding any
        edges that point towards beginWord.

        Note that in the graph all paths between beginWord and endWord obtained through BFS will be the shortest
        possible. This is because all the edges in the graph will be directed in the direction of beginWord to endWord.
        Furthermore, there will not be any edge between the words that are on the same level. Therefore, iterating over
        any edge will bring us one step closer to the endWord, thus there is no need to compare the length of the paths
        each time we reach the endWord.

        Store the words present in wordList in an unordered set so that the words can be efficiently removed during
        the breadth-first search.

        Perform the BFS and once a level is finished remove the visited words from the wordList.

        Start from beginWord and while keeping track of the current path as cur_path traverse all the possible paths,
        and whenever the path leads to the endWord store the path in the final result list.

    Time complexity:
    Space complexity:
    """
    word_list = set(word_list)
    res = []
    queue = deque([[begin_word]])
    visited = set()
    while queue:
        size = len(queue)
        for _ in range(size):
            cur_path = queue.popleft()
            word = cur_path[-1]
            n = len(word)
            for i in range(n):
                for c in string.ascii_lowercase:
                    intermediate_word = word[:i] + c + word[i + 1:]
                    if intermediate_word in word_list:
                        new_path = cur_path[:]  # Path will be reused in the loop so copy it into a new path
                        new_path.append(intermediate_word)
                        visited.add(intermediate_word)
                        if intermediate_word == end_word:
                            res.append(new_path)
                        else:
                            queue.append(new_path)
        # 'visited' records all the visited nodes on this level. These words will never be visited again after this
        # level and should be removed from words list.
        for word in visited:
            word_list.discard(word)
    return res
