""" Given a paragraph and a list of banned words, return the most frequent word that is not in the list of banned
words.  It is guaranteed there is at least one word that isn't banned, and that the answer is unique.
Words in the list of banned words are given in lowercase, and free of punctuation.  Words in the paragraph are not case
sensitive.  The answer is in lowercase. """


from collections import Counter, defaultdict
import unittest2 as unittest


def most_common_word_v1(paragraph, banned):
    """ We'll need some count of words (converted to lowercase) that we have seen in the paragraph. As we iterate
        through the paragraph, we will collect these words (with punctuation removed and converted to lowercase) if
        the word is not banned.
        For each word (lowercase, and free of punctuation), we'll update our count and update the answer if the count
        of that word is highest.
    Time complexity: O(N + M), where N is the size of paragraph and M is the size of banned
    Space complexity: O(N + M), to store the count and the banned set
    """
    banned = set(banned)  # Membership test is going to be performed on the banned list, so better make it a set
    for c in '!?\',;.':
        paragraph = paragraph.replace(c, ' ')
    counter = Counter(word for word in paragraph.lower().split() if word not in banned)
    most_common, count = '', 0
    for k, v in counter.items():
        if v > count:
            most_common, count = k, v
    return most_common


def most_common_word_v2(paragraph, banned):
    """ Perform a single pass over the paragraph, constructing the counter hash map and updating the final result
        as we go.
    Time complexity: O(N + M), where N is the size of paragraph and M is the size of banned
    Space complexity: O(N + M), to store the count and the banned set
    """
    banned = set(banned)
    for c in '!?\',;.':
        paragraph = paragraph.replace(c, ' ')
    words = paragraph.lower().split()
    counter = defaultdict(int)
    max_count, res = float('-inf'), ''
    for word in words:
        if word not in banned:
            counter[word] += 1
            if counter[word] > max_count:
                max_count, res = counter[word], word
    return res


class Test(unittest.TestCase):
    data = [('Bob hit a ball, the hit BALL flew far after it was hit.', ["hit"], 'ball')]

    def test_most_common_word(self):
        for test_paragraph, banned, result in self.data:
            self.assertEqual(result, most_common_word_v1(test_paragraph, banned))
            self.assertEqual(result, most_common_word_v2(test_paragraph, banned))


if __name__ == '__main__':
    unittest.main()
