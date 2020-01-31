""" A permutation can be specified by an array P, where P[i] represents the location of the element at i in the
permutation. For example, the array (2,0,1,3) represents the permutation that maps the element at location 0 to
location 2, the element at location 1 to location 0, the element at location 2 to location 1, and keep the element at
location 3 unchanged. A permutation can be applied to an array to reorder the array
Given an array A of n elements and a permutation P, apply P to A.

Note: this is not a backtracking problem. It was moved to be closer to the other permutation problem.
"""


def apply_permutation(perm, A):
    """ Decompose permutations into simpler structures which can be processed incrementally. For example, consider
        the permutation [3, 2, 1, 0]. To apply it to an array [a, b, c, d], we move the element at index 0 (a) to index
        3 and the element already at index 3 (d) to index 0. Continuing, we move the element at index 1 (b) to index 2
        and the element already at index 2 (c) to index 1. Now all elements have been moved according to the
        permutation, and the result is [d, c, b, a].
        This example generalizes: every permutation can be represented by a collection of independent permutations,
        each of which is cyclic, that is, it moves all elements by a fixed offset, wrapping around.
        To find and apply the cycle that includes entry i, we just keep going forward (from i to P[i]) till we get
        back to i. After we are done with that cycle, we need to find another cycle that has not yet been applied.
        One way to perform this without explicitly using additional O(n) storage is to use the sign bit in the entries
        in the permutation array. Specifically, we subtract n from P[i] after applying it. This means that if an entry
        in P[i] is negative, we have performed the corresponding move.
        For example, to apply [3, 1, 2, 0], we begin with the first entry, 3. We move A[0] to A[3], first saving the
        original A[3]. We update the permutation to [-1, 1 , 2, 0]. We move A[3] to A[0]. Since P[0] is negative we
        know we are done with the cycle starting at 0. We also update the permutation to [-1, 1, 2, -4].
        Now we examine  P[1]. Since it is not negative, it means the cycle it belongs to cannot have been applied.
        We continue as before.
    Time complexity: O(N)
    Space complexity: O(1)
    """
    n = len(A)
    for i in range(n):
        next = i
        while perm[next] >= 0:  # Following the current cycle that starts at index i
            A[i], A[perm[next]] = A[perm[next]], A[i]  # Perform the local permutation (swap)
            temp = perm[next]
            perm[next] -= n  # Subtracts n from the entry in perm to make it negative, which indicates the
            # corresponding move has been performed.
            next = temp  # Continue the cycle
    perm[:] = [val + n for val in perm]  # Restore perm



