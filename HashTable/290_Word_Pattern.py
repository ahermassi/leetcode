""" Given a pattern and a string s, find if s follows the same pattern.
Here follow means a full match, such that there is a bijection between a letter in pattern and a non-empty word in s.
"""

import unittest2 as unittest


# Video explanation: https://youtu.be/W_akoecmCbM
def word_pattern(pattern, s):
    """ Similar to 205- Isomorphic Strings.

        We use two hash maps, one for mapping characters to words and the other for mapping words to characters. We need
        two dictionaries instead of one since we need one-to-one mapping from each pattern character to each word and
        vice versa. While scanning each character-word pair:

        - If the character is not in the character to word mapping, we additionally check whether that word is also in
           the word to character mapping. If that word is already in the word to character mapping, then we can return
           False immediately since it has been mapped with some other character before. Else, update both mappings.

        - If a mapping already exists for a character or a word, but it doesn't map to the other word or character. In
           this case, we can return False immediately.

    Time complexity: O(N + M), where N is the length of s and M is the length of pattern
    Space complexity: O(N), where N is the length of s. No more than 26 bijections will be added to each hashmap since
    they are limited by the number of letters in the alphabet. The character to word hashmap stores a word for each
    entry, which are substrings of s, so their combined lengths equal s. Therefore, this hashmap requires O(26+N) space.
    The other hashmap requires the same amount of space.
    """
    words = s.split(' ')
    if len(pattern) != len(words):
        return False
    pattern_map, words_map = dict(), dict()
    for i, c in enumerate(pattern):
        if (c in pattern_map and pattern_map[c] != words[i]) or (words[i] in words_map and words_map[words[i]] != c):
            return False
        pattern_map[c] = words[i]
        words_map[words[i]] = c
    return True


class Test(unittest.TestCase):
    data = [
        ('abba', 'dog cat cat dog', True),
        ('abba', 'dog cat cat fish', False)
        ]

    def test_is_isomorphic(self):
        for pattern, test_string, result in self.data:
            self.assertEqual(result, word_pattern(pattern, test_string))
            self.assertEqual(result, word_pattern(pattern, test_string))


if __name__ == '__main__':
    unittest.main()