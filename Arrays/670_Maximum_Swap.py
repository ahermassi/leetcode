""" Given a non-negative integer, you could swap two digits at most once to get the maximum valued number. Return the
maximum valued number you could get. """

import unittest2 as unittest


def maximum_swap_v1(num):
    """ At each digit of the input number in order, if there is a larger digit that occurs later, we know that the best
        swap must occur with the digit we are currently considering.
        We first compute last_occurrence[d] = i, the index i of the last occurrence of digit d.
        Afterwards, when scanning the number from left to right, if there is a larger digit that occurs after the
        current index, we will swap it with the largest such digit. If there are multiple such digits, we will swap it
        with the one that occurs the latest.
        Why record the last index of each digit?
        Because we want to lose as least as possible. For example, num = 943848, which 8 should we swap with 4?
        Rightmost 8, because no matter which 8 is chosen, we gain the same at 4's position. However, if we choose the
        1st 8 (from the left), then we lose 400 for that position. If we choose the 2nd 8, then we only lose 4. So we
        always choose the rightmost one.
        Thinking process:
        To make num maximum, we need to find the most significant digit who has a higher value to its right. It makes
        the direction to scan from left(most significant) to right(least significantly).
    Time complexity: O(N)
    Space complexity: O(N)
    """
    digits = [int(c) for c in str(num)]
    last_occurrence, n = {val: i for i, val in enumerate(digits)}, len(digits)
    for i in range(n - 1):
        cur_digit = digits[i]
        for val in reversed(range(cur_digit + 1, 10)):  # Start from 9 down to (current digit + 1)
            if val in last_occurrence and last_occurrence[val] > i:  # This greater digit occurs at a later index
                digits[i], digits[last_occurrence[val]] = digits[last_occurrence[val]], digits[i]
                return int(''.join(map(str, digits)))
    return num


def maximum_swap_v2(num):
    """ Actually this problem can be easily solved by only one pass from backward. During the scan, we only need to do
        2 things:
        - Record the largest digit cur_max and its corresponding index max_index
        - If the current digit is smaller than the largest digit, this digit and the largest digit are the best
          candidates for max swap so far. In this case, this digit pair is recorded (left_index and right_index).
    Time complexity: O(N)
    Space complexity: O(1)
    """
    digits = [int(c) for c in str(num)]
    n = len(digits)
    cur_max, max_index = -1, 0
    left_index = right_index = 0
    for i in reversed(range(n)):
        cur_digit = digits[i]
        if cur_digit > cur_max:
            cur_max, max_index = cur_digit, i
        elif cur_digit < cur_max:
            # Best candidates for max swap if there is no more similar situation on the left side
            left_index = i
            right_index = max_index
    digits[left_index], digits[right_index] = digits[right_index], digits[left_index]
    return int(''.join(map(str, digits)))


class Test(unittest.TestCase):
    data = [(2736, 7236), (9973, 9973), (115, 511), (10909091, 90909011)]

    def test_maximum_swap(self):
        for test_num, result in self.data:
            self.assertEqual(result, maximum_swap_v1(test_num))
            self.assertEqual(result, maximum_swap_v2(test_num))


if __name__ == '__main__':
    unittest.main()
