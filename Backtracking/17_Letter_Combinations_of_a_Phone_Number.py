''' Given a string containing digits from 2-9 inclusive, return all possible letter combinations that the number could
represent.
A mapping of digit to letters (just like on the telephone buttons) is given. Note that 1 does not map to any letters.
'''

import unittest2 as unittest


def letter_combinations(digits):
    """ If there is no more digits to check that means that the current combination 's' is done (marked by len(s) == n)
        If there are still digits to check :
            Iterate over the letters mapping the next available digit (at index i of digits)
            Append the current letter to the current combination s = s + letter.
            Proceed to check next digits : backtrack(s + letter, i + 1).
    Time complexity: O(3 ** N + 4 ** M), where N is the number of digits in the input that maps to 3 letters (e.g. 2,
    3, 4, 5, 6, 8) and M is the number of digits in the input that maps to 4 letters (e.g. 7, 9), and N+M is the total
    number digits in the input.
    Space complexity: O(3 ** N + 4 ** M) since we have to keep O(3 ** N + 4 ** M) solutions
    """
    n = len(digits)
    d = {'2': 'abc', '3': 'def', '4': 'ghi', '5': 'jkl', '6': 'mno', '7': 'pqrs', '8': 'tuv', '9': 'wxyz'}

    def backtrack(s, i):
        if len(s) == n:
            res.append(s)
            return
        chars = d[digits[i]]
        for char in chars:
            backtrack(s + char, i + 1)

    res = []
    if digits:
        backtrack('', 0)
    return res


class Test(unittest.TestCase):
    data = [('23', ['ad', 'ae', 'af', 'bd', 'be', 'bf', 'cd', 'ce', 'cf'])]

    def test_min_meeting_rooms(self):
        for test_digits, result in self.data:
            self.assertEqual(result, letter_combinations(test_digits))


if __name__ == '__main__':
    unittest.main()