""" Given a string containing digits from 2-9 inclusive, return all possible letter combinations that the number could
represent.
A mapping of digit to letters (just like on the telephone buttons) is given. Note that 1 does not map to any letters.
"""

import unittest2 as unittest


def letter_combinations_v1(digits):
    """ If there is no more digits to check, that means that the current combination 'path' is done.
        If there are still digits to check :
            Iterate over the letters mapping the next available digit (at index 'index' of digits)
            Append the current letter to the current combination: path = path + letter.
            Proceed to check next digits : dfs(index + 1, path + letter).
    Time complexity: O(3^N + 4^M), where N is the number of digits in the input that map to 3 letters (e.g. 2, 3, 4,
    5, 6, 8) and M is the number of digits in the input that map to 4 letters (e.g. 7, 9), and N+M is the total number
    of digits in the input. So overall, O(4^N) worst case where N is the length of digits.
    Space complexity: O(3^N + 4^M) since we have to keep O(3^N + 4^M) solutions, or O(4^N).
    """

    def dfs(index, path):
        if index == n:
            res.append(path)
            return
        for c in mapping[digits[index]]:
            dfs(index + 1, path + c)

    if not digits:
        return None
    mapping = {'2': 'abc', '3': 'def', '4': 'ghi', '5': 'jkl', '6': 'mno', '7': 'pqrs', '8': 'tuv', '9': 'wxyz'}
    n, res = len(digits), []
    dfs(0, '')
    return res


def letter_combinations_v2(digits):
    """ Iterative approach, similar to BFS where 'result' list is the queue.
        Example: digits = 23
            1st iteration: result = [''], new_result = [a, b, c]
            2nd iteration: result = [a, b, c], new_result = [ad, bd, cd, ae, be, ce, af, bf, cf]
            Return: result = [ad, bd, cd, ae, be, ce, af, bf, cf]
        Example: digits = 234
            1st iteration: result = [''], new_result = [a, b, c]
            2nd iteration: result = [a, b, c], new_result = [ad, bd, cd, ae, be, ce, af, bf, cf]
            3rd iteration: result = [ad, bd, cd, ae, be, ce, af, bf, cf],
            new_result = [adg, bdg, cdg, aeg, beg, ceg, afg, bfg, cfg, adh, bdh, cdh, aeh, beh, ceh, afh, bfh, cfh, adi,
                          bdi, cdi, aei, bei, cei, afi, bfi, cfi]
            Return: result
    Time complexity: O(3^N + 4^M)
    Space complexity: O(3^N + 4^M)
    """
    if not digits:
        return None
    mapping = {'2': 'abc', '3': 'def', '4': 'ghi', '5': 'jkl', '6': 'mno', '7': 'pqrs', '8': 'tuv', '9': 'wxyz'}
    result = ['']
    for digit in digits:
        new_result = []
        for c in mapping[digit]:
            for path in result:
                new_result.append(path + c)
        result = new_result
    return result


class Test(unittest.TestCase):
    data = [('23', ['ad', 'ae', 'af', 'bd', 'be', 'bf', 'cd', 'ce', 'cf'])]

    def test_letter_combinations(self):
        for test_digits, result in self.data:
            self.assertEqual(result, letter_combinations_v1(test_digits))
            self.assertEqual(result, sorted(letter_combinations_v2(test_digits)))


if __name__ == '__main__':
    unittest.main()
