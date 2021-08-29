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
