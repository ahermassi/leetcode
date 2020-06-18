""" Given two integers representing the numerator and denominator of a fraction, return the fraction in string format.
If the fractional part is repeating, enclose the repeating part in parentheses. """

import unittest2 as unittest


def fraction_to_decimal(numerator, denominator):
    """ The key insight here is to notice that once the remainder starts repeating, so does the divided result.
        We will need a hash table that maps the remainder to its position in the fractional part. Once we find a
        repeating remainder, we may enclose the reoccurring fractional part with parentheses by consulting the position
        from the hash table.
        The remainder could be zero while doing the division. That means there is no repeating fractional part and we
        should stop right away.
    """
    if not numerator:
        return '0'
    res = []
    if (numerator < 0) ^ (denominator < 0):  # If either one is negative (not both)
        res.append('-')
    numerator, denominator, remainders = abs(numerator), abs(denominator), {}
    n, remainder = divmod(numerator, denominator)
    res.append(n)
    if not remainder:
        return ''.join(map(str, res))
    res.append('.')
    while remainder:
        if remainder in remainders:  # Recurring decimal found
            index = remainders[remainder]  # Find the first occurrence of the decimal ..
            res.insert(index, '(')  # and enclose it within parentheses
            res.append(')')
            break
        remainders[remainder] = len(res)
        remainder *= 10
        n, remainder = divmod(remainder, denominator)
        res.append(n)
    return ''.join(map(str, res))


class Test(unittest.TestCase):
    data = [(1, 2, '0.5'), (2, 1, '2'), (2, 3, '0.(6)')]

    def test_fraction_to_decimal(self):
        for test_numerator, test_denominator, result in self.data:
            self.assertEqual(result, fraction_to_decimal(test_numerator, test_denominator))


if __name__ == '__main__':
    unittest.main()
