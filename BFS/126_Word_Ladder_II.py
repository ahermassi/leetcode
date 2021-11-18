""" A transformation sequence from word beginWord to word endWord using a dictionary wordList is a sequence of words
beginWord -> s1 -> s2 -> ... -> sk such that:

Every adjacent pair of words differs by a single letter.
Every si for 1 <= i <= k is in wordList. Note that beginWord does not need to be in wordList.
sk == endWord

Given two words, beginWord and endWord, and a dictionary wordList, return all the shortest transformation sequences
from beginWord to endWord, or an empty list if no such sequence exists. Each sequence should be returned as a list of
the words [beginWord, s1, s2, ..., sk]. """

import string
from collections import deque, defaultdict


def findLadders_v1(begin_word, end_word, word_list):
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

        Perform the BFS and once a level is finished remove the next_queue words from the wordList.

        Start from beginWord and while keeping track of the current path as cur_path traverse all the possible paths,
        and whenever the path leads to the endWord store the path in the final result list.

    Time complexity:
    Space complexity:
    """
    word_list = set(word_list)
    res = []
    queue = deque([[begin_word]])
    next_queue = set()
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
                        next_queue.add(intermediate_word)
                        if intermediate_word == end_word:
                            res.append(new_path)
                        else:
                            queue.append(new_path)
        # 'next_queue' records all the next_queue nodes on this level. These words will never be next_queue again after this
        # level and should be removed from words list.
        for word in next_queue:
            word_list.discard(word)
    return res


def findLadders_v2(begin_word, end_word, word_list):
    """ BFS + DFS.

        The basic idea is to:
        Use BFS to find the shortest distance between start and end, storing node's next level neighbors in a hash map.
        Use DFS to output the shortest transformation paths.

        We need to build a search tree during BFS and backtrack along that tree to restore all shortest paths.
        We can't stop BFS once we found a transformed word is equal to end word but we should instead finish searching
        in the current BFS layer since there could be more than one shortest path.

        We still need to rule out all nodes that we have searched previously. This helps avoid add edges connecting to
        strings from the previous level (e.g avoid any back-track path). Meanwhile, if two nodes have the same child
        node, we need to add that child node to both node's children/neighbors list as we need to backtrack all valid
        paths. So unlike a regular BFS, we can't use a "next_queue" set but more like an "explored" set. Otherwise,
        e.g. neighbors: {x->z, y->z}, z won't be added to y's children list if x is next_queue first and z is already seen
        in x's search.

        Example:
        neighbors =   {
                'hit': ['hot'],
                'hot': ['dot', 'lot'],
                'dot': ['dog'],
                'lot': ['log'],
                'log': ['cog'],
                'dog': ['cog']
                }


        1. build_paths_from(hit) -> [hit] + build_paths_from(hot) -> [hit, hot, dot, dog, cog], [hit, hot, lot, log, cog]

            2. build_paths_from(hot) -> [hot] + build_paths_from(dot), [hot] + build_paths_from(lot) -> [hot, dot, dog, cog], [hot, lot, log, cog]

                3. build_paths_from(dot) -> [dot] + build_paths_from(dog) -> [dot, dog, cog]

                    4. build_paths_from(dog) -> [dog] + build_paths_from(cog) -> [dog, cog]

                        5. build_paths_from(cog) -> [cog]

                3. build_paths_from(lot) -> [lot, log, cog]

                    4. build_paths_from(log) -> [log, cog]

                        5. build_paths_from(cog) -> [cog]

    Time complexity:
    Space complexity:
    """

    def build_paths_from(word):
        if word == end_word:
            return [[word]]
        res = []
        for neighbor in neighbors[word]:
            rest = build_paths_from(neighbor)
            for lst in rest:
                # Add 'word' in front of all of its children nodes’ paths
                res.append([word] + lst)
        return res

    word_list = set(word_list)
    queue, next_queue = {begin_word}, set()
    neighbors = defaultdict(list)
    end_word_found = False
    while queue:
        word_list -= set(queue)  # Discard words in current level so that they won't be used again
        for word in queue:
            n = len(word)
            for i in range(n):
                for c in string.ascii_lowercase:
                    intermediate_word = word[:i] + c + word[i + 1:]
                    if intermediate_word in word_list:
                        neighbors[word].append(intermediate_word)
                        if intermediate_word == end_word:
                            end_word_found = True
                        else:
                            next_queue.add(intermediate_word)
        # After this level (let's say L(n-1)) we are reaching end. So even if we are reaching end from some other level
        # (let's say L(n)), then distance from L(n) will be grater than L(n-1) because L(n) is further down, as we are
        # doing a level-by-level exploration.
        if end_word_found:
            break
        queue, next_queue = next_queue, set()
    return build_paths_from(begin_word)


def findLadders_v3(begin_word, end_word, word_list):
    """ Bi-Directional BFS + DFS.

        This approach is very similar to the previous one in that both approaches will use the same Directed Acyclic
        Graph (DAG). The difference lies in the way that the graph is produced, which is better optimized in this case.

        In the previous solution, we performed BFS starting from beginWord and explored down the ladder until we
        reached endWord. However, now we will start from beginWord stored in begin_queue and from endWord stored in
        end_queue and explore towards the middle of the ladder. At each iteration, we will connect the words to their
        neighbors.

        At each iteration, we will have two options, either to connect edges using the begin_queue or by using the
        end_queue. The optimal choice is to use the queue that contains fewer words. In this solution, for simplicity,
        we will swap begin_queue and end_queue whenever begin_queue is larger. In doing so, we will always choose the
        begin_queue.

        We will traverse the begin_queue and find the neighbors of each of the words present. We will also store the
        next layer words in the next_queue list. Once a level is finished, we can assign the begin_queue to next_queue.
        We will repeat this process until either the size of begin_queue becomes zero, signifying that there is no
        valid sequence from beginWord to endWord, or until the contents of begin_queue and end_queue overlap.

        The reason for stopping when begin_queue and end_queue overlap is because after completing this level, it is
        guaranteed that beginWord and endWord will be connected by at least one sequence that that passes through the
        words that exist in both queues. Thus, the DAG will be completed.

        The remaining process is the same as the previous approach: Once the queue has been traversed, at each
        iteration, we will remove those words from the wordList to avoid including any edges to previous layers. Once
        the graph is complete, we will use backtracking to find all of the paths between beginWord and endWord.

        Store the words present in wordList in an unordered set so that the words can be efficiently removed during
        the breadth-first search.
        Perform a bidirectional BFS. Initialize two queues, begin_queue with beginWord and end_queue with endWord.
        At each iteration, add the edges to the adjacency list by extending the shorter queue.
        The parameter 'direction' is used to decide in which direction the edges should be connected, where 1 indicates
        towards endWord (down the ladder) and vice versa.
        If a sequence connecting beginWord to endWord does not exist, return an empty list. Otherwise, start from
        beginWord and while keeping track of the current path traverse all the possible paths, whenever the path leads
        to the endWord store the path in the result list.

    Time complexity:
    Space complexity:
    """

    def build_paths_from(word):
        if word == end_word:
            return [[word]]
        res = []
        for neighbor in neighbors[word]:
            rest = build_paths_from(neighbor)
            for lst in rest:
                res.append([word] + lst)
        return res

    if end_word not in word_list:
        return []
    word_list = set(word_list)
    begin_queue, end_queue = {begin_word}, {end_word}
    next_queue = set()
    neighbors = defaultdict(list)
    end_word_found = False
    direction = 1
    while begin_queue:
        word_list -= set(begin_queue)
        for word in begin_queue:
            n = len(word)
            for i in range(n):
                for c in string.ascii_lowercase:
                    intermediate_word = word[:i] + c + word[i + 1:]
                    if intermediate_word in word_list:
                        neighbors[word].append(intermediate_word) if not direction == 1 else neighbors[intermediate_word].append(word)
                        if intermediate_word in end_queue:
                            end_word_found = True
                        else:
                            next_queue.add(intermediate_word)
        if end_word_found:
            break
        begin_queue, next_queue = next_queue, set()
        if len(end_queue) < len(begin_queue):
            begin_queue, end_queue = end_queue, begin_queue
            direction = -direction
    return build_paths_from(begin_word)
