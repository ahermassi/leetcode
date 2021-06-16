""" Design a data structure that supports the following two operations:
void addWord(word)
bool search(word)
search(word) can search a literal word or a regular expression string containing only letters a-z or .. A . means it
can represent any one letter. """

import unittest2 as unittest


class TrieNode:
    def __init__(self):
        self.children = {}
        self.end_of_word = False


class WordDictionaryV1(object):
    """ Use a trie to store the words, and backtracking to check each character of word to search.
    """

    def __init__(self):
        """
        Initialize your data structure here.
        """
        self.root = TrieNode()

    def addWord(self, word):
        """ Adds a word into the data structure.
        Time complexity: O(M), where M is the length of word
        Space complexity: O(M) in the worst case where the newly inserted word doesn't share a prefix with the the
        words already inserted in the trie. We have to add M new nodes.
        """
        root = self.root
        for c in word:
            if c not in root.children:
                root.children[c] = TrieNode()
            root = root.children[c]
        root.end_of_word = True

    def search(self, word):
        """ Returns if the word is in the data structure. A word could contain the dot character '.' to represent
            any one letter.
            The function tries to find a suffix of the string that starts at 'index'. If the value of one of the
            children of the current trie node is equal to the character at current 'index', we recursively try to find
            the rest of the string starting at ('index' + 1), and the exploration starts from that child.
            If the first character of the suffix is the wildcard '.', then all the children of the current trie node
            are good candidates to hold the rest of the string. If any of the children returns a positive result,
            we win.
        Time complexity: O(M) if we exclude wildcards (.), worst case search will iterate through the longest word
        (i.e. linear to the maximum number of characters in a word). With wildcards, it will iterate through the whole
        tree in the worst case (i.e. linear to the total number of characters), which is O(26^M) when we have an
        undefined word '.....' whose length is M, as the branching factor is 26 and the depth is M. Each key could
        have 26 chars, and for M length of searched word we need to search 26^M with all keys.
        Suppose the word is '...z'; It would be O(26^M) where M is the length of the word; At each node due to dot
        we search in 26 more branches until we find the match.
        """

        def dfs(root, index):
            if index == n:
                return root.end_of_word
            c = word[index]
            if c == '.':
                # Can we find the REST of the string in any of the children ?
                return any(dfs(child, index + 1) for child in root.children.values())
            if c not in root.children:
                return False
            return dfs(root.children[c], index + 1)  # Start of the prefix was found, so keep following that path

        n, root = len(word), self.root
        return dfs(root, 0)


class WordDictionaryV2(object):
    """ A different implementation using hash map as a trie (nested hash maps). """

    def __init__(self):
        self.trie = dict()

    def addWord(self, word):
        trie = self.trie
        for c in word:
            if c not in trie:  # Add a dictionary for each new character, creating a nested dictionary from word's
                # characters
                trie[c] = dict()
            trie = trie[c]
        trie['#'] = '#'  # Add end of word mark to the dictionary of current node

    def search(self, word):

        def dfs(node, index):
            if index == n:
                # If any word is found there should be an end of word mark in the dictionary of current node
                return '#' in node
            c = word[index]
            if c == '.':
                # Search for any sub-string starting with current character
                # Why exclude '#'? Since '#' is not a 'real' character and only a placeholder (and we know it won't
                # have any children, since the word finished here), we don't want to traverse down this path.
                return any(dfs(node[child], index + 1) for child in node if child != '#')
            if c not in node:
                return False
            return dfs(node[c], index + 1)

        trie = self.trie
        n = len(word)
        return dfs(trie, 0)


class Test(unittest.TestCase):
    word_dictionary = WordDictionaryV1()
    word_dictionary.addWord("bad")
    word_dictionary.addWord("dad")
    word_dictionary.addWord("mad")
    search1 = word_dictionary.search("pad")
    search2 = word_dictionary.search("bad")
    search3 = word_dictionary.search(".ad")
    search4 = word_dictionary.search("b..")

    def test_word_dictionary(self):
        self.assertFalse(self.search1)
        self.assertTrue(self.search2)
        self.assertTrue(self.search3)
        self.assertTrue(self.search4)


if __name__ == '__main__':
    unittest.main()