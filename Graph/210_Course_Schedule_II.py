""" There are a total of n courses you have to take, labeled from 0 to n-1.
Some courses may have prerequisites, for example to take course 0 you have to first take course 1, which is expressed
as a pair: [0,1]
Given the total number of courses and a list of prerequisite pairs, return the ordering of courses you should take to
finish all courses.
There may be multiple correct orders, you just need to return one of them. If it is impossible to finish all courses,
return an empty array. """

from collections import defaultdict, deque


# Refer to this excellent article for both solutions: https://leetcode.com/articles/course-schedule-ii/
# Video explanation: https://www.youtube.com/watch?v=Akt3glAwyfY
def find_order_v1(num_courses, prerequisites):
    """ This problem is a natural fit for graph based algorithms, and we can easily model the elements in the problem
         statement as a graph.

        Each course would represent a vertex in the graph. The edges are modeled after the prerequisite relationship
        between courses. So, we are given that a pair such as [a, b] means the course b is a prerequisite for the
        course a. This can be represented as a directed edge a ➔ b in the graph.

        There is a possibility of a cycle in the graph. If the graph was acyclic, then an ordering of subjects as
        required in the question would ALWAYS be possible. Since it's mentioned that such an ordering may not always be
        possible, that means we have a cyclic graph.

        Such an ordering of subjects is referred to as a Topological Sort and this is a common algorithmic problem in
        the graph domain. There are two approaches to solve this problem. One of them is DFS which is implemented in
        this approach. Same logic as 207- Course Schedule.

        Suppose we are at a node in the graph during the depth first traversal. Let's call this node A.

        The way DFS works is that we would consider all possible paths stemming from A before finishing up the recursion
        for A and moving on to other nodes. All the nodes in the paths stemming from the node A would have A as an
        ancestor. The way this fits in our problem is that all the courses in the paths stemming from the course A would
        have A as a prerequisite.

        Now we know how to get all the courses that have a particular course as a prerequisite. If a valid ordering of
        courses is possible, the course A would come before all the other set of courses that have it as a prerequisite.
        This idea for solving the problem can be explored using depth-first search.

            - Construct the adjacency list using the edge pairs given in the input. An important thing to note about the
               input for the problem is that a pair such as [a, b] represents that the course b needs to be taken in
               order to do the course a. This implies an edge of the form a ➔ b.

            - For each of the nodes in the graph, we will run a depth-first search in case that node was not already
               visited in some other node's DFS traversal.

            - Suppose we are executing the depth-first search for a node N. We will recursively traverse all the
               neighbors of node N which have not been processed before, which represent the prerequisites of N.

            - Once the processing of all the neighbors is done, we will add the node N to the result list. When we add
               the node N to the list, all the prerequisite nodes of N will already be in the list.

        Recall that DFS maintains a color for each vertex. Initially, all vertices are white (-1). When a vertex is
        first discovered, it is colored gray (0). When DFS finishes processing a vertex and all its neighbors, that
        vertex is colored black (1). As soon as we discover an edge from a gray vertex back to a gray vertex, a cycle
        exists, and we can stop.

        If node course has not been visited, then mark it as -1.
        If node course is being visited, then mark it as 0. If we find a vertex marked as 0 during DFS, then this
        vertex is part of a cycle.
        If node course has been visited, then mark it as 1. If a vertex was marked as 1, then no cycle contains course
        or its successors.

        0 means this node is part of the current trip, and either all of its descendants are not processed or it's still
        in the function call stack. If you see it again, it's a cycle.
        1 means the node and all its descendants were processed, and no cycle was found. if we hit this, going down this
        path won't find any cycles.

        Another way to think about it is the last few in the order must be those which are not prerequisites of other
        courses. Thinking it recursively means if one node has unvisited child node, we should visit them first before
        we put this node down in the final order array. This sounds like a postorder DFS.

        Because the tree is a connected graph, we can start from any node. The graph is possibly not connected, so we
        need to check every node.

        An important thing to note about Topological Sort is that there won't be just one ordering of nodes (courses).
        There can be multiple.

    Time complexity: O(|V| + |E|), where V is the number of vertices/courses and E is the number of edges/dependencies.
    It would take ∣E∣ time complexity to build the graph in the first step. Since we perform a postorder DFS traversal
    on the graph, we visit each vertex and each edge once and only once in the worst case, i.e. ∣V∣+∣E∣.
    Space complexity: O(|V| + |E|), we build a graph that would consume |V| + |E| space. Then, |V| is the maximum stack
    depth. If we go deeper than |V| calls, some vertex must repeat, implying a cycle in the graph, which leads to
    early termination.
    """

    def dfs(node):
        if visited[node] == 0:
            # Don't proceed further if we found a cycle already
            return False
        if visited[node] == 1:
            return True
        visited[node] = 0  # Start the recursion
        for neighbor in prereq[node]:
            if not dfs(neighbor):
                return False
        res.append(node)
        visited[node] = 1
        return True

    prereq = defaultdict(list)
    visited = [-1] * num_courses
    for a, b in prerequisites:
        prereq[a].append(b)
    res = []
    for course in range(num_courses):
        # If a cycle exists, no topological ordering is possible, and therefore it will be impossible to take all
        # the courses.
        if not dfs(course):
            return None
    return res


def find_order_v2(num_courses, prerequisites):
    """ Kahn's algorithm for Topological Sorting.

         The problem is to find a global ordering for all nodes in a DAG (Directed Acyclic Graph) with regard to their
         dependencies.

         Kahn’s algorithm works by keeping track of the number of outgoing edges from each node (outdegree). It works by
         repeatedly visiting the nodes with an outdegree of zero and deleting all the edges associated with it leading
         to a decrement of outdegree for the nodes whose outgoing edges are deleted. This process continues until no
         elements with zero outdegree can be found.

         In our case, the nodes with zero outdegree correspond to the nodes which do not have any prerequisites:
         These can be started immediately.

         The algorithm terminates when we can no longer remove edges from the graph. There are two possible outcomes:

            1- If there are still some edges left in the graph, then these edges must have formed certain cycles, which
                 is similar to the deadlock situation. It is due to these cyclic dependencies that we cannot remove them
                 during the above processes.
            2- Otherwise, we have removed all the edges from the graph, and we got ourselves a topological order of the
                 graph.

        The first node in the topological ordering will be the node that doesn't have any outcoming edges. Essentially,
        any node that has an outdegree of 0 can start the topological sort. If there are multiple such nodes,
        their relative order doesn't matter, and they can appear in any order.

    Time complexity: O(|V| + |E|), where V is the number of vertices/courses and E is the number of edges/prerequisites.
    It would take ∣E∣ time complexity to build the graph. Each queue operation takes O(1) time, and a single node will
    be pushed once, leading to O(|V|) operations. We iterate over the neighbors of each node that is popped out of the
    queue iterating over all the edges once. Since there are total of |E| edges, it would take O(|E|) time to iterate
    over the edges.
    Space complexity: O(|V| + |E|), the graph takes O(|E|) space. The outdegree array takes O(|V|) space. We use an
    intermediate queue data structure to keep all the nodes with 0 outdegree. In the worst case, there won't be any
    prerequisite relationship and the queue will contain all the vertices initially since all of them will have
    0 outdegree, which gives O(|V|).
    """
    courses_that_depend_on, outdegree = defaultdict(list), [0] * num_courses
    for course, prereq in prerequisites:
        # (courses_that_depend_on[prerq] = course) means 'prereq' is a prerequisite of 'course'
        courses_that_depend_on[prereq].append(course)
        outdegree[course] += 1  # Record the number of prerequisites each course has
    # Iterate the outdegree list and find the nodes that have 0 in-degree, which maps to 0 prerequisites. If none is
    # found, then there must be a cycle and a topological ordering is not possible.
    queue = deque(course for course in range(num_courses) if outdegree[course] == 0)
    res = []
    while queue:
        course = queue.popleft()
        res.append(course)
        for neighbor in courses_that_depend_on[course]:
            # Iterate over the courses that have 'course' as prerequisite. This is equivalent to removing the edge
            # neighbor -> course, which in other words means taking 'course' and 'course' is no longer in the list
            # of prerequisite of 'neighbor'
            outdegree[neighbor] -= 1
            if outdegree[neighbor] == 0: # We've taken all the prerequisites of course 'neighbor'
                queue.append(neighbor)
    return res if len(res) == num_courses else []


