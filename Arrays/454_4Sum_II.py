""" Given four lists A, B, C, D of integer values, compute how many tuples (i, j, k, l) there are such that
A[i] + B[j] + C[k] + D[l] is zero.
To make problem a bit easier, all A, B, C, D have same length of N where 0 ≤ N ≤ 500. All integers are in the range
of -228 to 228 - 1 and the result is guaranteed to be at most 2^31 - 1. """

from collections import defaultdict
import unittest2 as unittest


def four_sum_count(A, B, C, D):
    """ We aim to find all possible A[i] + B[j] + C[k] + D[l] = 0, such that A[i] + B[j] = -(C[k] + D[l]). In other
        words, we need to count the number of all possible two-sums between A and B that equal the opposite of any
        two-sum between C and D.
        Thus, we enumerate all two-sums between A and B and store sum-to-frequency mappings for reference.
        Compute all the possible sums of the arrays C and D. If the hash map contains the opposite value of the current
        sum, increase the count of four elements sum to 0 by the counter in the map.
        The trick behind the scene is similar to dynamic programming. Why?
        Because for A and B (which two doesn't matter), if the sum of A[i] and B[j] equals A[m] + B[n], if A[i] and
        B[j] is calculated for every element in C and D iteratively, we don't have to calculate A[m] + B[n] because
        the case is just the same. So first we would store the sum occurrences hash map to mark the number of
        occurrences of a given sum for A and B, so next time we don't have to iterate the A and B for every element
        pair in C and D. The only thing we need to do is check if there exists the key-value pair in hash map where the
        key equals the negative of current sum of element pair in C and D.
        It doesn't matter which pair of arrays we choose to store in the hash map (A, B), (B, D), etc. Think about the
        solution where we have 4 for-loops to compare all the sums. It's comparing every sum of A[a] and B[b] with
        C[c] and D[d]. Since it's comparing every A[a] + B[b] with every C[c] + D[d], why don't we just pre-compute
        every A[a] + B[b] and store those results? This'll save us a lot of time.
    Time complexity: O(N^2)
    Space complexity: O(N^2)
    """
    two_sum, res = defaultdict(int), 0
    for a in A:
        for b in B:
            two_sum[a + b] += 1
    for c in C:
        for d in D:
            if -(c + d) in two_sum:
                res += two_sum[-(c + d)]
    return res


class Test(unittest.TestCase):
    data = [([1, 2], [-2, -1], [-1, 2], [0, 2], 2)]

    def test_four_sum_count(self):
        for test_a, test_b, test_c, test_d, result in self.data:
            self.assertEqual(result, four_sum_count(test_a, test_b, test_c, test_d))


if __name__ == '__main__':
    unittest.main()
