""" Given a binary tree containing digits from 0-9 only, each root-to-leaf path could represent a number.
An example is the root-to-leaf path 1->2->3 which represents the number 123.
Find the total sum of all root-to-leaf numbers. """


# Video explanation: https://youtu.be/Jk16lZGFWxE
def sum_numbers_v1(root):
    """ Recursive preorder traversal.

         Each time we visit a node, we compute the integer it encodes using the number for its parent. If the node is a
         leaf, we add its integer to the total output sum. If it is not a leaf, we recursively explore the left and
         right subtrees.

            - Start at the root with current number = 0.

            - Every time, the current node's digit will be appended to the number from root to leaf and we recurse for
               left and right children.

            - If we reach a leaf node, we have formed the complete root-to-leaf number. We will then add this number to
               the overall sum.

        Note that this implementation can be converted to an iterative preorder using an explicit stack and to a BFS
        traversal using a queue.

    Time complexity: O(N), each node is visited once
    Space complexity: O(h), to keep the recursion stack, where h is the tree height
    """

    def dfs(root, number):
        if not root:
            return
        number = number * 10 + root.val
        if not root.left and not root.right:
            res[0] += number
        else:
            dfs(root.left, number)
            dfs(root.right, number)

    res = [0]
    dfs(root, 0)
    return res[0]


def sum_numbers_v2(root):
    """ DFS but without the use of the global variable. Each time we visit a node, we compute the integer it encodes
         using the number for its parent. If the node is a leaf, we return its integer. If it is not a leaf, we return
         the sum of the results from its left and right subtrees.

         Example:
                1
	        /    \
	      2       3
		          /
		        4

        dfs(1, 0) = dfs(2, 1) + dfs(3, 1)
        dfs(2, 1) = 10 + 2 = 12     // base case
        dfs(3, 1) = dfs(4, 10 + 3) + 0 = dfs(4, 13)
        dfs(4, 13) = 130 + 4 = 134    // base Case
        => dfs(1) = 12 + 134 = 146

    Time complexity: O(N)
    Space complexity: O(h)
    """

    def dfs(root, number):
        if not root:
            return 0
        number = number * 10 + root.val
        if not root.left and not root.right:
            return number
        left_sum = dfs(root.left, number)
        right_sum = dfs(root.right, number)
        return left_sum + right_sum

    return dfs(root, 0)


def sum_numbers_v3(root):
    """ Here we implement the iterative preorder traversal using an explicit stack.

    Time complexity: O(N)
    Space complexity: O(h), to keep the recursion stack, where h is the tree height
    """
    if not root:
        return 0
    res, stack = 0, [(root, 0)]
    while stack:
        node, number = stack.pop()
        number = number * 10 + node.val
        if not node.left and not node.right:
            res += number
        else:
            stack.extend([(child, number) for child in (node.left, node.right) if child])
    return res

