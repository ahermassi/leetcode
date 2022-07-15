""" Given a reference of a node in a connected undirected graph, return a deep copy (clone) of the graph. Each node in
the graph contains a val (int) and a list (List[Node]) of its neighbors. """

from collections import deque


# Definition for a Node.


class Node(object):
    def __init__(self, val, neighbors=None):
        self.val = val
        self.neighbors = neighbors

# Video explanation: https://www.youtube.com/watch?v=mQeF6bN8hMk


def clone_graph_v1(node):
    """ The basic intuition for this problem is to just copy as we go. To avoid getting stuck in a loop, we would need
        some way to keep track of the nodes which have already been copied. By doing this we don't end up traversing
        them again.

            - Start traversing the graph from the given node.

            - We would take a hash map to store the reference of the copy of all the nodes that have already been
               visited and cloned. The key for the hash map would be the node of the original graph and corresponding
               value would be corresponding cloned node of the cloned graph. If the node already exists in the map,
               we return corresponding stored reference of the cloned node.

            - If we don't find the node in the hash map, we create a copy of it and put it in the hash map. It's
               important to create a copy of the node and add it to the hash map before entering recursion. In the
               absence of such an ordering, we would be caught in the recursion because of encountering the node again
               somewhere down the recursion, we will be traversing it again thus getting into cycles.

            - Now make the recursive call for the neighbors of the node. Each recursive call made would return the
               clone of a neighbor. We will prepare the list of these clones returned and put into neighbors of clone
               node which we had created earlier. This way we will have cloned the given node and its neighbors.

    Time complexity: O(|V| + |E|), we will touch V nodes and traverse E edges
    Space complexity: O(|V|), this space is occupied by the hash map and in addition to that, space would also be
    used by the recursion stack, which would be equal to O(H) where H is the height of the graph.
    """

    def dfs(node):
        # The job of dfs() is to clone a node and recursively clone its neighbors. Once again, we TRUST that the
        # recursive call will handle copying the neighbors
        if node in clones:
            return clones[node]
        node_clone = Node(node.val)
        clones[node] = node_clone  # We can also use the node's value as key as it's guaranteed to be unique
        for neighbor in node.neighbors:
            node_clone.neighbors.append(dfs(neighbor))
        return node_clone

    clones = {}
    return dfs(node) if node else None

# Watch: https://www.youtube.com/watch?v=vma9tCQUXk8


def clone_graph_v2(node):
    """ BFS version.
        We will use a hash map to store the reference of the copy of all the nodes that have already been visited and
        copied.
        Add the first node to the queue. Clone the first node and add it to the hash map.
        Do the BFS traversal.
            - Pop a node from the front of the queue
            - Visit all the neighbors of this node
            - If any of the neighbors was already visited, then it must be present in the hash map. Get the clone of
              this neighbor from the hash map in that case.
            - Otherwise, create a clone and store it in the hash map
            - Add the clones of the neighbors to the corresponding list of the clone node
    Time complexity: O(V + E), we will touch V nodes and traverse E edges
    Space complexity: O(V), we will store V vertices in the hashtable (and the queue can hold at worst some fractional
    multiple of the total number for vertices. Imagine 1 node connected to 9 nodes all at once in a graph of size
    10, and we start from that 1 node. Our queue would have 9 nodes in it at once on the first iteration)
    """
    new_node = Node(node.val)
    clones = {node: new_node}
    queue = deque([node])  # The queue is used to to store ORIGINAL nodes that need to be cloned
    while queue:
        top = queue.popleft()
        for neighbor in top.neighbors:
            if neighbor not in clones:  # Has this neighbor been given a clone?
                # No? Give it a mapping and add the original neighbor to the search queue so we can express ITS edges
                # later
                clones[neighbor] = Node(neighbor.val)
                queue.append(neighbor)
            clones[top].neighbors.append(clones[neighbor])  # Draw the edge from 'top' clone to 'neighbor' clone.
            # Do you see how our hash map makes this quick access possible?
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
