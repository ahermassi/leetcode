""" Given an array of characters, compress it in-place.
Every element of the array should be a character (not int) of length 1.
After you are done modifying the input array in-place, return the new length of the array.
Input:
['a','a','b','b','c','c','c']
Output:
Return 6, and the first 6 characters of the input array should be: ['a','2','b','2','c','3']
"""

import unittest2 as unittest


def compress(chars):
    """ Group the array into repeated chunks, keeping track of the character and the count. This forms the encoded
        contents.
        Update the original array with the encoded contents. We maintain a left pointer to know which position to
        update the original array with the encoded contents and increment it according to the length of the encoded
        contents.
    Time complexity: O(N)
    Space complexity: O(1)
    """
    left, right = 0, 1
    while right < len(chars):
        while right < len(chars) and chars[left] == chars[right]:
            right += 1
        count = right - left
        if count > 1:
            digits = list(str(count))
            chars[left + 1:left + count] = digits
            left += len(digits) + 1
            right = left + 1
        else:
            left = right
            right += 1
    return left + 1  # 'left' would always point to the last character in the string, so the array length is left+1


class Test(unittest.TestCase):
    data = [(['a', 'a', 'b', 'b', 'c', 'c', 'c'], 6, ['a', '2', 'b', '2', 'c', '3']),
            (['a', 'b', 'b', 'b', 'b', 'b', 'b', 'b', 'b', 'b', 'b', 'b', 'b'], 4, ['a', 'b', '1', '2']),
            ]

    def test_compress(self):
        for test_chars, result, new_array in self.data:
            i = compress(test_chars)
            self.assertEqual(new_array, test_chars[:i])


if __name__ == '__main__':
    unittest.main()
