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


# Video explanation: https://www.youtube.com/watch?v=nPtARJ2cYrg
def distance_k_v3(root, target, k):
    """ We can take the hash map of the previous implementation one step further and transform the given binary tree
         into an equivalent graph, where each pointer is treated as an undirected edge. Hence, the graph retains all the
         connected nodes from the original binary tree, including the pointers from children to parents. Consequently,
         we can perform a regular search on this graph.

         In the equivalent graph, we only need to visit all unvisited neighboring nodes of the current node, which
         include nodes that are equivalent to the left and right children and the parent in the original tree.

         Similarly, we use a hash set to keep track of all the visited nodes. Whenever we find an unvisited neighbor
         node, we add it to the hash set so it won't be visited anymore.

         A recursive dfs function build_graph helps build a hash map similar to a graph's adjacency list. The key of the
         map is a node and the value is a list of nodes connected to the key node.

         This solution is more suitable when the given tree is read-only and the parent annotation is not possible.

    Time complexity: O(N)
    Space complexity: O(N)
    """

    def build_graph(node, par):
        # This function serves the purpose of annotation of the first implementation. If modifying the tree is not
        # possible, we map each node to its children and each child node to its parent.
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
    while k:
        size = len(queue)
        for _ in range(size):
            node = queue.popleft()
            visited.add(node)
            queue.extend([neighbor for neighbor in graph[node] if neighbor not in visited])
        k -= 1
    return [node.val for node in queue]


def distance_k_v4(root, target, k):
    """ We can also perform the graph search using DFS.

         In the equivalent graph, we only need to recursively visit all unvisited neighboring nodes of the current node,
         which include nodes that are equivalent to the left and right children and the parent in the original tree.

         We define a recursive function to explore nodes as far as possible along each branch. Upon reaching the end of
         the current branch, we backtrack to the next possible branch and continue exploring. Once we encounter an
         unvisited node, we take one of its neighbor nodes (left child, right child, or parent) as the next node on this
         branch. Recursively call the function to the next node and solve the sub-problem.

         If we reach the end of this branch, we backtrack to the previous node and visit the next neighbor node, and
         repeat the process.

         If we reach a node with a distance of k to target, it denotes that this node is one of the destination nodes.
         Since continuing on with this branch leads to nodes with a distance larger than k, we also backtrack to the
         previous node and try visiting the next neighbor node.

    Time complexity: O(N)
    Space complexity: O(N)
    """

    def build_graph(node, par):
        if not node:
            return
        if par:
            graph[node].append(par)
            graph[par].append(node)
        build_graph(node.left, node)
        build_graph(node.right, node)

    def dfs(node, distance):
        if distance == k:
            res.append(node.val)
            return
        visited.add(node)
        for neighbor in graph[node]:
            if neighbor not in visited:
                dfs(neighbor, distance + 1)

    graph = defaultdict(list)
    build_graph(root, None)
    visited = set()
    res = []
    dfs(target, 0)
    return res
