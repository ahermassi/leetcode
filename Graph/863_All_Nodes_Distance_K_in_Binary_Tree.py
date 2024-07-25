""" We are given a binary tree (with root node root), a target node, and an integer value K.
Return a list of the values of all nodes that have a distance K from the target node.  The answer can be returned in any
order. """

from collections import deque, defaultdict


def distance_k_v1(root, target, k):
    """ In the given tree, each node only has pointers to its left and right child nodes, making the typical tree
         traversal approach only applicable to the subtree rooted at the target node. We cannot access other parts of
         the tree beyond the subtree as we can't access the parent, which implies the need to establish additional
         connections beyond the child node pointers.

         We can implement a parent pointer to each node (apart from the root node) recursively.
         If we know the parent of every node x, we know all nodes that are distance 1 from x. We can then perform a BFS
         from the target node to find the answer.


        We use a hash set to keep track of all the visited nodes. Whenever we find an unvisited neighbor node, we add
        it to the hash set, so it won't be visited anymore.

        The BFS processes the nodes in layers, where the entirety of nodes of each level are popped at each iteration,
        and their unvisited children and parent are added to the queue. Done k times, this leaves us with a queue that
        contains all the nodes k distance from target node.

    Time complexity: O(N), where N is the number of nodes in the given tree. In a typical BFS search, the time
    complexity is O(V+E) where V is the number of vertices and E is the number of edges. There are N nodes and
    N-1 edges because the graph is a tree. Each node is added to the queue and popped from the queue once, and it takes
    O(N) to handle all nodes.
    Space complexity: O(N)
    """

    def annotate(node, par):
        if node:
            node.par = par
            annotate(node.left, node)
            annotate(node.right, node)

    annotate(root, None)
    queue = deque([target])  # When BFS starts, we are standing at layer 0
    visited = set()
    while k:
        size = len(queue)
        # Let's process all nodes in the layer
        for _ in range(size):
            # Pull a node from the search queue. We are going to basically use the current layer to populate the next
            # layer of nodes that we need to search in the next while loop iteration.
            node = queue.popleft()
            visited.add(node)
            # Every node is going to add its children as well as its parent if they haven't been already processed
            queue.extend(neighbor for neighbor in (node.left, node.right, node.par) if neighbor and neighbor not in visited)
        k -= 1
    return [node.val for node in queue]


def distance_k_v2(root, target, k):
    """ The previous approach of dynamically adding attributes is not a recommended practice. A safer method is to
         use a hash map to save pointers to each node's parent before performing the BFS.

    Time complexity: O(N)
    Space complexity: O(N)
    """

    def get_parents(root, parent):
        if not root:
            return
        parents[root] = parent
        get_parents(root.left, root)
        get_parents(root.right, root)

    parents = dict()
    get_parents(root, None)
    queue = deque([target])
    visited = set()
    while k:
        size = len(queue)
        for _ in range(size):
            node = queue.popleft()
            visited.add(node)
            queue.extend(neighbor for neighbor in (node.left, node.right, parents[node]) if neighbor and neighbor not in visited)
        k -= 1
    return [node.val for node in queue]



# Watch: https://www.youtube.com/watch?v=nPtARJ2cYrg
def distance_k_v3(root, target, K):
    """ If we view the tree structure as a graph, then it is easy to come up the BFS solution to find the nodes that
        are located at a certain distance from the target node.
        What is missing in the original tree data structure that makes the above idea a bit tricky to implement is the
        explicit pointer to a node's parent which is the neighbor for a node, the same as its children nodes.
        Due to this missing pointer, there is no explicit way for a node to reach out directly its neighbor nodes that
        is connected through the parent node.
        So the solution becomes clear, let's construct a graph from a given tree structure.
        A recursive dfs function 'build_graph' helps build a map 'graph', similar to a graph's adjacency list. The
        key of map is node and the value of map is a list of nodes connected to the key node.
        Then we do K times a BFS search loop to find all nodes of distance K from target.
        This solution is more suitable when the given tree is read-only and the parent annotation is not possible.
    Time complexity: O(N)
    Space complexity: O(N)
    """

    def build_graph(node, par):  # This function serves the purpose of annotation of the previous solution. If
        # modifying the tree is not possible, we map each node to its children and each child node to its parent.
        # This results in an undirected graph, which is a more flexible representation of the given tree.
        if not node:
            return
        if par:
            graph[node].append(par)
            graph[par].append(node)
        build_graph(node.left, node)
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
