""" Given two nodes of a binary tree p and q, return their lowest common ancestor (LCA).

Each node will have a reference to its parent node. The definition for Node is below:

class Node {
    public int val;
    public Node left;
    public Node right;
    public Node parent;
}
According to the definition of LCA on Wikipedia: "The lowest common ancestor of two nodes p and q in a tree T is the
lowest node that has both p and q as descendants (where we allow a node to be a descendant of itself)." """


def lowest_common_ancestor_v1(p, q):
    """ Store the path from p to the root, then traverse the path from q to the root. The first common point of the two
    paths is the LCA.
    Time complexity: O(h), where h is the height of p
    Space complexity: O(h)
    """
    ancestors_path = set()
    while p:
        ancestors_path.add(p)
        p = p.parent
    while q not in ancestors_path:
        q = q.parent
    return q