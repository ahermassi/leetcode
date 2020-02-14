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
    """ If we have parent pointers for each node we can traverse back from p and q to get their ancestors. The first
        common node we get during this traversal would be the LCA node. We can save the parent pointers in a dictionary
        as we traverse the tree.
        Once we have found both p and q, we get all the ancestors for p using the parent dictionary and add to a set
        called 'p_ancestor'. Similarly, we traverse through ancestors for node q. If the ancestor is present in the
        ancestors set for p, this means this is the first ancestor common between p and q (while traversing UPWARDS)
        and hence this is the LCA node.
        Note that this algorithm can benefit from the optimization implemented in 236- Lowest Common Ancestor with
        Parent Pointers.
    Time complexity: O(N), in the worst case we might be visiting all the nodes of the binary tree
    Space complexity: O(N), in the worst case space utilized by the stack, the parent pointer dictionary and the
    ancestor set, would be N each, since the height of a skewed binary tree could be N
    """
    parent = {}
    stack = [(root, None)]
    while p not in parent or q not in parent:
        node, par = stack.pop()
        if node:
            parent[node] = par
            stack.append((node.left, node))
            stack.append((node.right, node))
    p_ancestor = set()
    while p:
        p_ancestor.add(p)
        p = parent[p]
    while q:
        if q in p_ancestor:
            return q
        q = parent[q]
    return root


# Check this out: https://www.youtube.com/watch?v=py3R23aAPCA

def lowest_common_ancestor_v2(root, p, q):
    """ Recursive approach.
        The key is that we want to root ourselves at a node and then search left and then right for either of the 2
        nodes given.
        If we see either node, we will return it. If we do not find the node in a subtree, the value of null will be
        returned and bubbled up.
        After we search both left and right, we ask ourselves what our results mean.
        If we found nothing to the left, we just bubble up what is on the right (whatever that search result may be).
        This node we sit at cannot be the LCA since the left and right did not yield the 2 nodes we want.
        If we found nothing to the right, we just bubble up what is on the left (whatever that search result may be).
        This node we sit at cannot be the LCA since the left and right did not yield the 2 nodes we want.
        If both the right and left result are not null, we have found our LCA. Why? We know it is an ancestor at the
        least but we definitely know it is the lowest common ancestor because we went bottom upwards, whatever we hit
        will be the LCA and it will bubble up.
    Time complexity: O(N), in the worst case we might be visiting all the nodes of the binary tree
    Space complexity: O(N) worst case, O(logN) average case
    """
    if not root:
        return None
    if root == p or root == q:  # If we find either value, return ourselves to the caller
        return root
    # 'root' doesn't satisfy any of our base cases. Search left and then search right
    left = lowest_common_ancestor_v2(root.left, p, q)
    right = lowest_common_ancestor_v2(root.right, p, q)
    if left and right:  # We got something back on the left AND right. That means this node is the LCA because our
        # recursion returns from bottom to up, so we return what we hold: 'root'
        return root
    # Either one of the children returned a node, meaning either p or q found on left or right branch. Return whatever
    # we got.
    return left or right


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
