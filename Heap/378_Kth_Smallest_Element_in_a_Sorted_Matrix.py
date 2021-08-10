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
    Time complexity: O(N + k logN), First, we inserted N elements from each of the ‘N’ rows, which will take O(N).
    Then we went through at most K elements in the matrix and removed/added one element in the heap in each step. As
    we can’t have more than N elements in the heap in any condition, therefore, the overall time complexity of the above
    algorithm will be O(N + k logN)
    Space complexity: O(N), for the heap
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
        number? The biggest problem in using binary search in this case is that we don’t have a straightforward sorted
        array, instead we have a matrix. As we remember, in binary search, we calculate the middle index of the search
        space (1 to N) and see if our required number is pointed out by the middle index. If not, we either search in
        the lower half or the upper half. In a sorted matrix, we can’t really find a middle. Even if we do consider some
        index as middle, it is not straightforward to find the search space containing numbers bigger or smaller than
        the number pointed out by the middle index.
        An alternate could be to apply the binary search on the VALUES RANGE instead of the INDICES RANGE. As we know
        that the smallest number of our matrix is at the top left corner and the biggest number is at the bottom lower
        corner. These two numbers can represent the range i.e. the start and the end for the binary search.
        Here is how our algorithm will work:
            1- Start the binary search with left = matrix[0][0] and right = matrix[n-1][n-1].
            2- In a normal, one-dimensional binary search, we use the indices to find the middle element. In this case,
               the left and the right ends of our sorted matrix are the two values. So, we use them to find the
               hypothetical middle of the matrix. The reason we call this hypothetical is because it is NOT necessary
               that the middle value will exist in the matrix.
            3- Count all the numbers smaller than or equal to middle in the matrix. As the matrix is sorted, we can do
               this in O(N). So, after finding the middle element, we need to determine the size of the left half. Why,
               you might ask? Well, because we want the Kth smallest element and not the largest. If the question asked
               us for the largest, we would be determining the size of the right half.
            4- While counting, we need to keep track of the smallest number greater than the middle (let’s call it R)
               and at the same time the biggest number less than or equal to the middle (let’s call it L). These two
               numbers will be used to adjust the number range for the binary search in the next iteration.
            5- If the count is equal to K, L will be our required number as it is the biggest number less than or equal
               to the middle, and is definitely present in the matrix.
            6- If the count is less than K, we can update left = R to search in the higher part of the matrix
            7- If the count is greater K, we can update right = L to search in the lower part of the matrix
        How to count the number of elements less than or equal to x efficiently?
        Since the matrix is sorted in ascending order by rows and columns, we use two pointers, one points to the
        rightmost column c = m-1, and one points to the first row r = 0.
            - If matrix[r][c] <= x then the number of elements in row r less or equal to x is (c + 1) because row[r] is
              sorted in ascending order, so if matrix[r][c] <= x then matrix[r][c-1] is also <= x. Then we move down to
              next row to continue counting.
            - If matrix[r][c] > x, we decrease column c (move left) until matrix[r][c] <= x
    Time complexity: O(N log(max - min)), we are defining our binary search space in terms of the minimum and the
    maximum numbers in the matrix. The complexity for our binary search should be O(log(max − min)) where 'max' is the
    maximum element in the array and 'min' is the minimum element. In each iteration of the binary search approach, we
    iterate over the matrix trying to determine the size of the left half as explained above. That takes O(N).
    Space complexity: O(1)
    """

    def get_less_or_equal(mid):
        count = 0
        smallest_greater_than_mid, largest_smaller_than_mid = float('inf'), float('-inf')
        row, col = 0, m - 1
        while row < n and col >= 0:
            if matrix[row][col] > mid:  # As matrix[row][col] is bigger than the mid, let's keep track of the smallest
                # number greater than mid
                smallest_greater_than_mid = min(smallest_greater_than_mid, matrix[row][col])
                col -= 1
            else:
                count += col + 1  # If matrix[row][col] <= val, then all the elements in the row 'row' before this
                # element i.e. (col) other elements in this row are also going to be less than this element.
                # Why? Because the rows are sorted as well!
                largest_smaller_than_mid = max(largest_smaller_than_mid, matrix[row][col])  # As matrix[row][col] is
                # less than or equal to the mid, let's keep track of the biggest number less than or equal to the mid
                row += 1
        return count, smallest_greater_than_mid, largest_smaller_than_mid

    n, m = len(matrix), len(matrix[0])
    left, right = matrix[0][0], matrix[n - 1][n - 1]
    while left < right:
        mid = (left + right) // 2
        count, smallest_greater_than_mid, largest_smaller_than_mid = get_less_or_equal(mid)
        if count == k:
            return largest_smaller_than_mid
        if count < k:
            left = smallest_greater_than_mid
        else:
            right = largest_smaller_than_mid
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
