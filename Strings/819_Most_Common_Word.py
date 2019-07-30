from collections import Counter
import unittest2 as unittest


def most_common_word(paragraph, banned):
    """ 1- Remove all punctuations
        2- Change to lowercase
        3- words count for each word not in banned set
        4- return the most common word
    Time complexity: O(N + M) where N is the size of paragraph and M is the size of banned
    Space complexity: O(N + M) to store the count and the banned set (I'd argue that storing the banned set is O(1))
    """
    ban_set = set(banned)  # Membership test is going to be performed on the banned list, so better make it a set
    for c in '!?\',;.':
        paragraph = paragraph.replace(c, ' ')
    counter = Counter(word.lower() for word in paragraph.split() if word.lower() not in ban_set)
    most_common, count = '', 0
    for k, v in counter.items():
        if v > count:
            most_common, count = k, v
    return most_common


class Test(unittest.TestCase):
    data = [('Bob hit a ball, the hit BALL flew far after it was hit.', ["hit"], 'ball')]

    def test_most_common_word(self):
        for test_paragraph, banned, result in self.data:
            self.assertEqual(result, most_common_word(test_paragraph, banned))


if __name__ == '__main__':
    unittest.main()
