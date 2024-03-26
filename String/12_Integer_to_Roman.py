""" Given an integer, convert it to a roman numeral. """

import unittest2 as unittest


#  Video explanation: https://youtu.be/ohBNdSJyLh8
def int_to_roman(num):
    """ Roman numerals are made with 7 single-letter symbols, each with its own value. Additionally, the subtractive
         rules (as explained in the problem description) give an additional 6 symbols. This gives us a total of 13
         unique symbols (each symbol is made of either 1 or 2 letters).

         An integer is represented as a Roman numeral by finding symbols that add to its value.

         One thing that can be a bit confusing if you're not familiar with Roman numerals is to know which
         representation is the "correct" one for a particular integer. For example, consider these possible ways of
         representing 140:
         50 + 50 + 40
         100 + 10 + 10 + 10 + 10
         100 + 40
         90 + 50
         40 + 40 + 40 + 10 + 10
         100 + 10 + 10 + 5 + 5 + 5 + 5

         The system we use to decide is to select the representation with the largest possible symbols, working from
         left to right. For example, the representations above with the largest symbol at the start are the ones
         starting with C (100):
         100 + 10 + 10 + 10 + 10
         100 + 40
         100 + 10 + 10 + 5 + 5 + 5 + 5

         To decide which of these to go with, we look at the next symbol. Two of them have an X, which is worth 10, and
         one of them has an XL, which is worth 40. Because the XL is worth more, we go with that representation.
         Therefore, the representation for 140 is CXL (100 + 40).

        Representing a given integer as a Roman numeral requires finding a sequence of the above 13 symbols, where their
        corresponding values add up to the integer. This sequence must be in order from largest to smallest, based on
        symbol value. So to represent a given integer, we look for the largest symbol that fits into it. We subtract
        that, and then look for the largest symbol that fits into the remainder, and so on until the remainder is 0.
        Each of the symbols we take out are appended to the output Roman numeral string.

        For example, suppose we need to make the number 671.
        The largest symbol that fits into 671 is D (which is worth 500). The next symbol up, CM, is worth 900 and so is
        too big to fit. Therefore, we now have the following:

        Roman numeral so far: D
        Integer remainder: 671 - 500 = 171

        We now repeat the process with 171. The largest symbol that fits into it is C (worth 100).

        Roman numeral so far: DC
        Integer remainder: 171 - 100 = 71

        Repeating this with 71, we find the largest symbol that fits in is L (worth 50).

        Roman numeral so far: DCL
        Integer remainder: 71 - 50 = 21

        For 21, the largest symbol that fits in is X (worth 10).

        Roman numeral so far: DCLX
        Integer remainder: 21 - 10 = 11

        For 11, the largest symbol that fits in is again X.

        Roman numeral so far: DCLXX
        Integer remainder: 11 - 10 = 1

        Finally, the 1 is represented with I, and we're done.

        Roman numeral so far: DCLXXI
        Integer remainder: 1 - 1 = 0

        The cleanest way to implement this in code is to loop over each symbol, from largest to smallest, checking how
        many copies of the current symbol fit into the remaining integer.

        We use a decreasingly ordered mapping from decimals to roman symbols. We keep dividing the original number by
        the largest possible decimal and convert the division result to the corresponding roman symbol which we append
        to the final string, get the modulo and re-iterate.

    Time complexity: O(1), as there is a finite set of roman numerals, there is a hard upper limit on how many times
    the loop can iterate. This upper limit is 15, and it occurs for the number 3888, which has a representation
    of MMMDCCCLXXXVIII
    Space complexity: O(1)
    """
    numerals_to_romans = [
        (1000, 'M'),
        (900, 'CM'),
        (500, 'D'),
        (400, 'CD'),
        (100, 'C'),
        (90, 'XC'),
        (50, 'L'),
        (40, 'XL'),
        (10, 'X'),
        (9, 'IX'),
        (5, 'V'),
        (4, 'IV'),
        (1, 'I')
    ]
    res = []
    for numeral, roman in numerals_to_romans:
        count = num // numeral
        # Append "count" copies of "roman" to roman_digits
        res.append(count * roman)
        num = num % numeral
        if not num:
            # We don't want to continue looping if we're done
            break
    return ''.join(res)


class Test(unittest.TestCase):
    data = [
        (3, 'III'),
        (4, 'IV'),
        (9, 'IX'),
        (58, 'LVIII'),
        (1994, 'MCMXCIV')
    ]

    def test_int_to_roman(self):
        for test_int, result in self.data:
            self.assertEqual(result, int_to_roman(test_int))


if __name__ == '__main__':
    unittest.main()

