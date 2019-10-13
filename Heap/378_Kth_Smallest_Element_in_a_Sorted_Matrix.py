""" Given a n x n matrix where each of the rows and columns are sorted in ascending order, find the kth smallest
element in the matrix.
Note that it is the kth smallest element in the sorted order, not the kth distinct element. """

from heapq import heapify, heappop, heappush
import unittest2 as unittest


def kth_smallest(matrix, k):
    """ As each row (or column) of the given matrix can be seen as a sorted list, we essentially need to find the Kth
        smallest number in ‘N’ sorted lists.
        Build a minHeap of elements from the first column (every row/column is a sorted array) (could be done with
        first row as well, same logic)
        Do the following operations k times :
        Every time when you poll out the root (top Element in Heap), you need to know the row number and column number
        of that element. Replace that root with the next element from the same row (which is a sorted array).
    Time complexity: O(k logN), First, we inserted N elements from each of the ‘N’ rows, which will take O(N). Then we
    went through at most K elements in the matrix and removed/added one element in the heap in each step. As we can’t
    have more than N elements in the heap in any condition, therefore, the overall time complexity of the above
    algorithm will be O(N + k logN)
    Space complexity: O(N) for the heap
    """
    heap = [(row[0], i, 0) for i, row in enumerate(matrix)]  # Put the 1st element of each column in the min heap
    heapify(heap)
    n, res = len(matrix[0]), 0
    for _ in range(k):
        res, row, col = heappop(heap)  # Take the smallest (top) element form the min heap, if the running count is
        # equal to k return the number. If the row of the top element has more elements, add the next element to the
        # heap
        if col + 1 < n:
            heappush(heap, (matrix[row][col + 1], row, col + 1))
    return res


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
