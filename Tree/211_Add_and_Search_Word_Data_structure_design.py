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


class WordDictionary(object):
    """ Use a trie to store the words, and backtracking to check each character of word to search.
    Time complexity:
        addWord: O(k) where k is the length of word (worst case if the word is new)
        search: if we exclude wildcards (.), worst-case search will iterate through the longest word (i.e. linear to
        the maximum number of characters in a word). With wildcards, it will iterate through the whole tree in the
        worst case (i.e. linear to the total number of characters)
    Space complexity:
        addWord: O(K), in the worst case newly inserted word doesn't share a prefix with the the words already
        inserted in the trie. We have to add K new nodes
        search: O(1) if we exclude wildcards, O(N) (i.e. linear to the total number of characters) in the worst case
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
            if c in root.children:
                root = root.children[c]
            else:
                root.children[c] = TrieNode()
                root = root.children[c]
        root.end_of_word = True

    def search(self, word):
        """
        Returns if the word is in the data structure. A word could contain the dot character '.' to represent any one letter.
        :type word: str
        :rtype: bool
        """

        def helper(index, node):
            if index == len(word):
                return node.end_of_word
            c = word[index]
            if c in node.children:
                return helper(index + 1, node.children[c])
            elif c == '.':
                for n in node.children.values():
                    if helper(index + 1, n):
                        return True
                return False

        root = self.root
        return helper(0, root)


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