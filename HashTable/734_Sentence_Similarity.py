""" Given two sentences words1, words2 (each represented as an array of strings), and a list of similar word pairs
pairs, determine if two sentences are similar.
For example, "great acting skills" and "fine drama talent" are similar, if the similar word pairs are
pairs = [["great", "fine"], ["acting","drama"], ["skills","talent"]]. """

import unittest2 as unittest


def are_sentences_similar_v1(words1, words2, pairs):
    """ To check whether words1[i] and words2[i] are similar, either they are the same word, or (words1[i], words2[i])
        or (words2[i], words1[i]) appear in pairs.
        To check whether (words1[i], words2[i]) appears in pairs quickly, we could put all such pairs into a Set
        structure.
    Time complexity: O(N + M) where N is the maximum length of words1 and words2, and M is the length of pairs
    Space complexity: O(M)
    """
    if len(words1) != len(words2):
        return False
    pair_set = set(tuple(pair) for pair in pairs)
    for word1, word2 in zip(words1, words2):
        if word1 != word2 and (word1, word2) not in pair_set and (word2, word1) not in pair_set:
            return False
    return True


class Test(unittest.TestCase):
    data = [
        (['great', 'acting', 'skills'], ['fine', 'drama', 'talent'], [['great', 'fine'], ['acting', 'drama'], ['skills', 'talent']],
         True),
        (['great'], ['doubleplus', 'good'], [], False)
        ]

    def test_are_sentences_similar(self):
        for test_words1, test_words2, pairs, result in self.data:
            self.assertEqual(result, are_sentences_similar_v1(test_words1, test_words2, pairs))


if __name__ == '__main__':
    unittest.main()
