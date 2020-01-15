""" Given a reference of a node in a connected undirected graph, return a deep copy (clone) of the graph. Each node in
the graph contains a val (int) and a list (List[Node]) of its neighbors. """

from collections import deque


# Definition for a Node.


class Node(object):
    def __init__(self, val, neighbors=None):
        self.val = val
        self.neighbors = neighbors


def clone_graph_v1(node):
    """ The basic intuition for this problem is to just copy as we go. To avoid getting stuck in a loop, we would need
        some way to keep track of the nodes which have already been copied. By doing this we don't end up traversing
        them again.
        Start traversing the graph from the given node.
        We would take a hash map to store the reference of the copy of all the nodes that have already been visited and
        cloned. The key for the hash map would be the node of the original graph and corresponding value would be the
        corresponding cloned node of the cloned graph. If the node already exists in the map, we return corresponding
        stored reference of the cloned node.
        If we don't find the node in the hash map, we create a copy of it and put it in the hash map. It's important to
        create a copy of the node and add it to the hash map before entering recursion. In the absence of such an
        ordering, we would be caught in the recursion because on encountering the node again in somewhere down the
        recursion again, we will be traversing it again thus getting into cycles.
        Now make the recursive call for the neighbors of the node. Each recursive call made would return the clone of a
        neighbor. We will prepare the list of these clones returned and put into neighbors of clone node which we had
        created earlier. This way we will have cloned the given node and its neighbors.
    Time complexity: O(V + E)
    Space complexity: O(V)
    """

    def dfs(node):  # The job of dfs() is to clone a node an recursively clone its neighbors. One again, we TRUST that
        # the recursive call will handle copying the neighbors
        if node in clones:
            return clones[node]
        new_node = Node(node.val)
        clones[node] = new_node
        for neighbor in node.neighbors:
            new_node.neighbors.append(dfs(neighbor))
        return new_node

    clones = {}
    return dfs(node)


def clone_graph_v2(node):
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


def clone_graph_v3(node):
    """ Iterative version of above DFS.
    Time complexity: O(V + E)
    Space complexity: O(V)
    """
    new_node = Node(node.val)
    clones = {node: new_node}
    stack = [node]
    while stack:
        top = stack.pop()
        for neighbor in top.neighbors:
            if neighbor not in clones:
                stack.append(neighbor)
                clones[neighbor] = Node(neighbor.val)
            clones[top].neighbors.append(clones[neighbor])
    return new_node
