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
    """ DFS but without the use of a "global" variable to store the result.
    Time complexity: O(N)
    Space complexity: O(h)
    """

    def dfs(root, cur_sum):
        if not root:
            return 0
        cur_sum = cur_sum * 10 + root.val
        if not root.left and not root.right:
            return cur_sum
        left_sum = dfs(root.left, cur_sum)
        right_sum = dfs(root.right, cur_sum)
        return left_sum + right_sum

    return dfs(root, 0)


def sum_numbers_v3(root):
    """ Here we implement standard iterative pre-order traversal with the stack.
    Time complexity: O(N)
    Space complexity: O(h), to keep the recursion stack, where h is tree height
    """
    if not root:
        return 0
    res, stack = 0, [(root, 0)]
    while stack:
        node, total = stack.pop()
        total = total * 10 + node.val
        if not node.left and not node.right:
            res += total
        else:
            stack.extend([(child, total) for child in (node.left, node.right) if child])
    return res

