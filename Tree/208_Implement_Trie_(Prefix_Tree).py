""" Implement a trie with insert, search, and startsWith methods. """

import unittest as unittest


class TrieNode:
    def __init__(self):
        self.children = dict()
        self.end_of_word = False


class Trie(object):
    """ Do yourself a favor and checkout this article: https://leetcode.com/articles/implement-trie-prefix-tree/
    Time complexity:
        insert(word): O(k) where k is the length of word
        search(word): O(k)
        startsWith(prefix):
    Space complexity:
        insert(word): O(k), in the worst case newly inserted key doesn't share a prefix with the the keys already
        inserted in the trie. We have to add k new nodes
        search(word): O(1)
        startsWith(prefix): O(1)
    """

    def __init__(self):
        """
        Initialize your data structure here.
        """
        self.root = TrieNode()

    def insert(self, word):
        """
        Inserts a word into the trie.
        :type word: str
        :rtype: None
        """
        root = self.root
        for c in word:
            if c not in root.children:
                root.children[c] = TrieNode()
            root = root.children[c]  # By doing this we traverse down the tree.. so the root is reassigned to its
            # child.. and so on.. so we are progressively following the child till we reach the end of word
        root.end_of_word = True

    def search(self, word):
        """
        Returns if the word is in the trie.
        :type word: str
        :rtype: bool
        """
        root = self.root
        for c in word:
            if c not in root.children:
                return False
            root = root.children[c]
        return root.end_of_word

    def startsWith(self, prefix):
        """
        Returns if there is any word in the trie that starts with the given prefix.
        :type prefix: str
        :rtype: bool
        """
        root = self.root
        for c in prefix:
            if c not in root.children:
                return False
            root = root.children[c]
        return True


class Test(unittest.TestCase):
    trie = Trie()
    trie.insert("apple")
    search1 = trie.search("apple")
    search2 = trie.search("app")
    search3 = trie.startsWith("app")
    trie.insert("app")
    search4 = trie.search("app")

    def test_trie(self):
        self.assertTrue(self.search1)
        self.assertFalse(self.search2)
        self.assertTrue(self.search3)
        self.assertTrue(self.search4)


if __name__ == '__main__':
    unittest.main()