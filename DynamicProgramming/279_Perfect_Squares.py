""" Given a positive integer n, find the least number of perfect square numbers (for example, 1, 4, 9, 16, ...) which
sum to n. """

import unittest as unittest


def num_squares_v1(n):
    """ Let dp[i] be the least number of perfect square numbers that sum up to i.
        There are multiple ways for perfect square numbers to sum up to i. The candidate way is to add a perfect square
        number j^2 to a sum of perfect square numbers that equals (i - j^2). It can be generalized as:
            i = (i- j^2) + j^2
        The least number of perfect square numbers that sum up to (i - j^2) is dp[i - j^2]. Therefore:
            dp[i] = min(dp[i - j^2] for valid values of j) + 1
        Add 1 because j^2 itself is a perfect square.
        At each iteration, i - j^2 has to be >= 0 because we're working only with positive integers.
        i - j^2 >= 0
        --> j^2 <= i
        --> j <= sqrt(i) = i^0.5
        For this reason, the second loop goes from 1 to sqrt(i)
    Time complexity: O(n sqrt(n)), in main step we have a nested loop, where the outer runs for n iterations and in the
    inner loop takes at maximum sqrt(n) iterations.
    Space complexity: O(n)
    """
    dp = [float('inf')] * (n + 1)
    dp[0] = 0
    for i in range(1, n + 1):
        for j in range(1, int(i ** 0.5) + 1):
            dp[i] = min(dp[i], dp[i - j ** 2] + 1)
    return dp[n]


def num_squares_v2(n):
    """ The basic idea of this solution is a BSF search for shortest path.
        The root node is n, and we are trying to keep reducing a perfect square number from it at each layer. So the
        next layer nodes are {n - i**2 for i in range(1, int(n**0.5)+1)}. And target leaf node is 0, indicates n is
        made up of a number of perfect square numbers and depth is the least number of perfect square numbers.
    Time complexity: O(n), sqrt(n) elements in the queue checked sqrt(n) times (length of perfect_squares list)
    Space complexity: O(sqrt(n))
    """
    perfect_squares = [i * i for i in range(1, int(n ** 0.5) + 1)]  # These are the candidate perfect squares that n can
    # be made of: all squares less than or equal to n
    queue, count = {n}, 0  # queue holds the intermediate integers that result from reducing n by (n - perfect square).
    # The same process is applied to those intermediate results until 0 is found. We use a set data structure to
    # eliminate the duplicate integers. Example: n = 12, perfect_squares = [1, 4, 9]. In second iteration, 11 - 4 = 7
    # and 8 - 1 = 7 as well (see execution tree in notes)
    while queue:
        count += 1  # A new depth: count + 1
        new_queue = set()
        for i in queue:
            for j in perfect_squares:
                if i == j:  # 0 is found: i - j == 0
                    return count
                if j > i:  # (i - j) would result in a negative integer
                    break
                new_queue.add(i - j)
        queue = new_queue
    return count


class Test(unittest.TestCase):
    data = [(12, 3), (13, 2)]

    def test_num_squares(self):
        for test_number, result in self.data:
            self.assertEqual(result, num_squares_v1(test_number))
            self.assertEqual(result, num_squares_v2(test_number))


if __name__ == '__main__':
    unittest.main()