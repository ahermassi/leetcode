""" We are given a binary tree (with root node root), a target node, and an integer value K.
Return a list of the values of all nodes that have a distance K from the target node.  The answer can be returned in any
order. """

from collections import deque
import unittest2 as unittest


def distance_k(root, target, K):
    """ If we know the parent of every node x, we know all nodes that are distance 1 from x. We can then perform a
        breadth first search from the target node to find the answer.
        We first do a depth first search where we annotate every node with information about it's parent.
        After, we do a breadth first search to find all nodes a distance K from the target.
    Time complexity: O(N), where N is the number of nodes in the given tree
    Space complexity: O(N)
    """

    def annotate(node, par=None):
        if node:
            node.par = par
            annotate(node.left, node)
            annotate(node.right, node)

    annotate(root)
    queue = deque()
    queue.append((target, 0))
    seen = {target}
    while queue:
        if queue[0][1] == K:
            return [node.val for node, depth in queue]
        node, depth = queue.popleft()
        for n in (node.left, node.right, node.par):
            if n and n not in seen:
                queue.append((n, depth + 1))
                seen.add(n)
    return []
