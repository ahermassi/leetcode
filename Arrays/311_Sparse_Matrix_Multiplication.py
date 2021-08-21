""" Given two sparse matrices mat1 of size m x k and mat2 of size k x n, return the result of mat1 x mat2. You may
assume that multiplication is always possible. """

from collections import defaultdict


def multiply_v1(mat1, mat2):
    """ Brute force.
        The normal way of multiplying two metrics A and B is as follow:
        We take the the all values from the first row of A, and all values from the first column of B, and multiply the
        corresponding values and sum them up. The final sum is the value for the location of first column and first row
        in final result matrix. Similarly, the value at [i][j] of result matrix C, which is C[i][j], is calculated as:

            C[i][j] = A[i][0] * B[0][j] + A[i][1] * B[1][j] + A[i][2] * B[2][j] + ... A[i][k] * B[k][j]

        Which is the sum of each multiplication of corresponding k values from row i of A and k values from column j
        of B.
    Time complexity: O(N * M * L)
    Space complexity: O(1)
    """
    rows_a, cols_a, cols_b = len(mat1), len(mat1[0]), len(mat2[0])
    res = [[0] * cols_b for _ in range(rows_a)]
    for i in range(rows_a):
        for j in range(cols_b):
            for k in range(cols_a):
                res[i][j] += mat1[i][k] * mat2[k][j]
    return res


def multiply_v2(mat1, mat2):
    """ Optimized brute force.
        The key part of this solution is that it does not calculate the final result at once, but it takes each value
        from A and calculates and partial sum and accumulates it into the final spot.
        If A[i][k] == 0, we skip the multiplication . This is achieved by moving the innermost loop to the middle so
        that we can check whether A[i][k] == 0.
        For each value A[i][k], if it is non-zero, it will be used at most cols_b times (cols_b = B[0].length ), which
        can be illustrated as follows:
        Generally for the following equation:
        C[i][j] = A[i][0] * B[0][j] + A[i][1] * B [1][j] + A[i][2] * B[2][j] + ... A[i][k] * B[k][j]
        j can be from 0 to cols_b, so if we write all of them down, it will look like the following:
        For j from 0 to cols_b:

            C[i][0] = A[i][0] * B[0][0] + A[i][1] * B[1][0] + A[i][2] * B[2][0] + ... A[i][k] * B[k][0]
            C[i][1] = A[i][0] * B[0][1] + A[i][1] * B[1][1] + A[i][2] * B[2][1] + ... A[i][k] * B[k][0]
            ...
            C[i][cols_b] = A[i][0] * B[0][cols_b] + A[i][1] * B[1][cols_b] + A[i][2] * B[2][cols_b] + ... A[i][k] * B[k][cols_b]

        As we can see from above, the same value A[i][k] from the first matrix  will be used at most cols_b times if
        A[i][k] is non-zero. This solution is taking advantage of that.
        For each value A[i][k] in matrix A, if it is not zero, we calculate A[i][k] * B[k][j] and accumulate it into
        C[i][j]. The key observation is that C[i][j] by now is not the final value in the result matrix. C[i][j] is
        only sum of some multiplication values.
    Time complexity: O(N * M * L)
    Space complexity: O(1)
    """
    rows_b, cols_b = len(mat2), len(mat2[0])
    rows_a, cols_a, cols_b = len(mat1), len(mat1[0]), len(mat2[0])
    res = [[0] * cols_b for _ in range(rows_a)]
    for i in range(rows_a):
        for k in range(rows_b):
            if mat1[i][k]:
                for j in range(cols_b):
                    res[i][j] += mat1[i][k] * mat2[k][j]
    return res


def multiply_v3(mat1, mat2):
    """ A sparse matrix can be represented as a grouping of ((row index, col_index): value) pairs of the nonzero values
        in the matrix.
    Time complexity: O(N * M)
    Space complexity: O(N * M)
    """

    def collect_non_zeros(mat):
        n, m = len(mat), len(mat[0])
        elements = dict()
        for i in range(n):
            for j in range(m):
                if mat[i][j]:
                    elements[(i, j)] = mat[i][j]
        return elements

    elements_a, elements_b = collect_non_zeros(mat1), collect_non_zeros(mat2)
    rows_a, cols_b = len(mat1), len(mat2[0])
    res = [[0] * cols_b for _ in range(rows_a)]
    for (row_a, col_a), val_a in elements_a.items():
        for (row_b, col_b), val_b in elements_b.items():
            if col_a == row_b:
                res[row_a][col_b] += val_a * val_b
    return res


def multiply_v4(mat1, mat2):
    """ A sparse matrix can be represented as a sequence of rows, each of which is a sequence of (column index, value)
        pairs of the nonzero values in the row. So let's create a non-zero map for B and do multiplication on A.
    Time complexity: O(N * M)
    Space complexity: O(N * M)
    """

    def collect_non_zeros(mat):
        n, m = len(mat), len(mat[0])
        elements = defaultdict(dict)
        for i in range(n):
            for j in range(m):
                if mat[i][j]:
                    elements[i][j] = mat[i][j]
        return elements

    elements_b = collect_non_zeros(mat2)
    rows_a, cols_a = len(mat1), len(mat1[0])
    rows_b, cols_b = len(mat2), len(mat2[0])
    res = [[0] * cols_b for _ in range(rows_a)]
    for i in range(rows_a):
        for k in range(cols_a):
            if mat1[i][k]:
                for j, val in elements_b[k].items():  # In row k, iterate only over indexes that have non-zero values
                    res[i][j] += val * mat1[i][k]
    return res
