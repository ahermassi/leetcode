""" Given a binary tree, find the lowest common ancestor (LCA) of two given nodes in the tree. According to the
definition of LCA on Wikipedia: “The lowest common ancestor is defined between two nodes p and q as the lowest node
in T that has both p and q as descendants (where we allow a node to be a descendant of itself).” """

import unittest2 as unittest


# Definition for a binary tree node.


class TreeNode(object):
    def __init__(self, x):
        self.val = x
        self.left = None
        self.right = None


def lowest_common_ancestor_v1(root, p, q):
    """ If we have parent pointers for each node, we can traverse back from p and q to get their ancestors. The first
         common node we get during this traversal would be the LCA node.

         We can save the parent pointers in a dictionary as we traverse the tree. Once we have found both p and q, we
         get all the ancestors of p using the parent dictionary and add to a set called 'p_ancestors'.

         Similarly, we traverse through the ancestors of node q. If the ancestor is present in the ancestors set of p,
         this means this is the first ancestor common between p and q (while traversing UPWARDS) and hence this is the
         LCA node.

         Note that this algorithm can benefit from the optimization implemented in 236- Lowest Common Ancestor with
         Parent Pointers.

    Time complexity: O(N), in the worst case we might be visiting all the nodes of the binary tree
    Space complexity: O(N), in the worst case the space used by the stack, the parent pointer dictionary and the
    ancestor set, would be N each, since the height of a skewed binary tree could be N
    """
    parent = {}
    stack = [(root, None)]
    # The following loop is nothing but the iterative version of the recursive annotate(node, par) method with a slight
    # change: We keep storing the parent pointers in a dictionary until we find both p and q. No need to annotate the
    # entire tree.
    while p not in parent or q not in parent:
        node, par = stack.pop()
        parent[node] = par
        stack.extend([(child, node) for child in (node.left, node.right) if child])
    p_ancestors = set()
    while p:
        p_ancestors.add(p)
        p = parent[p]
    # The first ancestor of q which appears in p's ancestor set is their lowest common ancestor
    while q not in p_ancestors:
        q = parent[q]
    return q


# Video explanation: https://www.youtube.com/watch?v=py3R23aAPCA
def lowest_common_ancestor_v2(root, p, q):
    """ The recursive approach is pretty intuitive. The key is that we want to root ourselves at a node and then search
         left and then right for either of the 2 given nodes. The moment we encounter either of the nodes p or q, return
         some boolean flag. The flag helps determine if we found the required nodes in any of the paths. The least
         common ancestor would then be the node for which both the subtree recursions return a True flag. It can also be
         the node which itself is one of p or q and for which one of the subtree recursions returns a True flag.

        After we search both left and right subtrees, we ask ourselves what our results mean:

            - If we found nothing to the left, we just bubble up what is on the right (whatever that search result may
               be). The node we sit at cannot be the LCA since the left and right did not yield the 2 nodes we want.

            - If we found nothing to the right, we just bubble up what is on the left (whatever that search result may
               be). This node we sit at cannot be the LCA since the left and right did not yield the 2 nodes we want.

            - If both the right and left results are not null, we have found our LCA. Why? We know it is an ancestor at
               the very least, but we definitely know it is the lowest common ancestor because we went bottom upwards,
               whatever we hit will be the LCA, and it will bubble up.

    Time complexity: O(N), in the worst case we might be visiting all the nodes of the binary tree
    Space complexity: O(N) worst case, O(logN) average case
    """
    # It is crucial to define what lowest_common_ancestor(root, p, q) means: What is the LCA of p and q in the tree
    # ROOTED AT current 'root' node
    if not root or root == p or root == q:
        # If the current root is one of p or q, return ourselves to the caller
        return root
    # 'root' doesn't satisfy any of our base cases. Search left and then search right.
    left_search = lowest_common_ancestor_v2(root.left, p, q)
    right_search = lowest_common_ancestor_v2(root.right, p, q)
    if left_search and right_search:
        # We got something back from the left AND right. That means this node is the LCA because our recursion
        # returns from bottom to top, and we have found both p and q in different subtrees of the current root, so we
        # return what we hold: 'root'.
        # In other words, if the left subtree contains one of the descendants (p or q), and the right subtree
        # contains the remaining descendant (q or p),  then the root is their LCA
        return root
    # Either one of the children returned a node, meaning either p or q found on left or right branch.
    # If the left subtree contains both p and q then return left as their LCA.
    # If the right subtree contains both p and q then return right as their LCA.
    # Example: Assume p was found in the left subtree, right child returned None. This means q is somewhere below the
    # node where p was found. We don't need to search all the way, because in such scenario the node where p was found
    # is the LCA.
    return left_search or right_search


class Test(unittest.TestCase):
    root = TreeNode(3)
    root.left = TreeNode(5)
    root.right = TreeNode(1)
    root.left.left = TreeNode(6)
    root.left.right = TreeNode(2)
    root.right.left = TreeNode(0)
    root.right.right = TreeNode(8)
    root.right.left.left = TreeNode(7)
    root.right.right.right = TreeNode(4)
    p = root.left
    q = root.right.right.right
    result = root

    def test_lowest_common_ancestor(self):
        self.assertEqual(self.result, lowest_common_ancestor_v1(self.root, self.p, self.q))
        self.assertEqual(self.result, lowest_common_ancestor_v2(self.root, self.p, self.q))


if __name__ == '__main__':
    unittest.main()
