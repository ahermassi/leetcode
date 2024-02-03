""" Given an arbitrary ransom note string and another string containing letters from all the magazines, write a
function that will return true if the ransom note can be constructed from the magazines ; otherwise, it will return
false.
Each letter in the magazine string can only be used once in your ransom note. """

from collections import defaultdict
import unittest2 as unittest


def can_construct_v1(ransomNote, magazine):
    """ Make a single pass over the magazine, storing the character counts in a single hashmap. Next, we make a pass
         over the ransom note. When processing a character, decrease its count in the frequency map. If at any time the
         count of a character drops below 0, it means there are more occurrences of this character in the note than in
         the magazine.

    Time complexity: O(N + M), where N is the length of the ransom note and M is the length of the magazine.
    Space complexity: O(1), the counter can hold at most 26 characters (or 128 characters)
    """
    counter = defaultdict(int)
    for c in magazine:
        counter[c] += 1
    for c in ransomNote:
        counter[c] -= 1
        if counter[c] < 0:
            return False
    return True


def can_construct_v2(ransomNote, magazine):
    """ Make a single pass over the ransom note, storing the character counts in a hashmap. Next, we make a pass over
         the magazine. When processing a character, if it appears in the hashmap, we reduce its count by 1; we remove it
         from the hashmap if its count drops to zero.

         If the hashmap becomes empty, we return true. If we reach the end of the ransom note and the hashmap is
         not empty, we return false: Each of the characters remaining in the hashmap occurs more times in the ransom
         note than the magazine.

    Time complexity: O(N + M)
    Space complexity: O(1)
    """
    counter = defaultdict(int)
    for c in ransomNote:
        counter[c] += 1
    for c in magazine:
        if c in counter:
            counter[c] -= 1
            if counter[c] == 0:
                del counter[c]
                if len(counter) == 0:
                    return True
    return False


class Test(unittest.TestCase):
    data = [('a', 'b', False), ('aa', 'ab', False), ('aa', 'aab', True)]

    def test_can_construct(self):
        for test_ransom_note, test_magazine, result in self.data:
            self.assertEqual(result, can_construct_v1(test_ransom_note, test_magazine))
            self.assertEqual(result, can_construct_v2(test_ransom_note, test_magazine))


if __name__ == '__main__':
    unittest.main()