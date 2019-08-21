""" Given an integer, convert it to a roman numeral. """

import unittest2 as unittest


def int_to_roman_v1(num):
    """ Most intuitive approach, at least to me. It scans num backwards, constructing the result as we go. Reading
        backwards was decided so we don't need to know the number of digits in the number beforehand.
    Time complexity: O(N)
    Space complexity: O(1)
    """
    ans, num, weight = [], str(num)[::-1], 1
    d = {1: 'I', 5: 'V', 10: 'X', 50: 'L', 100: 'C', 500: 'D', 1000: 'M'}
    for digit in num:
        digit = int(digit)
        if digit == 0:
            weight *= 10
            continue
        if digit in {4, 9}:
            ans.append(d[(digit + 1) * weight])
            ans.append(d[weight])
        elif digit in {1, 5}:
            ans.append(d[digit * weight])
        elif digit in {2, 3}:
            for _ in range(digit):
                ans.extend(d[weight])
        else:
            for _ in range(digit % 5):
                ans.extend(d[weight])
            ans.append(d[5 * weight])
        weight *= 10
    return ''.join(ans[::-1])


class Test(unittest.TestCase):
    data = [
        (3, 'III'),
        (4, 'IV'),
        (9, 'IX'),
        (58, 'LVIII'),
        (1994, 'MCMXCIV')
    ]

    def test_roman_to_int(self):
        for test_int, result in self.data:
            self.assertEqual(result, int_to_roman_v1(test_int))


if __name__ == '__main__':
    unittest.main()

