""" Read description on Leetcode """


# Definition for a QuadTree node.
class Node(object):
    def __init__(self, val, isLeaf, topLeft, topRight, bottomLeft, bottomRight):
        self.val = val
        self.isLeaf = isLeaf
        self.topLeft = topLeft
        self.topRight = topRight
        self.bottomLeft = bottomLeft
        self.bottomRight = bottomRight


# Video explanation: https://youtu.be/UQ-1sBMV0v4
def construct_v1(grid):
    """ We have a square matrix of size N * N of 0's and 1's. We need to convert this matrix to a quad tree with nodes
         having two attributes, val and isLeaf:

            1- If the whole matrix has the same value (0 or 1), then isLeaf would be true and val would be the same as
                 the matrix value, and we can return.
            2- Otherwise, it's not a leaf node, so isLeaf would be false, and val will not matter. This node will have
                 four child nodes.
            3- Divide the current matrix into four equally sized square matrices and recurse the same process to each.

        We can see in that the matrix is repeatedly divided into 4 sub-parts again and again. It suggests we use a
        recursive approach to divide the current matrix into 4 equal parts and then again repeat the same division on
        smaller parts recursively.

        The most intuitive way of solving recursive problems like this is to perform what the problem description says
        and just follow the same recursive approach. Before we start the process, we need a way to define the current
        state of the matrix to generate the following states from it.

        The given matrix is square; we can represent it using two coordinates such as the top-left and bottom-right.
        Though this would be correct too, for simplicity, we will use only one top-left coordinate and another variable,
        side_length, which will be the side of the square. Using these two pieces of information, we can find any corner
        coordinate of the square.

            - If the matrix contains only 0 or 1, then we can return. Notice that this is the base condition, we can
               simply check all the values of the current matrix state, and if it has all the same values, we will
               simply return the node with specified attributes.

            - If not, then we need to divide the matrix into 4 equal parts and follow the above process to each of the
               4 separately, and then they would become the four child nodes. The four matrices would have the top-left
               coordinates, and each of them would have the length of the side as side_length / 2. Therefore, we will
               call the recursive function for each sub-matrix and assign the returned nodes as the child of the root
               node we will return.
               For each recursive call at position (i,j), where i is the row index and j is the column index of the
               top-left corner of the current sub-grid, we have the following:

                    * Top-left matrix has top-left coordinate as (i, j)
                    * Top-right matrix has top-left coordinate as (i, j + side_length / 2)
                    * Bottom-left matrix has top-left coordinate as (i + side_length / 2, j)
                    * Bottom-right matrix has top-left coordinate as (i + side_length / 2, j + side_length / 2)

    Time complexity: O(N^2 * logN), after every level of recursion the original length of matrix get reduced to half,
    this implies that the size of matrix will be reduced down to 1 after logN iterations. At each of these logN
    iterations, we will have some number of recursive calls for the current matrix size. For example, initially we have
    one call for the size of matrix N * N, then we will have four recursive calls each for matrix of size ( N * N)/4 and
    so on. At each level the total number of iterations over the matrix cells remains same at N^2. Hence, N^2 iterations
    at each of the logN levels makes up the time complexity to be O(N^2 * logN).
    Space complexity: O(logN), for the recursion call stack; the maximum number of active stack calls is logN
    """

    def dfs(i, j, side_length):
        all_same_value = True
        for x in range(i, i + side_length):
            for y in range(j, j + side_length):
                if grid[x][y] != grid[i][j]:
                    all_same_value = False
                    break
        if all_same_value:
            return Node(grid[i][j], True, None, None, None, None)
        topLeft = dfs(i, j, side_length // 2)
        topRight = dfs(i, j + side_length // 2, side_length // 2)
        bottomLeft = dfs(i + side_length // 2, j, side_length // 2)
        bottomRight = dfs(i + side_length // 2, j + side_length // 2, side_length // 2)
        return Node(grid[i][j], False, topLeft, topRight, bottomLeft, bottomRight)

    return dfs(0, 0, len(grid))


def construct_v2(grid):
    """ Use the results of recursive calls to improve time complexity. Each cell is examined only once.
    Time complexity: O(N ** 2)
    Space complexity: O(log N), where log is base 4
    """

    def helper(x, y, length):
        if length == 1:
            return Node(grid[0][0] == 1, True, None, None, None, None)
        root = Node(grid[0][0] == 1, False, None, None, None, None)
        topLeft = helper(x, y, length // 2)
        topRight = helper(x, y + length // 2, length // 2)
        bottomLeft = helper(x + length // 2, y, length // 2)
        bottomRight = helper(x + length // 2, y + length // 2, length // 2)
        if topLeft.isLeaf and topRight.isLeaf and bottomLeft.isLeaf and bottomRight.isLeaf and topLeft.val == \
                topRight.val and topRight.val == bottomLeft.val and bottomLeft.val == bottomRight.val:
            root.isLeaf = True
            root.val = topLeft.val
        else:
            root.topLeft = topLeft
            root.topRight = topRight
            root.bottomLeft = bottomLeft
            root.bottomRight = bottomRight
        return root

    return helper(0, 0, len(grid))

