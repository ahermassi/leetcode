""" Implement a trie with insert, search, and startsWith methods. """

import unittest as unittest
from collections import defaultdict

# Video explanation: https://www.youtube.com/watch?v=oobqoCJlHA0

# Do yourself a favor and check out this article: https://leetcode.com/articles/implement-trie-prefix-tree/


class TrieNode:
    def __init__(self):
        self.children = defaultdict(TrieNode)
        self.end_of_word = False


class TrieV1(object):
    """ There are several other data structures, like balanced trees and hash tables, which give us the possibility to
         search for a word in a dataset of strings. Then why do we need trie? Trie could use less space compared to
         Hash Table when storing many keys with the same prefix.

         Trie is a rooted tree. Its nodes have the following fields:
            - Maximum of R links to its children, where each link corresponds to one of R character values from
               dataset alphabet. We assume that R is 26, the number of lowercase latin letters.
            - Boolean field which specifies whether the node corresponds to the end of the key, or is just a key prefix.

    Time complexity:
        insert(word): O(k), where k is the length of word. In each iteration we either examine or create a node in the
        trie till we reach the end of the word.
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
        """ We insert a key by searching into the trie. We start from the root and search a link, which corresponds to
             the first key character. There are two cases :

                - A link exists. Then we move down the tree following the link to the next child level. The algorithm
                   continues with searching for the next key character.
                - A link does not exist. Then we create a new node and link it with the parent's link matching the
                   current key character.
                   We repeat this step until we encounter the last character of the key, then we mark the current node
                   as an end node.
        """
        root = self.root
        for c in word:
            root = root.children[c]
            # By doing this we traverse down the tree, so the root is reassigned to its child, and so on, so we are
            # progressively following the child till we reach the end of word
        root.end_of_word = True

    def search(self, word):
        """ Each key is represented in the trie as a path from the root to the internal node or leaf.

             We start from the root with the first key character. We examine the current node for a link corresponding
             to the key character. There are two cases :

                - A link exists. We move to the next node in the path following this link, and proceed searching for
                   the next key character.

                - A link does not exist. If there are no available key characters and current node is marked as
                   end_of_word we return true. Otherwise, there are possible two cases in each of them we return false :
                        -> There are key characters left, but it is impossible to follow the key path in the trie, and
                              the key is missing.
                        -> No key characters left, but current node is not marked as end_of_word. Therefore, the search
                              key is only a prefix of another key in the trie.
        """
        root = self.root
        for c in word:
            if c not in root.children:
                return False
            root = root.children[c]
        return root.end_of_word

    def startsWith(self, prefix):
        """ The approach is very similar to the one we used for searching a key in a trie. We traverse the trie from
             the root, till there are no characters left in key prefix, or it is impossible to continue the path in the
             trie with the current key character. The only difference with the mentioned above search for a key is that
             when we come to an end of the key prefix, we always return true. We don't need to consider the end_of_word
             mark of the current trie node, because we are searching for a prefix of a key, not for a whole key.
        """
        root = self.root
        for c in prefix:
            if c not in root.children:
                return False
            root = root.children[c]
        return True


class TrieV2:
    """ A trie implementation using nested hash map. """

    def __init__(self):
        self.root = dict()

    def insert(self, word: str) -> None:
        root = self.root
        for c in word:
            if c not in root:
                root[c] = dict()
            root = root[c]
        root['#'] = '#' # Add end of word marker to the map of current node

    def search(self, word: str) -> bool:
        root = self.root
        for c in word:
            if c not in root:
                return False
            root = root[c]
        return '#' in root

    def startsWith(self, prefix: str) -> bool:
        root = self.root
        for c in prefix:
            if c not in root:
                return False
            root = root[c]
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