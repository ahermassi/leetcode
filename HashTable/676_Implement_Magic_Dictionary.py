""" Design a data structure that is initialized with a list of different words. Provided a string, you should
determine if you can change exactly one character in this string to match any word in the data structure.

Implement the MagicDictionary class:

MagicDictionary() Initializes the object.
void buildDict(String[] dictionary) Sets the data structure with an array of distinct strings dictionary.
bool search(String searchWord) Returns true if you can change exactly one character in searchWord to match any string
in the data structure, otherwise returns false. """

from collections import defaultdict


class MagicDictionaryV1(object):
    """ For each word in the dictionary, use the word'a length as key and save all the words with the same length
        in a list as value of that key.
        During the search, we iterate over the list of words that have the same length as the search word. For each of
        these words, we count the number of non-equal characters at each index. If one word has only 1 different
        character than the search word, we return true. If at any point the character difference is more than 1, then
        we immediately stop comparing the current dictionary word.
    Time complexity: O(N) for buildDict, O(N * L) for search, where N is the number of words in the dictionary and L
    is the length of the longest word.
    Space complexity: O(N)
    """

    def __init__(self):
        """
        Initialize your data structure here.
        """
        self.lengths = defaultdict(list)

    def buildDict(self, dictionary):
        """
        :type dictionary: List[str]
        """
        for word in dictionary:
            self.lengths[len(word)].append(word)

    def search(self, search_word):
        n = len(search_word)
        if n not in self.lengths:
            return False
        for word in self.lengths[n]:
            different_chars = 0
            for i, c in enumerate(word):
                if c != search_word[i]:
                    different_chars += 1
                    if different_chars > 1:  # No hope. Move on to the next dictionary word.
                        break
            if different_chars == 1:
                return True
        return False


class TrieNode(object):
    def __init__(self):
        self.children = defaultdict(TrieNode)
        self.is_word = False


class MagicDictionaryV2(object):
    """ Use a trie to store the words in a space-efficient manner. During the search, we use a boolean 'change_allowed'
        to tell whether we still can change a character in the search word. Let 'c' be th character at the current
        index. We need to take care of 4 cases:
            - If 'c' is not a child of the current trie node:
                * If no 'change_allowed', we return False as no further character changes are possible.
                * If 'change_allowed', we continue the search from all the trie nodes of the current node's children.
                  Each of these nodes accounts for a character change and change_allowed=False is passed down.
                  If any of these searches returns True, we're done. Otherwise, we return False.
            - If 'c' is a child of the current trie node:
                * If 'change_allowed', we carry on the search from the trie node associated with 'c' with still a
                  possibility of 'change_allowed'. If the search returns a favorable result, we're done. Otherwise, we
                  continue the search from all the trie nodes of the current node's children whose values are not equal
                  to 'c'. Each of these nodes accounts for a character change and change_allowed=False is passed down.
                  If any of these searches returns True, we're done. Otherwise, we return False.
                * If no 'change_allowed', we carry on the search from the trie node associated with 'c' with no more
                  possibility of 'change_allowed'. The result of this search determines the final outcome.
    """

    def __init__(self):
        """
        Initialize your data structure here.
        """
        self.trie = TrieNode()

    def buildDict(self, dictionary):
        """
        :type dictionary: List[str]
        """
        for word in dictionary:
            self.add_word(word)

    def add_word(self, word):
        trie = self.trie
        for c in word:
            trie = trie.children[c]
        trie.is_word = True

    def search(self, search_word):

        def word_exists(trie, index, change_allowed):
            if index == n:
                return trie.is_word and not change_allowed
            c = search_word[index]
            if c not in trie.children:
                if not change_allowed:
                    return False
                for child in trie.children:
                    if word_exists(trie.children[child], index + 1, False):
                        return True
                return False
            if change_allowed:
                if word_exists(trie.children[c], index + 1, True):
                    return True
                for child in trie.children:
                    if child != c and word_exists(trie.children[child], index + 1, False):
                        return True
                return False
            return word_exists(trie.children[c], index + 1, False)

        n = len(search_word)
        return word_exists(self.trie, 0, True)
