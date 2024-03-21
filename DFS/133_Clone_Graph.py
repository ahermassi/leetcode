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
    """ The basic intuition for this problem is to just copy as we go. What is crucial to understand is that we don't
         want to get stuck in a cycle while we are traversing the graph.

         According to the problem statement, any given undirected edge could be represented as two directional edges.
         So, if there is an undirected edge between node A and node B, the graph representation for it would have a
         directed edge from A to B and another from B to A.

         To avoid getting stuck in a loop, we would need some way to keep track of the nodes which have already been
         copied. By doing this we don't end up traversing them again.

            - Start traversing the graph from the given node.

            - Use a hashmap to store the reference of the copy of all the nodes that have already been visited and
               cloned. The key for the hashmap would be the node of the original graph and its corresponding value would
               be the cloned node of the clone graph.

               - If the node already exists in the map, we return the stored  reference of the cloned node.

            - If we don't find the node in the hashmap, we create a copy of it and put it in the hashmap. It's important
               to create a copy of the node and add it to the hashmap before entering the recursion. In the absence of
               such an ordering, we would be caught in an infinite loop because of encountering the node again somewhere
               down the recursion path, we will be traversing it again thus getting into cycles.

            - Now make the recursive call for the neighbors of the node. Each recursive call would return the clone of
               a neighbor. We will prepare the list of these clones returned and put into neighbors of clone node which
               we had created earlier. This way we will have cloned the given node and its neighbors.

    Time complexity: O(|V| + |E|), we will touch V nodes and traverse E edges
    Space complexity: O(|V|), this space is occupied by the hashmap and in addition to that, space would also be
    used by the recursion stack, which would be equal to O(H) where H is the height of the graph.
    """

    def dfs(node):
        # The job of dfs(node) is to clone a node and recursively clone its neighbors. Once again, we TRUST that the
        # recursive call will handle copying the neighbors.
        if node in clones:
            return clones[node]
        node_clone = Node(node.val)
        clones[node] = node_clone  # We can also use the node's value as key as it's guaranteed to be unique
        for neighbor in node.neighbors:
            # Iterate over the neighbors to create their clones
            node_clone.neighbors.append(dfs(neighbor))
        return node_clone

    clones = {}
    return dfs(node) if node else None


def clone_graph_v2(node):
    """ Iterative DFS using a stack. It's crucial to understand that the stack contains the nodes that have been cloned
         but whose neighbors' clones and connections haven't been set up yet.

    Time complexity: O(|V| + |E|)
    Space complexity: O(|V|)
    """
    node_clone = Node(node.val)
    clones = {node: node_clone}
    stack = [node]
    while stack:
        cur_node = stack.pop() # This node has a clone but its neighbors' connections haven't been established yet
        for neighbor in cur_node.neighbors:
            if neighbor not in clones:
                clones[neighbor] = Node(neighbor.val)
                stack.append(neighbor)
            clones[cur_node].neighbors.append(clones[neighbor])
    return node_clone


# Video explanation: https://www.youtube.com/watch?v=vma9tCQUXk8
def clone_graph_v3(node):
    """ We also have the BFS way of doing iterative traversal of the graph.

         We use a hashmap to store the reference of the copy of all the nodes that have already been visited and
         copied in order to avoid cycles.

            - Add the first node to the queue. Clone the first node and add it to the hashmap.

            - Do the BFS traversal:

                * Pop a node from the front of the queue
                * Visit all the neighbors of this node.
                      If any of the neighbors was already visited, then it must be present in the hashmap. Get the
                      clone of this neighbor from the hashmap in that case.
                      Otherwise, create a clone and store it in the hashmap.
                * Add the clones of the neighbors to the corresponding list of the clone node

        It's crucial to understand that the queue is used to store the ORIGINAL nodes that have been cloned BUT still
        need their neighbors' edges established. In other words, a node is in the queue if it has a clone but its edge
        relationships haven't yet been explored.

        In summary: We push a node to the queue and make sure that the node is already cloned. Then, we process
        neighbors. If a neighbor is already cloned, we just append it to the current clone neighbors list. Otherwise,
        we clone the neighbor and append it to the queue to make sure that we can visit it in the next iteration.

    Time complexity: O(|V| + |E|), we keep track of all the nodes that are visited in a hashmap, which ensures that
    each vertex (node) is enqueued at most once, and dequeued at most once. So the total time devoted to queue
    operations is O(|V|), where V is the number of nodes/vertices. The inner loop scans the neighbors list of each
    node only when the node is dequeued. Therefore, it scans each neighbors list at most once and so the total time in
    scanning the list is O(|E|), where E is the number of edges.
    Space complexity: O(|V|), we store V vertices in the hashmap, and the queue can hold at worst some fractional
    multiple of the total number for vertices. Imagine 1 node connected to 9 nodes all at once in a graph of size
    10, and we start from that 1 node. The queue would have 9 nodes in it at once in the first iteration. In addition,
    each vertex is enqueued at most once and dequeued at most once.
    Take this example: Nodes 1 2 3 4 5 6 7 8, [[2,4],[1,3],[2,4],[1,3],[5,6],[7,8],[5,6],[7,8]]
    In this example there are 8 nodes and 16 edges.
    When we look at node 1, we only go to edges 2 and 4.
    When we look at node 2, we only go to edges 1 and 3.
    So basically we go through 16 edges + 8 nodes = O(|V| + |E|)
    """
    if not node:
        return None
    clones = {node: Node(node.val)}
    # The queue is used to store ORIGINAL nodes that have been cloned BUT still need their neighbors' edges established
    queue = deque([node])
    while queue:
        cur_node = queue.popleft()
        for neighbor in cur_node.neighbors:
            if neighbor not in clones:
                # Has this neighbor been given a clone?
                # No? Clone it and add the original neighbor to the search queue, so we can explore ITS edges later
                clones[neighbor] = Node(neighbor.val)
                queue.append(neighbor)
            # Draw the edge from 'cur_node' clone to 'neighbor' clone.
            # Do you see how our hash map makes this quick access possible?
            clones[cur_node].neighbors.append(clones[neighbor])
    return clones[node]
