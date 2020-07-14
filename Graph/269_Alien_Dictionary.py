""" There is a new alien language which uses the latin alphabet. However, the order among letters are unknown to you.
You receive a list of non-empty words from the dictionary, where words are sorted lexicographically by the rules of
this new language. Derive the order of letters in this language. """

from collections import defaultdict, deque
import unittest2 as unittest


def alien_order(words):
    """ Kahn's algorithm for topological sorting.
        A few things to keep in mind:
            - The letters within a word don't tell us anything about the relative order. For example, the presence of
              the word 'kitten' in the list does not tell us that the letter 'k' is before the letter 'i'.
            - The input can contain words followed by their prefix, for example, 'abcd' and then 'ab'. These cases will
              never result in a valid alphabet (because in a valid alphabet, prefixes are always first). We'll need to
              make sure our solution detects these cases correctly.
        All approaches break the problem into three steps:
            1- Extracting dependency rules from the input. For example 'A must be before C', 'X must be before D', or
               'E must be before B'.
            2- Putting the dependency rules into a graph with letters as nodes and dependencies as edges (an adjacency
               list is best).
            3- Topologically sorting the graph nodes
        Remember that in an ordinary English dictionary, all the words starting with 'a' are at the start, followed by
        all the ones starting with 'b', then 'c', 'd', 'e', and at the very end, 'z'. In the alien dictionary, we also
        expect the first letters of each word to be in alphabetical order.
        Going back to the English dictionary analogy, the word 'abacus' will appear before 'algorithm'. This is because
        when the first letter of two words is the same, we instead look at the second letter; 'b' and 'l' in this case.
        'b' is before 'l' in the alphabet.
        Hopefully, we're starting to see a pattern here. Where two words are adjacent, we need to look for the first
        difference between them. That difference tells us the relative order between two letters.
        We now have a set of relations stating how pairs of letters are ordered relative to each other. How could we
        put these together? When we have a set of relations, often drawing a graph is the best way to visualize them.
        The nodes are the letters, and an edge between two letters 'A' and 'B' represents that 'A' is after 'B' in the
        alien alphabet.
        Now, we need to somehow identify which letters have no outcoming links left. With the adjacency list format,
        this is a bit annoying to do, because determining whether or not a particular letter has any outcoming links
        requires repeatedly checking over the adjacency lists of all the other letters to see whether or not they
        feature that letter. However, we can do even better than that. Instead of keeping track of all the other
        letters that must be before a particular letter, we only need to keep track of how many of them there are!
        While building the forward adjacency list, we can also count up how many outcoming edges each letter has.
        We call the number of outcoming edges the out-degree of a node.
        We'll do a BFS for all letters that are reachable, adding each letter to the output as soon as it's reachable.
        A letter is reachable once all of the letters that need to be before it have been added to the output.
        To do a BFS, recall that we use a queue. We should initially put all letters with an out-degree of 0 onto that
        queue. Each time a letter gets down to an out-degree of 0, it is added to the queue.
        We continue this until the queue is empty. After that, we check whether or not all letters were put in the
        output list. If some are missing, this is because we got to a point where all remaining letters had at least
        one edge going out; this means there must be a cycle! In that case, we should return '' as per the problem
        description. Otherwise, we should return the complete ordering we found.
        One edge case we need to be careful of is where a word is followed by its own prefix. In these cases, it is
        impossible to come up with a valid ordering and so we should return ''. The best place to detect it is in the
        loop that compares each adjacent pair of words.
    Time complexity: O(|V| + |E|), https://leetcode.com/articles/alien-dictionary/
    Space complexity: O(|V| + |E|)
    """
    graph, outdegree = defaultdict(set), {c: 0 for word in words for c in word}
    length, res = len(words), []
    for i in range(length - 1):
        cur_word, next_word = words[i], words[i + 1]
        n, m, j, k = len(cur_word), len(next_word), 0, 0
        while j < n and k < m and cur_word[j] == next_word[k]:
            j += 1
            k += 1
        if j < n and k >= m:  # Check that 'next_word' isn't a prefix of 'cur_word'
            return ''
        if j < n and k < m and next_word[k] not in graph[cur_word[j]]:
            graph[cur_word[j]].add(next_word[k])
            outdegree[next_word[k]] += 1
    queue = deque([c for c in outdegree if outdegree[c] == 0])
    if not queue:
        return ''
    while queue:
        node = queue.popleft()
        res.append(node)
        for neighbor in graph[node]:
            outdegree[neighbor] -= 1
            if outdegree[neighbor] == 0:
                queue.append(neighbor)
    return ''.join(res) if len(res) == len(outdegree) else ''  # If not all letters are in output, that means there
    # was a cycle and so no valid ordering. Return '' as per the problem description.


class Test(unittest.TestCase):
    data = [(['wrt', 'wrf', 'er', 'ett', 'rftt'], 'wertf'), (['z', 'x'], 'zx'), (['z', 'x', 'z'], '')]

    def test_alien_order(self):
        for test_words, result in self.data:
            self.assertEqual(result, alien_order(test_words))


if __name__ == '__main__':
    unittest.main()
