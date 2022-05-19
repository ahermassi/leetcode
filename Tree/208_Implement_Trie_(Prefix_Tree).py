""" Implement a trie with insert, search, and startsWith methods. """

import unittest as unittest
from collections import defaultdict

# Video explanation: https://www.youtube.com/watch?v=oobqoCJlHA0


class TrieNode:
    def __init__(self):
        self.children = defaultdict(TrieNode)
        self.end_of_word = False


class TrieV1(object):
    """ Do yourself a favor and checkout this article: https://leetcode.com/articles/implement-trie-prefix-tree/
    Time complexity:
        insert(word): O(k), where k is the length of word
        search(word): O(k), in each step we search for the next key character. In the worst case the algorithm performs
        k operations
        startsWith(prefix): O(k)
    Space complexity:
        insert(word): O(k), in the worst case the newly inserted key doesn't share a prefix with the keys already
        inserted in the trie. We have to add k new nodes.
        search(word): O(1)
        startsWith(prefix): O(1)
    """

    def __init__(self):
        self.root = TrieNode()

    def insert(self, word):
        root = self.root
        for c in word:
            root = root.children[c]  # By doing this we traverse down the tree, so the root is reassigned to its
            # child, and so on, so we are progressively following the child till we reach the end of word
        root.end_of_word = True

    def search(self, word):
        root = self.root
        for c in word:
            if c not in root.children:
                return False
            root = root.children[c]
        return root.end_of_word

    def startsWith(self, prefix):
        """ Returns if there is any word in the trie that starts with the given prefix. """
        root = self.root
        for c in prefix:
            if c not in root.children:
                return False
            root = root.children[c]
        return True


class TrieV2:
    """ The Trie itself can be used as a root node without the need of creating a TrieNode. """

    def __init__(self):
        self.children = defaultdict(TrieV2)
        self.end_of_word = False

    def insert(self, word):
        root = self
        for c in word:
            root = root.children[c]
        root.end_of_word = True

    def search(self, word):
        root = self
        for c in word:
            if c not in root.children:
                return False
            root = root.children[c]
        return root.end_of_word

    def startsWith(self, prefix):
        root = self
        for c in prefix:
            if c not in root.children:
                return False
            root = root.children[c]
        return True


class Test(unittest.TestCase):
    trie = TrieV1()
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