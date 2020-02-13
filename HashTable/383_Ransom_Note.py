""" Given an arbitrary ransom note string and another string containing letters from all the magazines, write a
function that will return true if the ransom note can be constructed from the magazines ; otherwise, it will return
false.
Each letter in the magazine string can only be used once in your ransom note. """

from collections import Counter
import unittest2 as unittest


def can_construct_v1(ransomNote, magazine):
    """ Make a single pass over the magazine, storing the character counts in a single hash map. Next, we make a pass
        over the ransom note. When processing a character c, decrease its count in the frequency map. If at any time
        the count of a character drops below 0, it means there are more occurrences of this character in the note than
        in the magazine.
    Time complexity: O(N + M)
    Space complexity: O(1), the counter can hold at most 26 characters (or 128 characters)
    """
    counter = Counter(magazine)
    for c in ransomNote:
        counter[c] -= 1
        if counter[c] < 0:
            return False
    return True


class Test(unittest.TestCase):
    data = [('a', 'b', False), ('aa', 'ab', False), ('aa', 'aab', True)]

    def test_can_construct(self):
        for test_ransom_note, test_magazine, result in self.data:
            self.assertEqual(result, can_construct_v1(test_ransom_note, test_magazine))


if __name__ == '__main__':
    unittest.main()