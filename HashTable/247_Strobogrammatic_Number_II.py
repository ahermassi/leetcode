""" A strobogrammatic number is a number that looks the same when rotated 180 degrees (looked at upside down).
Find all strobogrammatic numbers that are of length = n. """

import unittest2 as unittest


def find_strobogrammatic_v1(n):
    """ Some observation to the sequence:
        n = 1: [0, 1, 8]
        n = 2: [11, 88, 69, 96]
        How about n = 3 ?
        => It can be retrieved if we insert [0, 1, 8] to the middle of solution of n = 3 - 1 = 2
        How about n = 4 ?
        => It can be retrieved if we insert [00, 11, 88, 69, 96] to the middle of solution of n = 4 - 2 = 2
        How about n = 5 ?
        => It can be retrieved if we insert [0, 1, 8] to the middle of solution of n = 5 - 1 = 4
        Same for n = 6, it can be retrieved if we insert [00, 11, 88, 69, 96] to the middle of solution of n = 6 - 2 = 4
    Time/space complexity: this thread discusses that:
    https://leetcode.com/problems/strobogrammatic-number-ii/discuss/67280/AC-clean-Java-solution
    """
    odd, even = ['0', '1', '8'], ['00', '11', '69', '88', '96']
    if n == 1:
        return odd
    if n == 2:
        return even[1:]
    pre = find_strobogrammatic_v1(n - 1) if n % 2 == 1 else find_strobogrammatic_v1(n - 2)
    temp = odd if n % 2 == 1 else even
    res = []
    for val in pre:
        for c in temp:
            res.append(val[:(n - 1) // 2] + c + val[(n - 1) // 2:])
    return res


def find_strobogrammatic_v2(n):
    """ We start from the middle and expand out.
    Time complexity: O(n), since res has at most 5 elements
    Space complexity: O(1), temp uses constant space of at most 5
    """
    res = [''] if n % 2 == 0 else ['0', '1', '8']
    for _ in range(n // 2):
        temp = []
        for num in res:
            temp.append('1' + num + '1')
            temp.append('8' + num + '8')
            temp.append('6' + num + '9')
            temp.append('9' + num + '6')
            if len(num) < n - 2:
                temp.append('0' + num + '0')
        res = temp
    return res


class Test(unittest.TestCase):
    data = [(2, ['11', '69', '88', '96']),
            (3, ['101', '111', '181', '609', '619', '689', '808', '818', '888', '906', '916', '986'])]

    def test_find_strobogrammatic(self):
        for test_num, result in self.data:
            self.assertEqual(result, find_strobogrammatic_v1(test_num))


if __name__ == '__main__':
    unittest.main()
