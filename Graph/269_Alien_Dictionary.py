""" There is a new alien language which uses the latin alphabet. However, the order among letters are unknown to you.
You receive a list of non-empty words from the dictionary, where words are sorted lexicographically by the rules of
this new language. Derive the order of letters in this language. """

from collections import defaultdict, deque
import unittest2 as unittest


def alien_order_v1(words):
    """ Kahn's algorithm for topological sorting.

         A few things to keep in mind:

            - The letters within a word don't tell us anything about the relative order. For example, the presence of
               the word 'kitten' in the list does not tell us that the letter 'k' is before the letter 'i'.

            - The input can contain words followed by their prefix, for example, 'abcd' and then 'ab'. These cases will
               never result in a valid alphabet (because in a valid alphabet, prefixes are always first). We'll need to
               make sure the solution detects these cases correctly.

            - There can be more than one valid alphabet ordering. It is fine for the algorithm to return anyone of them.

            - The output string must contain all unique letters that were within the input list, including those that
               could be in any position within the ordering. It should not contain any additional letters that were not
               in the input.

        All approaches break the problem into three steps:

            1- Extract dependency rules from the input. For example 'A must be before C', 'X must be before D', or
                 'E must be before B'.

            2- Put the dependency rules into a graph with letters as nodes and dependencies as edges (an adjacency list
                 is best).

            3- Topologically sort the graph nodes

        Remember that in an ordinary English dictionary, all the words starting with 'a' are at the start, followed by
        all the ones starting with 'b', then 'c', 'd', 'e', and at the very end, 'z'. In the alien dictionary, we also
        expect the first letters of each word to be in alphabetical order.

        Going back to the English dictionary analogy, the word 'abacus' will appear before 'algorithm'. This is because
        when the first letter of two words is the same, we instead look at the second letter; 'b' and 'l' in this case.
        'b' is before 'l' in the alphabet.

        Let's take a closer look at the first two words of an "alien dictionary"; ''wxqkj' and 'whgg'. Seeing as the
        first letters are the same, 'w', we look at the second letters. The first word has 'x', and the second word has
        'h'. Therefore, we know that 'x' is before 'h' in this alien dictionary.

        Hopefully, we're starting to see a pattern here. When two words are adjacent, we need to look for the first
        difference between them. That difference tells us the relative order between two letters.

        We now have a set of relations stating how pairs of letters are ordered relative to each other. How could we
        put these together? When we have a set of relations, often drawing a graph is the best way to visualize them.
        The nodes are the letters, and an edge between two letters 'A' and 'B' represents that 'A' is before 'B' in the
        alien alphabet, or 'A' is a prerequisite of 'B' (similar to 207- Course Schedule).

        Some letters will have no arrows going into them. What this means is that there are no letters that have to be
        before any of these. We need to somehow identify which letters have no incoming links left. With the adjacency
        list format, this is a bit annoying to do, because determining whether a particular letter has any incoming
        links requires repeatedly checking over the adjacency lists of all the other letters to see whether they feature
        that letter.

        However, we can do better than that. Instead of keeping track of all the other letters that must be before a
        particular letter, we only need to keep track of how many of them there are. While building the adjacency list,
        we can also count up how many incoming edges each letter has. We call the number of incoming edges the
        indegree of a node.

        Therefore, when a character has a 'prerequisite' extracted, we can simply decrement its count by 1. Once the
        count reaches 0, this is equivalent to there being no incoming edges left.

        We'll do a BFS for all letters that are reachable, adding each letter to the output as soon as it's reachable.
        A letter is reachable once all the letters that need to be before it have been added to the output.

        To do a BFS, recall that we use a queue. We should initially put all letters with an indegree of 0 into that
        queue. Each time a letter gets down to an indegree of 0, it is added to the queue.

        We continue this until the queue is empty. After that, we check whether all letters were put in the output list.
        If some are missing, this is because we got to a point where all remaining letters had at least one edge going
        in; this means there must be a cycle! In that case, we should return '' as per the problem description.
        Otherwise, we should return the complete ordering we found.

        One edge case we need to be careful of is where a word is followed by its own prefix. In these cases, it is
        impossible to come up with a valid ordering, and so we should return ''. The best place to detect it is in the
        loop that compares each adjacent pair of words.

    Time complexity: O(|V| + |E|), https://leetcode.com/articles/alien-dictionary/
    Space complexity: O(|V| + |E|)
    """
    n = len(words)
    graph = defaultdict(set)
    indegree = {c: 0 for word in words for c in word}
    for i in range(n - 1):
        cur_word, next_word = words[i], words[i + 1]
        min_len = min(len(cur_word), len(next_word))
        # We can check if 'next_word' is a prefix of 'cur_word' before starting the while loop:
        # if len(cur_word) > len(next_word) and cur_word.startswith(next_word):
        #     return ''
        j = 0
        while j < min_len and cur_word[j] == next_word[j]:
            j += 1
        if j == min_len and len(cur_word) > len(next_word):  # Check that next_word isn't a prefix of cur_word
            return ''
        # Even though the adjacency lists are hash sets, we have to check that we're not processing the same edge
        # more than once as it would result in a wrong indegree value
        if j < min_len and next_word[j] not in graph[cur_word[j]]:
            # Create graph, better thought of as is_prerequisite_of graph: graph[char1] = char2 means 'char1' is a
            # prerequisite of 'char2' and precedes it in the alien alphabet
            graph[cur_word[j]].add(next_word[j])
            indegree[next_word[j]] += 1  # Record the number of 'prerequisites' each character has
    queue = deque(c for c in indegree if indegree[c] == 0)
    res = []
    # Iterate over the indegree list and find the nodes that have an indegree of 0, which maps to 0 'prerequisites'.
    # If none is found, then there must be a cycle and a topological ordering is not possible.
    while queue:
        vertex = queue.popleft()
        res.append(vertex)
        for neighbor in graph[vertex]:
            indegree[neighbor] -= 1
            if indegree[neighbor] == 0:
                queue.append(neighbor)
    # If not all letters are in the output, that means there was a cycle and so no valid ordering. Return ''.
    return ''.join(res) if len(res) == len(indegree) else ''


# Video explanation: https://www.youtube.com/watch?v=6kTZYvNNyps
def alien_order_v2(words):
    """ Another approach is to use a depth-first search. We still need to extract relations and then generate an
         adjacency list in the same way as before, but this time we don't need the indegree map.

         Recall that in a depth-first search, nodes are returned once they either have no outgoing links left, or all
         their outgoing links have been visited. Therefore, the order in which nodes are returned by the depth-first
         search will be the reverse of a valid alphabet order.

         One issue we need to be careful of is cycles. In directed graphs, we often detect cycles by using graph
         coloring. All nodes start as white, and then once they're first visited they become grey, and then once all
         their outgoing nodes have been fully explored, they become black. We know there is a cycle if we enter a node
         that is currently grey. It works because all nodes that are currently on the stack are grey. Nodes are changed
         to black when they are removed from the stack.

         The way DFS would work is that we would consider all possible paths stemming from A before finishing up the
         recursion for A and moving onto other nodes. All the nodes in the paths stemming from the node A would have A
         as an ancestor. The way this fits in our problem is, all the characters in the paths stemming from character
         A would have A as a 'prerequisite'.

         For each of the nodes in our graph, we will run a depth-first search in case that node was not already visited
         in some other node's DFS traversal.

         Suppose we are executing the depth-first search for a node N. We will recursively traverse all the neighbors of
         node N which have not been processed before. Once the processing of all the neighbors is done, we will add the
         node N to the result list.

         visited[node] == 0 means this node is part of the current trip, and either all of its descendants are not
         processed or it's still in the function call stack. If we see it again, it's a cycle.
         visited[node] == 1: means the node and all its descendants were processed, and no cycle was found. if we hit
         this, going down this path won't find any cycles.

        Another way to think about it is the last few in the order must be those which are not prerequisites of other
        characters. Thinking of it recursively means if one node has unvisited children nodes, we should visit them
        first before we put this node down in the final order list. This sounds like the postorder DFS.

        An important thing to note about topologically sorted order is that there won't be just one ordering of nodes
        (characters). There can be multiple.

    Time complexity: O(|V| + |E|), where V is the number of vertices and E is the number of edges. Essentially we
    iterate through each node and each vertex in the graph once and only once.
    Space complexity: O(|V| + |E|), we use the adjacency list to represent our graph initially. The space occupied is
    defined by the number of edges because for each node as the key, we have all its adjacent nodes in the form of a
    list as the value.
    """

    def dfs(vertex):
        if visited[vertex] == 0:  # Don't recurse further if a cycle was already found
            return False
        if visited[vertex] == 1:
            return True
        visited[vertex] = 0  # Start the recursion
        for neighbor in graph[vertex]:
            if not dfs(neighbor):
                return False
        res.append(vertex)
        visited[vertex] = 1
        return True

    n = len(words)
    graph = defaultdict(list)
    for i in range(n - 1):
        cur_word, next_word = words[i], words[i + 1]
        min_len = min(len(cur_word), len(next_word))
        j = 0
        while j < min_len and cur_word[j] == next_word[j]:
            j += 1
        if j == min_len and len(cur_word) > len(next_word):
            return ''
        if j < min_len and next_word[j] not in graph[cur_word[j]]:
            # Create graph, better thought of as is_prerequisite_of graph: graph[char1] = char2 means 'char1' is a
            # prerequisite of 'char2' and precedes it in the alien alphabet
            graph[cur_word[j]].append(next_word[j])
    visited = {c: -1 for word in words for c in word}
    res = []
    for c in visited:
        if not dfs(c):
            # If a cycle exists, no topological ordering is possible
            return ''
    return ''.join(res[::-1])


class Test(unittest.TestCase):
    data = [(['wrt', 'wrf', 'er', 'ett', 'rftt'], 'wertf'), (['z', 'x'], 'zx'), (['z', 'x', 'z'], '')]

    def test_alien_order(self):
        for test_words, result in self.data:
            self.assertEqual(result, alien_order_v1(test_words))
            self.assertEqual(result, alien_order_v2(test_words))


if __name__ == '__main__':
    unittest.main()
