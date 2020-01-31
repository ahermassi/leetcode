""" Implement an algorithm that takes as input an array of distinct elements and a size, and returns a subset of the
given size of the array elements. All subsets should be equally likely. """

from random import randint


def random_sampling_v1(A, k):
    """ The key to efficiently building a random subset of size exactly k is to first build one of size (k - 1) and
        then adding one more element, selected randomly from the rest.
        We begin by choosing one element at random and we now repeat the same process with the (n - 1) element
        sub-array A[1, n - 1]. Eventually, the random subset occupies the slots A[0, k - 1] and the remaining elements
        are in the last (n - k) slots.
        Intuitively, if all subsets of size k are equally likely, then the construction process ensures that the
        subsets of size (k + 1( are also equally likely.
        As a concrete example, let the input be A = [3, 7, 5, 11] and the size k = 3.
        In the first iteration, we use the random number generator to pick a random integer in the interval [0, 3].
        Let the returned random number be 2. We swap A[0] with A[2]. Now the array is [5, 7, 3, 11].
        Now we pick a random integer in the interval [1, 3]. Let the returned random number be 3. We swap A[1] with
        A[3]. Now the resulting array is [5, 11, 3, 7].
        Now we pick a random integer in the interval [2, 3]. Let the returned random number be 2. When we swap A[2]
        with itself, the resulting array is unchanged.
        The random subset consists of the first three entries, i.e., [5, 11, 3]
    Time complexity: O(k)
    Space complexity: O(1)
    """
    for i in range(k):
        r = randint(i, len(A) - 1)
        A[i], A[r] = A[r], A[i]
    return A[:k]