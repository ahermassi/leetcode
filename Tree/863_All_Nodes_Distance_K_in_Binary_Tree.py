""" We are given a binary tree (with root node root), a target node, and an integer value K.
Return a list of the values of all nodes that have a distance K from the target node.  The answer can be returned in any
order. """

from collections import deque, defaultdict


def distance_k_v1(root, target, K):
    """ If we know the parent of every node x, we know all nodes that are distance 1 from x. We can then perform a
        breadth first search from the target node to find the answer.
        We first do a depth first search where we annotate every node with information about its parent. Therefore, we
        need a set to keep track of nodes we have visited so that we do not go back and revisit what has already been
        processed and cause an infinite cycle.
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
    queue.append((target, 0))  # When our search starts, we are standing at layer 0
    seen = {target}
    while queue:
        if queue[0][1] == K:  # Is this the layer we want? If so, extract and return it
            return [node.val for node, depth in queue]
        node, depth = queue.popleft()  # Pull a node from the search queue. We are going to basically use our current
        # layer to populate the next layer of nodes that we need to search in the next while loop iteration
        for n in (node.left, node.right, node.par):  # Let's process all nodes in the layer. This is BFS.
            if n and n not in seen:  # Has node been touched before?
                queue.append((n, depth + 1))
                seen.add(n)
    return []


def distance_k_v2(root, target, K):
    """ A recursive dfs function 'build_graph' help to build up a map 'graph', similar to a graph adjacency list. The
        key of map is node and the value of map is a list of nodes connected to the key node.
        Then we do K times a BFS search loop to find all nodes of distance K from target.
        This solution is more suitable when the given tree is read-only and the parent annotation is not possible.
    Time complexity: O(N)
    Space complexity: O(N)
    """

    def build_graph(node, par):
        if node and par:
            graph[node].append(par)
            graph[par].append(node)
        if node.left:
            build_graph(node.left, node)
        if node.right:
            build_graph(node.right, node)

    graph = defaultdict(list)
    build_graph(root, None)
    queue = deque([target])
    visited = set()
    for _ in range(K):
        n = len(queue)
        for _ in range(n):
            node = queue.popleft()
            visited.add(node)
            queue.extend([neighbor for neighbor in graph[node] if neighbor not in visited])
    return [node.val for node in queue]
