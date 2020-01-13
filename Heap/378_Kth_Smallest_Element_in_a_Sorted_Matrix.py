""" Given a n x n matrix where each of the rows and columns are sorted in ascending order, find the kth smallest
element in the matrix.
Note that it is the kth smallest element in the sorted order, not the kth distinct element. """

from heapq import heappop, heappush
import unittest2 as unittest


def kth_smallest(matrix, k):
    """ As each row (or column) of the given matrix can be seen as a sorted list, we essentially need to find the Kth
        smallest number in ‘N’ sorted lists.
        Build a min heap of elements from the first column (every row/column is a sorted array) (could be done with
        first row as well, same logic)
        Do the following operations k times :
        Every time when we poll out the root (top element in heap), we need to know the row number and column number
        of that element. Replace that root with the next element from the same row (which is a sorted array).
        The invariant of the algorithm is:
            At iteration i, the front of the heap is the (i+1)th smallest element in the matrix (i is 0-based)
        Think of the first element of each column (or row) we initially push to the heap as a representative of each
        column (or row). Each row (or column) keeps bringing the next greater element and the heap adjusts accordingly
        to keep the smallest in the front. As we know, the smallest element in the matrix is at the top left corner,
        so no matter what our choice was (pushing first element of each row or column), the very first element in the
        heap will be always the absolute smallest.
    Time complexity: O(k logN), First, we inserted N elements from each of the ‘N’ rows, which will take O(N). Then we
    went through at most K elements in the matrix and removed/added one element in the heap in each step. As we can’t
    have more than N elements in the heap in any condition, therefore, the overall time complexity of the above
    algorithm will be O(N + k logN)
    Space complexity: O(N) for the heap
    """
    heap = []
    for i, row in enumerate(matrix):  # Push the 1st element of each row (= 1st column) to the min heap
        heappush(heap, (row[0], i, 0))
    n, number = len(matrix[0]), 0
    for _ in range(k):
        number, row, col = heappop(heap)  # Take the smallest (top) element form the min heap. If the running count is
        # equal to k return the number. If the row of the top element has more elements, add the next element to the
        # heap
        if col + 1 < n:
            heappush(heap, (matrix[row][col + 1], row, col + 1))
    return number


class Test(unittest.TestCase):
    data = [([[1, 5, 9],
              [10, 11, 13],
              [12, 13, 15]
              ], 8, 13)]

    def test_kth_smallest(self):
        for test_matrix, test_k, result in self.data:
            self.assertEqual(result, kth_smallest(test_matrix, test_k))


if __name__ == '__main__':
    unittest.main()
