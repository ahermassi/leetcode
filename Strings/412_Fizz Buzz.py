''' Write a program that outputs the string representation of numbers from 1 to n.
But for multiples of three it should output “Fizz” instead of the number and for the multiples of five output “Buzz”.
For numbers which are multiples of both three and five output “FizzBuzz”. '''

import unittest2 as unittest


def fizz_buzz_v1(n):
    """ Naive approach.
        For every number, if it is divisible by both 3 and 5, add FizzBuzz to the answer list.
        Else, check if the number is divisible by 3, add Fizz.
        Else, check if the number is divisible by 5, add Buzz.
        Else, add the number.
    Time complexity: O(n)
    Space complexity: O(1)
    """
    res = []
    for i in range(1, n + 1):
        if i % 3 == 0 and i % 5 == 0:
            res.append('FizzBuzz')
        elif i % 3 == 0:
            res.append('Fizz')
        elif i % 5 == 0:
            res.append('Buzz')
        else:
            res.append(str(i))
    return res


class Test(unittest.TestCase):
    data = [(15, ['1', '2', 'Fizz', '4', 'Buzz', 'Fizz', '7', '8', 'Fizz', 'Buzz', '11', 'Fizz', '13', '14', 'FizzBuzz']
             )]

    def test_fizz_buzz(self):
        for test_n, result in self.data:
            self.assertEqual(result, fizz_buzz_v1(test_n))


if __name__ == '__main__':
    unittest.main()