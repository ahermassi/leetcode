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


def lowest_common_ancestor_v2(p, q):
    """ We can optimize the previous solution by not using extra space. The idea is fairly simple and similar to
    finding the convergence point of 2 linked lists in 160_Intersection_of_Two_Linked_Lists. We keep two pointers,
    pa and pb. Originally, these pointers point to q and p, respectively. Then we follow their parent pointers until
    they point to the same node. When either of the pointers points to root, we set it to the other original starting
    node. For example, when pa points to root (i.e pa.parent is None), assign pa to q.
    The idea is if you switch head, the possible difference between lengths would be countered. On the second
    traversal, they either hit or miss. If they didn't meet, they will hit the end at the same iteration,
    pa == pb == None, return either one of them is the same, None.
    This works because pointer pa walks through paths of p AND q (since once it hits null, it goes to q's path
    head). Pointer pb also walks through paths of q AND p. Regardless of the length of the two paths, the sum of
    the lengths are the same (i.e. a+b = b+a), which means that the pointers sync up at the point of intersection.
    If the paths never intersected, it's fine too, because they'll sync up at the end of each path, both of which
    are null.
    Time complexity: O(h1 + h2), where h1 is the height of node p and h2 is the height of node q
    Space complexity: O(1)
    """
    pa, pb = p, q
    while pa != pb:
        pa = pa.parent if pa else q
        pb = pb.parent if pb else p
    return pa