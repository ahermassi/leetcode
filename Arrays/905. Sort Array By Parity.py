def sort_array_by_parity(A):
    """
    Given an array A of non-negative integers, return an array consisting of all the even elements of A,
    followed by all the odd elements of A.
    :type A: List[int]
    :rtype: List[int]
    Time complexity: O(N) where N is the number of elements in A
    Space complexity: O(1) since it's in-place
    """
    i, j = 0, 1  # Keep two pointers
    while i < len(A) and j < len(A):
        if A[i] % 2 == 0:  # If even, move on
            i += 1
        elif A[j] % 2 == 0:  # Else, start looking for even and swap
            A[i], A[j] = A[j], A[i]
            i += 1
        j += 1
    return A


def sort_array_by_parity_v2(A):
    """
    Given an array A of non-negative integers, return an array consisting of all the even elements of A,
    followed by all the odd elements of A.
    :type A: List[int]
    :rtype: List[int]
    Time complexity: O(N) where N is the number of elements in A
    Space complexity: O(1) since it's in-place
    """
    A.sort(key=lambda x: x % 2)
    # This one is smart. In fact, applying that key returns either 0 or 1 (even or odd element). Since we want even
    # numbers to appear first, we sort in increasing order.


if __name__ == '__main__':
    A = [3, 1, 2, 4]
    print('Array before sorting: ', A)
    sort_array_by_parity_v2(A)
    print('Array after sorting: ', A)

