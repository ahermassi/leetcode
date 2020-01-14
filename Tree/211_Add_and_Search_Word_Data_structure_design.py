""" Design a data structure that supports the following two operations:
void addWord(word)
bool search(word)
search(word) can search a literal word or a regular expression string containing only letters a-z or .. A . means it
can represent any one letter. """

import unittest2 as unittest


class TrieNode:
    def __init__(self):
        self.children = {}
        self.is_word = False


class WordDictionary(object):
    """ Use a trie to store the words, and backtracking to check each character of word to search.
    Time complexity:
        addWord: O(k), where k is the length of word (worst case if the word is new)
        search: if we exclude wildcards (.), worst case search will iterate through the longest word (i.e. linear to
        the maximum number of characters in a word). With wildcards, it will iterate through the whole tree in the
        worst case (i.e. linear to the total number of characters)
    Space complexity:
        addWord: O(k), in the worst case newly inserted word doesn't share a prefix with the the words already
        inserted in the trie. We have to add k new nodes
        search: O(k) if we exclude wildcards, O(N) (i.e. linear to the total number of characters) in the worst case
        when there are wildcards.
    """

    def __init__(self):
        """
        Initialize your data structure here.
        """
        self.root = TrieNode()

    def addWord(self, word):
        """
        Adds a word into the data structure.
        :type word: str
        :rtype: None
        """
        root = self.root
        for c in word:
            if c not in root.children:
                root.children[c] = TrieNode()
            root = root.children[c]
        root.is_word = True

    def search(self, word):
        """
        Returns if the word is in the data structure. A word could contain the dot character '.' to represent any one
        letter.
        The function tries to find a suffix of the string that starts at 'index'. If the value of one of the children
        of the current trie node is equal to the character at current 'index', we recursively try to find the rest of
        the string starting at ('index' + 1), and the exploration starts from that child.
        If the first character of the suffix is the wildcard '.', then all the children of the current trie node are
        good candidates to hold the rest of the string. If any of the children returns a positive result, we win.
        :type word: str
        :rtype: bool
        """

        def dfs(root, index):
            if index == n:
                return root.is_word
            c = word[index]
            if c != '.':
                return c in root.children and dfs(root.children[c], index + 1)  # Start of the prefix was found, so
                # keep following that path
            for child in root.children.values():  # Can we find the REST of the string in any of the children ?
                if dfs(child, index + 1):
                    return True
            return False

        n, root = len(word), self.root
        return dfs(root, 0)


class Test(unittest.TestCase):
    word_dictionary = WordDictionary()
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