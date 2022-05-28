""" Given a string containing digits from 2-9 inclusive, return all possible letter combinations that the number could
represent.
A mapping of digit to letters (just like on the telephone buttons) is given. Note that 1 does not map to any letters.
"""

import unittest2 as unittest

# Video explanation: https://www.youtube.com/watch?v=a-sMgZ7HGW0


def letter_combinations_v1(digits):
    """ Whenever we have a problem where we need to generate all combinations/permutations of some group of
         letters/numbers, the first thought we should have is backtracking.

         There aren't any smart tricks needed for this problem - the hard part is just figuring out how to correctly
         generate all possible combinations, and to do this using a standard backtracking algorithm template.

         Let's break down the problem, by starting with an input that is only 1-digit long, for example digits = "2".
         This example is trivial - just generate all letters that correspond with digit = "2", which would be
         ["a", "b", "c"].

         What if instead we had a 2-digit long input, digits = "23"? Imagine taking each letter of digit = "2" as a
         starting point. That is, lock the first letter in, and solve all the possible combinations that start with that
         letter. If our first letter will always be "a", then the problem is trivial again - it's the 1-digit case, and
         all we have to do is generate all the letters corresponding with digit = "3", and add that to "a", to get
         ["ad", "ae","af"].

         This was easy because we ignored the first letter, and said it will always be "a". But we know how to generate
         all the first letters too - it's the 1-digit case which we already solved to be ["a", "b", "c"].

        As we can see, solving the 1-digit case is trivial, and solving the 2-digit case is just solving the 1-digit case
        twice. The same reasoning can be extended to n digits. For the 3-digit case, solve the 2-digit case to generate
        all combinations of the first 2 letters, and then solve the 1-digit case for the final digit.

        As mentioned previously, we need to lock-in letters when we generate new letters. The easiest way to save state
        like this is to use recursion.

            - If there is no more digits to check, that means that the current combination 'path' is done.

            - If there are still digits to check:
                - Iterate over the letters that correspond to the current digit we are looking at
                - Append the current letter to the current combination: path = path + letter
                - Proceed to check next digits : dfs(index + 1, path + letter)

    Time complexity: O(3^N + 4^M), where N is the number of digits in the input that map to 3 letters (e.g. 2, 3, 4,
    5, 6, 8) and M is the number of digits in the input that map to 4 letters (e.g. 7, 9), and N+M is the total number
    of digits in the input. So overall, O(4^N) worst case where N is the length of digits.
    Space complexity: O(N), occupied by the recursion call stack. It will only go as deep as the number of digits in the
    input since whenever we reach that depth, we backtrack. As the hash map does not grow as the inputs grows, it
    occupies O(1) space.
    """

    def dfs(index, path):
        if index == n:
            res.append(path)
            return
        # Get the letters that the current digit maps to, and loop through them
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
            for combination in result:
                new_result.append(combination + c)
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
