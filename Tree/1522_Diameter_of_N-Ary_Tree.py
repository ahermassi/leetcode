""" Given a root of an N-ary tree, you need to compute the length of the diameter of the tree.

The diameter of an N-ary tree is the length of the longest path between any two nodes in the tree. This path may or
may not pass through the root. """


def diameter(self, root):
    """ Similar to 543- Diameter of Binary Tree.
        The diameter is the maximum of either:
            1- Passing through the root, in which case the longest path would be using the 2 maximum heights amongst
               ALL the root's children
            2- The maximum diameter amongst ALL the children diameters
        So, we can solve this problem with two different cases:
            1- If the longest path will include the root node, then the longest path must be:
               first_max_child_height + second_max_child_height
            2- If the longest path does not include the root node, this problem is divided into k sub-problems, where
               k is the number of children: set each of the children as the new root separately, and repeat the
               previous step.
        Conclusion:
        Diameter of a tree with regards to root root can be defined as:
            Maximum(Diameter of child 1, Diameter of child 2,..., Diameter of child k, Longest path between two nodes
                    which passes through the root)
        Now, the diameter of each of the child subtrees can be solved recursively. Longest path between two nodes which
        passes through the root can be calculated as: first_max_child_height + second_max_child_height. Therefore:
            Diameter = max(Diameter of child 1, Diameter of child 2,..., Diameter of child k,
                           first_max_child_height + second_max_child_height)
    Time complexity: O(N)
    Space complexity: O(N)
    """

    def height(root):
        if not root:
            return 0
        first_max_height = second_max_height = 0
        for child in root.children:
            child_height = height(child)
            if child_height > first_max_height:
                first_max_height, second_max_height = child_height, first_max_height
            elif child_height > second_max_height:
                second_max_height = child_height
        self.diameter = max(self.diameter, first_max_height + second_max_height)
        return 1 + first_max_height

    self.diameter = 0
    height(root)
    return self.diameter
