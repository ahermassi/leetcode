""" Given two sparse matrices mat1 of size m x k and mat2 of size k x n, return the result of mat1 x mat2. You may
assume that multiplication is always possible. """


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
