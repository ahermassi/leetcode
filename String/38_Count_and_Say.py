""" The count-and-say sequence is the sequence of integers with the first five terms as following:
1.     1
2.     11
3.     21
4.     1211
5.     111221
1 is read off as "one 1" or 11.
11 is read off as "two 1s" or 21.
21 is read off as "one 2, then one 1" or 1211.
Given an integer n where 1 ≤ n ≤ 30, generate the nth term of the count-and-say sequence.  """

import unittest2 as unittest


def count_and_say_v1(n):
    """ To generate the nth term, just count and say the (n-1)th term. We can do it recursively.
        Actually, we could consider this problem as a naive compression algorithm for a sequence of numbers.
        Given two adjacent sequences of number, [S_n, S_n+1], there exists a pattern that can produce the sequence
        S_n+1 from its previous sequence S_n. More specifically, we can consider the sequence S_n+1 as a sort of
        summary to its previous sequence S_n, i.e. S_n+ contains a list of pairs as |count,digit∣ which encodes all the
        information about its previous sequence S_n.
    Time complexity: the precise time complexity is a function of the lengths of the terms, which is extremely hard to
    analyze. Each successive number can have at most twice as many digits as the previous number. This happens when all
    digits are different. This means the maximum length number has length no more than 2^n. Since there are n recursive
    calls and the work in each call is proportional to the length of the number computed, a simple bound on the time
    complexity is O(n * 2^n).
    Space complexity: O(n)
    """
    if n == 1:
        return '1'
    pre = count_and_say_v1(n-1)  # We're going to count and say the (n-1)th term
    i, j, n = 0, 0, len(pre)
    res = ''
    while i < n:
        while j < n and pre[i] == pre[j]:  # We keep a sliding window of identical digits with left=i and right=j
            j += 1
        res += str(j-i) + pre[i]
        i = j  # Slide the window
    return res


def count_and_say_v2(n):
    """ We compute the nth number by iteratively applying the rule (n - 1) times.
    Time complexity: O(n * 2^n)
    Space complexity: (n)
    """
    s = '1'  # Base case
    for _ in range(n-1):
        n, i, j, temp = len(s), 0, 0, ''
        while i < n:
            while j < n and s[i] == s[j]:  # We keep a sliding window of identical digits with left=i and right=j
                j += 1
            temp += str(j - i) + s[i]
            i = j
        s = temp  # We assign the result of transformation to s to be used in the next iteration
    return s


class Test(unittest.TestCase):
    data = [(3, '21'), (4, '1211')]

    def test_count_and_say(self):
        for test_n, result in self.data:
            self.assertEqual(result, count_and_say_v1(test_n))
            self.assertEqual(result, count_and_say_v2(test_n))


if __name__ == '__main__':
    unittest.main()
