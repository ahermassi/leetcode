""" Given a reference of a node in a connected undirected graph, return a deep copy (clone) of the graph. Each node in
the graph contains a val (int) and a list (List[Node]) of its neighbors. """

from collections import deque

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


def clone_graph_v2(node):
    """ Iterative version of above DFS.
    Time complexity: O(V + E)
    Space complexity: O(V)
    """
    new_node = Node(node.val, [])
    clones = {node.val: new_node}
    stack = [node]
    while stack:
        top = stack.pop()
        for neighbor in top.neighbors:
            if neighbor.val not in clones:
                stack.append(neighbor)
                clones[neighbor.val] = Node(neighbor.val, [])
            clones[top.val].neighbors.append(clones[neighbor.val])
    return new_node


def clone_graph_v3(node):
    """ BFS version.
    Time complexity: O(V + E)
    Space complexity: O(V)
    """
    new_node = Node(node.val, [])
    clones = {node.val: new_node}
    queue = deque([node])  # The queue is used to to store ORIGINAL nodes that need to be cloned
    while queue:
        top = queue.popleft()
        for neighbor in top.neighbors:
            if neighbor.val not in clones:  # Add to map and queue if this node hasn't been searched/cloned before
                queue.append(neighbor)
                clones[neighbor.val] = Node(neighbor.val, [])
            clones[top.val].neighbors.append(clones[neighbor.val])  # Add neighbor to newly cloned node
    return new_node

