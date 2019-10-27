""" Given a reference of a node in a connected undirected graph, return a deep copy (clone) of the graph. Each node in
the graph contains a val (int) and a list (List[Node]) of its neighbors. """

# Definition for a Node.


class Node(object):
    def __init__(self, val, neighbors):
        self.val = val
        self.neighbors = neighbors


def clone_graph_v1(node):
    """ Use a hash map to look up nodes and add connections to them while performing DFS.
    Time complexity: O(V + E)
    Space complexity: O(V)
    """

    def dfs(node):
        if node.val in clones:
            return clones[node.val]
        new_node = Node(node.val, [])
        clones[new_node.val] = new_node
        for neighbor in node.neighbors:
            new_node.neighbors.append(dfs(neighbor))
        return new_node

    clones = {}
    return dfs(node)
