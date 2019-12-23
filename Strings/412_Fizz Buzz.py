""" Write a program that outputs the string representation of numbers from 1 to n.
But for multiples of three it should output “Fizz” instead of the number and for the multiples of five output “Buzz”.
For numbers which are multiples of both three and five output “FizzBuzz”. """

import unittest2 as unittest


def fizz_buzz_v1(n):
    ''' Naive approach.
        For every number, if it is divisible by both 3 and 5, add FizzBuzz to the answer list.
        Else, check if the number is divisible by 3, add Fizz.
        Else, check if the number is divisible by 5, add Buzz.
        Else, add the number.
    Time complexity: O(n)
    Space complexity: O(1)
    '''
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


def fizz_buzz_v2(n):
    """ This approach won't reduce the asymptotic complexity, but proves to be a neater solution when FizzBuzz comes
        with a twist. What if FizzBuzz is now FizzBuzzJazz i.e. 3 ---> 'Fizz' , 5 ---> 'Buzz', 7 ---> 'Jazz'
        If we try to solve this with the previous approach, the program would have too many conditions to check.
        Instead of checking for every combination of these conditions, check for divisibility by given numbers i.e.
        3, 5 as given in the problem. If the number is divisible, concatenate the corresponding string mapping 'Fizz'
        or 'Buzz' to the current answer string.
        So for FizzBuzz we just check for two conditions instead of three conditions as in the first approach.
        Similarly, for FizzBuzzJazz now we would just have three conditions to check for divisibility.
    Time complexity: O(n)
    Space complexity: O(1)
    """
    res = []
    for i in range(1, n + 1):
        s = ''
        if i % 3 == 0:
            s += 'Fizz'
        if i % 5 == 0:
            s += 'Buzz'
        res.append(s if s else str(i))
    return res


class Test(unittest.TestCase):
    data = [(15, ['1', '2', 'Fizz', '4', 'Buzz', 'Fizz', '7', '8', 'Fizz', 'Buzz', '11', 'Fizz', '13', '14', 'FizzBuzz']
             )]

    def test_fizz_buzz(self):
        for test_n, result in self.data:
            self.assertEqual(result, fizz_buzz_v1(test_n))
            self.assertEqual(result, fizz_buzz_v2(test_n))


if __name__ == '__main__':
    unittest.main()