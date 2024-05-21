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
    """ We have a square matrix of size N*N of 0's and 1's. We need to convert this matrix into a quad tree with nodes
         having two attributes, val and isLeaf:

            1- If the entire matrix has the same value (0 or 1), then isLeaf would be true and val would be the same as
                 the matrix value, and we can return.

            2- Otherwise, it's not a leaf node, so isLeaf would be false, and val will not matter. This node will have
                 four children nodes.

            3- Divide the current matrix into 4 equally sized square matrices and apply the same process to each.

        We can see that the matrix is repeatedly divided into 4 sub-parts again and again. It suggests the use of a
        recursive approach to divide the current matrix into 4 equal parts and then again repeat the same division on
        smaller parts recursively.

        The most intuitive way of solving recursive problems like this is to perform what the problem description says
        and just follow the same recursive approach. Before we start the process, we need a way to define the current
        state of the matrix in order to generate the following states from it.

        The given matrix is square; we can represent it using two coordinates such as the top-left and bottom-right.
        Though this is correct too, for simplicity we can use only one top-left coordinate and another variable,
        side_length, which represents the side of the square. Using these two pieces of information, we can find any
        corner coordinate of the square.

            - If the matrix contains only 0's or 1's, then we can return. Notice that this is the base condition, we can
               check all the values of the current matrix state.

            - Otherwise, we need to divide the matrix into 4 equal parts and apply the above process to each of the 4
               separately, and then they would become the 4 children nodes. The four matrices would have the top-left
               coordinates, and each of them would have the length of the side as side_length / 2. Therefore, we call
               the recursive function for each sub-matrix and assign the returned nodes as the children of the root
               node.
               For each recursive call at position (i,j), where i is the row index and j is the column index of the
               top-left corner of the current sub-grid, we have the following:

                    * Top-left matrix has top-left coordinate (i, j)
                    * Top-right matrix has top-left coordinate (i, j + side_length / 2)
                    * Bottom-left matrix has top-left coordinate (i + side_length / 2, j)
                    * Bottom-right matrix has top-left coordinate (i + side_length / 2, j + side_length / 2)

    Time complexity: O(N^2 * logN), after every level of recursion the original length of matrix gets reduced to half,
    this implies that the size of matrix will be reduced down to 1 after logN iterations. At each of these logN
    iterations, we have a number of recursive calls for the current matrix size. For example, we initially have one call
    for the matrix of size N*N, then we have 4 recursive calls each matrices of size (N*N)/4 and so on. At each level,
    the total number of iterations over the matrix cells remains the same N^2. Hence, N^2 iterations at each of the logN
    levels makes a time complexity of O(N^2 * logN).
    Space complexity: O(logN), for the recursion call stack; the maximum number of active stack calls is logN
    """

    def dfs(top, left, side_length):
        if side_length == 1:
            return Node(grid[top][left], True, None, None, None, None)
        all_same_value = True
        for i in range(top, top + side_length):
            for j in range(left, left + side_length):
                if grid[i][j] != grid[top][left]:
                    all_same_value = False
                    break
        if all_same_value:
            return Node(grid[top][left], True, None, None, None, None)
        top_left = dfs(top, left, side_length // 2)
        top_right = dfs(top, left + side_length // 2, side_length // 2)
        bottom_left = dfs(top + side_length // 2, left, side_length // 2)
        bottom_right = dfs(top + side_length // 2, left + side_length // 2, side_length // 2)
        return Node(grid[top][left], False, top_left, top_right, bottom_left, bottom_right)

    return dfs(0, 0, len(grid))


def construct_v2(grid):
    """ In the previous approach, we first iterate over all the cells in the matrix and then decide if this should be a
         leaf or not and have four child nodes. In case we decide to have four child nodes, we recursively move to the
         4 sub-matrices and follow the same process.

         The redundant part in that approach is when we will iterate over the cells in the sub-matrices that would have
         already been iterated for the root node. It can also be explained by the time complexity of the previous
         approach, which is O(N^2 logN); hence all the N^2 cells can be at max iterated logN times.

         These redundant operations can be avoided if we simply make a recursive call to the 4 sub-matrices instead of
         first checking all the values. Once all four recursive calls returned, we will decide whether to let these as
         child nodes of the root node or should be combined into one as the root node.

         This decision will again depend on the values, but we won't have to check all the cells; instead, we can just
         check if the four nodes are leaf nodes and all have the same value (value attribute). If they are, we can just
         return a root leaf node with a value same as the 4 nodes; otherwise, we will return a node with any value and
         having these nodes as the respective child nodes.

         In this optimization, the only time we will have to check the cell value is when we have a matrix of size 1.
         This would be the base case of the recursion and is doable in constant time.

    Time complexity: O(N^2), each cell in the matrix is visited only once; we don't check to see if the grid contains
    the same value in each cell at each recursive call
    Space complexity: O(log N),  for the recursion call stack; the maximum number of active stack calls is logN
    """

    def helper(i, j, side_length):
        if side_length == 1:
            return Node(grid[i][j], True, None, None, None, None)
        topLeft = helper(i, j, side_length // 2)
        topRight = helper(i, j + side_length // 2, side_length // 2)
        bottomLeft = helper(i + side_length // 2, j, side_length // 2)
        bottomRight = helper(i + side_length // 2, j + side_length // 2, side_length // 2)
        if topLeft.isLeaf and topRight.isLeaf and bottomLeft.isLeaf and bottomRight.isLeaf and \
                topLeft.val == topRight.val and topRight.val == bottomLeft.val and bottomLeft.val == bottomRight.val:
            # If the 4 returned nodes are leaves and have the same value, return a leaf node with the same value.
            return Node(grid[i][j], True, None, None, None, None)
        return Node(grid[i][j], False, topLeft, topRight, bottomLeft, bottomRight)

    return helper(0, 0, len(grid))

