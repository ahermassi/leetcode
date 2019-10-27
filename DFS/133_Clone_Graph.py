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
        Add the start node the caller gave us to the queue and map the node to its clone through the hashtable.
        We will continue the cloning until the queue is empty (there will be no more nodes to process).
        We then pull a node from the queue, call it 'top'. We will iterate all of top's adjacent nodes, call each object
        yielded 'neighbor'.
        Do we create a cloned node for 'neighbor' ? If the 'neighbor' is NOT in the hashtable, create a mapping for
        'neighbor' and add 'neighbor' to the queue since it needs its adjacent nodes mapped out in the cloned graph.
        Add the cloned node of 'neighbor' as an adjacent node to the cloned node of 'top'.
    Time complexity: O(V + E), we will touch V nodes (vertices) and traverse E edges.
    Space complexity: O(V), we will store V vertices in the hashtable (and the queue can hold at worst some fractional
    multiple of the total number for vertices. Imagine 1 node connected to 9 nodes all at once in a graph of size
    10, and we start from that 1 node. Our queue would have 9 nodes in it at once on the first iteration)
    """
    new_node = Node(node.val, [])
    clones = {node.val: new_node}
    queue = deque([node])  # The queue is used to to store ORIGINAL nodes that need to be cloned
    while queue:
        top = queue.popleft()
        for neighbor in top.neighbors:
            if neighbor.val not in clones:  # Has this neighbor been given a clone?
                # No? Give it a mapping and add the original neighbor to the search queue so we can express ITS edges
                # later
                queue.append(neighbor)
                clones[neighbor.val] = Node(neighbor.val, [])
            clones[top.val].neighbors.append(clones[neighbor.val])  # Draw the edge from 'top' clone to  'neighbor'
            # clone. Do you see how our hashtable makes this quick access possible?
    return new_node
