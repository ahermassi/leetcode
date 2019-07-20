""" Convert an English string to Goat Latin """

import unittest2 as unittest


def to_goat_latin(S):
    """ Apply the transformations. Pretty straightforward.
    Time complexity: O(N ** 2): O(N) outer loop, O(N) word rotation in the worst case
    Space complexity: O(N)
    """
    words, res = S.split(' '), []
    for i, word in enumerate(words, 1):
        if word[0].lower() in set('aeiou'):
            word = word + 'ma'
        else:
            word = word[1:] + word[0] + 'ma'
        word = word + 'a' * i
        res.append(word)
    return ' '.join(res)


class Test(unittest.TestCase):
    data = [('I speak Goat Latin', 'Imaa peaksmaaa oatGmaaaa atinLmaaaaa'),
            ('The quick brown fox jumped over the lazy dog',
             'heTmaa uickqmaaa rownbmaaaa oxfmaaaaa umpedjmaaaaaa overmaaaaaaa hetmaaaaaaaa azylmaaaaaaaaa '
             'ogdmaaaaaaaaaa')
           ]

    def test_move_zeroes(self):
        for test_string, result in self.data:
            self.assertEqual(result, to_goat_latin(test_string))


if __name__ == '__main__':
    unittest.main()
