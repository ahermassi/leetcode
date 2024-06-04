""" Given a roman numeral, convert it to an integer.  """

import unittest2 as unittest


# Video explanation: https://youtu.be/3jdxYj3DD98
def roman_to_int(s):
    """ Let's work through some examples before having a go at writing the algorithm.

         What is CXVII as an integer?
         Recall that C = 100, X = 10, V = 5, and I = 1. Because the symbols are ordered from most to least significant,
         we can simply add the symbols, i.e. C + X + V + I + I = 100 + 10 + 5 + 1 + 1 = 117.

         What is DXCI as an integer?
         Recall that D = 500. Now, notice that this time the symbols are not ordered from most to least significant—the
         X and C are out of numeric order. Because of this, we subtract the value of X (10) from the value of C (100) to
         get 90. So, going from left to right, we have D + (C - X) + I = 500 + 90 + 1 = 591.

         What is CMXCIV as an integer?
        Recall that M = 1000. The symbols barely look sorted at all here—from left-to-right we have 100, 1000, 10, 100,
        1, 5. We just need to look for each occurrence of a smaller symbols preceding a bigger symbol. The first, third,
        and fifth symbols are all smaller than their next symbol. Therefore, they are all going to be subtracted from
        their next.
        The first two symbols are CM. This is M - C = 1000 - 100 = 900
        The second two symbols are XC. This is C - X = 100 - 10 = 90.
        The final two symbols are IV. This is V - I = 5 - 1 = 4.
        Like we did above, we add these together. (M - C) + (C - X) + (V - I) = 900 + 90 + 4 = 994.

        Let's hardcode a mapping with the value of each symbol so that we can easily look them up. Recall that each
        symbol adds its own value, except for when a smaller valued symbol is before a larger valued symbol. In those
        cases, instead of adding both symbols to the total, we need to subtract the large from the small, adding that
        instead.

        Therefore, the simplest algorithm is to use a pointer to scan through the string, and at each step decide
        whether to add or subtract the current symbol:

            - If the next symbol has a greater value, the current symbol has to be subtracted from the current total
            - If the next symbol has a smaller value, the current symbol's value can be added from the current total

        Note that we could also view the roman numeral as having 13 unique symbols instead of 7 {1, 4, 5, 9, 10, 40, 50,
        90, 100, 400, 500, 900, 1000}. In this case, we need to work our way down the string in the same way,
        left-to-right, firstly checking if we're at a length-2 symbol, and if not we treat it as a length-1 symbol:
                if at least 2 characters remaining and s[i:i+2] is in roman_to_integer:
                    res += roman_to_integer[s[i:i+2]]
                    i += 2
                else:
                    res += roman_to_integer[s[i]]
                    i += 1

    Time complexity: O(N)
    Space complexity: O(1)
    """
    roman_to_integer = {'I': 1, 'V': 5, 'X': 10, 'L': 50, 'C': 100, 'D': 500, 'M': 1000}
    n, res, i = len(s), 0, 0
    while i < n:
        if i < n - 1 and roman_to_integer[s[i]] < roman_to_integer[s[i + 1]]:
            res -= roman_to_integer[s[i]]
        else:
            res += roman_to_integer[s[i]]
        i += 1
    return res


class Test(unittest.TestCase):
    data = [
        (3, 'III'),
        (4, 'IV'),
        (9, 'IX'),
        (58, 'LVIII'),
        (1994, 'MCMXCIV')
    ]

    def test_roman_to_int(self):
        for result, test_string in self.data:
            self.assertEqual(result, roman_to_int(test_string))
            self.assertEqual(result, roman_to_int(test_string))


if __name__ == '__main__':
    unittest.main()
