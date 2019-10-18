""" In a row of dominoes, A[i] and B[i] represent the top and bottom halves of the i-th domino.  (A domino is a tile
with two numbers from 1 to 6 - one on each half of the tile.)
We may rotate the i-th domino, so that A[i] and B[i] swap values.
Return the minimum number of rotations so that all the values in A are the same, or all the values in B are the same.
If it cannot be done, return -1. """

from collections import Counter, defaultdict
import unittest2 as unittest


def min_domino_rotations_v1(A, B):
    """ Pick up the first element. It has two sides: A[0] and B[0].
        Check if we could make all elements in A row or B row to be equal to A[0]. If yes, return the minimum number
        of rotations needed.
        Otherwise, check if we could make all elements in A row or B row to be equal to B[0]. If yes, return the
        minimum number of rotations needed.
        Otherwise return -1.
    Time complexity: O(N), where N is the length of A (and B)
    Space complexity: O(1)
    """

    def rotate(val):
        rotate_a = rotate_b = 0
        for i in range(n):
            if A[i] != val and B[i] != val:
                return -1
            if A[i] != val:
                rotate_a += 1
            elif B[i] != val:
                rotate_b += 1
        return min(rotate_a, rotate_b)

    n = len(A)
    rotations = rotate(A[0])
    if rotations != -1 or A[0] == B[0]:  # Second condition prevents the second check from running, since B[0] is
        # passed in for the second check
        return rotations  # If A[0] works, no need to check B[0]. Because if both A[0] and B[0] exist in all
        # dominoes, when we swap A[0] in a whole row, we will swap B[0] in a whole at the same time. The result of
        # trying A[0] and B[0] will be the same.
    return rotate(B[0])


def min_domino_rotations_v2(A, B):
    """ Count the occurrence of all numbers in A and B, and also the intersection of A and B.
        Try all possibilities from 1 to 6. If we can make number i in a whole row, it MUST satisfy:
            countA[i] + countB[i] - intersection[i] = n
        It is like finding the union of two sets A and B <=> A + B - (A & B)
    Time complexity: O(N)
    Space complexity: O(1)
    """
    if len(A) != len(B):
        return -1
    n, counter_a, counter_b = len(A), Counter(A), Counter(B)
    intersection = defaultdict(int)
    for a, b in zip(A, B):
        if a == b:
            intersection[a] += 1
    for i in range(1, 7):
        if counter_a[i] + counter_b[i] - intersection[i] == n:
            return min(counter_a[i], counter_b[i]) - intersection[i]  # When the condition is met, we have 2 options:
            # either swap A's elements or swap B's elements, the intersection elements stay as they are. We choose
            # the minimum number of swaps which corresponds to the minimum number of occurrences of i in A or B.
    return -1


class Test(unittest.TestCase):
    data = [([2, 1, 2, 4, 2, 2], [5, 2, 6, 2, 3, 2], 2), ([3, 5, 1, 2, 3], [3, 6, 3, 3, 4], -1)]

    def test_min_domino_rotations(self):
        for test_a, test_b, result in self.data:
            self.assertEqual(result, min_domino_rotations_v1(test_a, test_b))
            self.assertEqual(result, min_domino_rotations_v2(test_a, test_b))


if __name__ == '__main__':
    unittest.main()
