""" Given a n x n matrix where each of the rows and columns are sorted in ascending order, find the kth smallest
element in the matrix.
Note that it is the kth smallest element in the sorted order, not the kth distinct element. """

from heapq import heappop, heappush
import unittest2 as unittest


def kth_smallest_v1(matrix, k):
    """ As each row (or column) of the given matrix can be seen as a sorted list, we essentially need to find the Kth
        smallest number in ‘N’ sorted lists.
        Before we get to this problem, let's first talk about a simpler version of the problem which is to find the
        Kth smallest element from amongst 2 sorted lists. This is easy enough to solve since all we need are a pair of
        pointers which act as indices in the two lists. At each step, we check which element is smaller amongst the two
        being pointed at by the indices and progress the corresponding index accordingly. We just need to run the
        algorithm for merging two sorted lists without actually merging them. We need to keep on running this algorithm
        until we find our Kth element.
        In this particular problem, we have N sorted lists instead of just 2. That's what adds to the complexity. We
        can't really keep N different pointers now, can we? The heap data structure is perfect for this problem since
        at all times, we want to maintain N different variables with each of them pointing to an element in their
        corresponding lists. We want to be able to find the minimum amongst these N pointers quickly and then replace
        that element with the next one in its corresponding list.
        We will take the first element of each row and add each of these elements to the heap. It's important to know
        what row and column an element belongs to. Without knowing that, we won't be able to move forward in that
        particular list. So, apart from adding an element to the heap, we also need to add its row and column number.
        Hence, our min-heap will contain a triplet of information (number, row, column). The heap will be arranged on
        the basis of the values and we will use the row and column number to add a replacement for the next element in
        case it gets popped off the heap.
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
        number, row, col = heappop(heap)  # Take the smallest (top) element from the min heap. If the running count is
        # equal to k, return the number. If the row of the top element has more elements, add the next element to the
        # heap
        if col + 1 < n:
            heappush(heap, (matrix[row][col + 1], row, col + 1))
    return number


def kth_smallest_v2(matrix, k):
    """ Since each row and column of the matrix is sorted, is it possible to use binary search to find the Kth smallest
        number?
        The biggest problem to use binary search in this case is that we don’t have a straightforward sorted array,
        instead we have a matrix. As we remember, in binary search, we calculate the middle index of the search space
        (1 to N) and see if our required number is pointed out by the middle index; if not we either search in the
        lower half or the upper half. In a sorted matrix, we can’t really find a middle. Even if we do consider some
        index as middle, it is not straightforward to find the search space containing numbers bigger or smaller than
        the number pointed out by the middle index.
        An alternate could be to apply the binary search on the VALUES RANGE instead of the INDEX RANGE. As we know
        that the smallest number of our matrix is at the top left corner and the biggest number is at the bottom lower
        corner. These two number can represent the range i.e., the start and the end for the binary search.
        Here is how our algorithm will work:
            1- Start the binary search with left = matrix[0][0] and right = matrix[n-1][n-1].
            2- Find middle of the left and the right. This middle number is NOT necessarily an element in the matrix.
            3- Count all the numbers smaller than or equal to middle in the matrix. As the matrix is sorted, we can do
               this in O(N).
            4- If the count is less than K, we can update left = mid+1 to search in the higher part of the matrix
            5- If the count is greater than or equal to K, we can update right = mid-1 to search in the lower part of
               the matrix in the next iteration.
        The element found by this algorithm has to be in the input matrix because the range converges to the minimum
        value that satisfies (or most closely follows) the condition count == K. The first value to satisfy count == K
        must be found in the range.
        If the mid value converges to an integer, a_mid, which is not the kth smallest element, a_k, in the array, then
        a_mid should be bigger than a_k, if not the count will be less than k and a_mid will increase.
        Therefore, left <= a_k < a_mid <= right will be true, and the loop ends at left = right, which means a_mid has
        to be equal to a_k.
        The result must be in the range of [min, max], and each iteration narrows the range of the [left, right] to
        exclude some potential answers. The termination condition of the iteration is left == right, so except the
        value of left, all other values are excluded, that makes left (or right) our answer.
        To sum up, 'left' is ensured to reach an authentic element in the matrix, because 'right' will approach and
        sit in the right spot anyway.
    Time complexity: O(N log(min-max))
    Space complexity: O(1)
    """

    def get_less_or_equal(val):
        res = 0
        row, col = n - 1, 0
        while row >= 0 and col < n:
            if matrix[row][col] > val:
                row -= 1
            else:
                res += row + 1  # If matrix[row][col] <= val, then all the elements on 'row' before column 'col'
                # (included) are smaller than or equal to val
                col += 1
        return res

    n = len(matrix)
    left, right = matrix[0][0], matrix[n - 1][n - 1]
    while left < right:
        mid = (left + right) // 2
        count = get_less_or_equal(mid)
        if count < k:
            left = mid + 1
        else:
            right = mid
    return left


class Test(unittest.TestCase):
    data = [([[1, 5, 9],
              [10, 11, 13],
              [12, 13, 15]
              ], 8, 13)]

    def test_kth_smallest(self):
        for test_matrix, test_k, result in self.data:
            self.assertEqual(result, kth_smallest_v1(test_matrix, test_k))
            self.assertEqual(result, kth_smallest_v2(test_matrix, test_k))


if __name__ == '__main__':
    unittest.main()
