""" There are a total of n courses you have to take, labeled from 0 to n-1.
Some courses may have prerequisites, for example to take course 0 you have to first take course 1, which is expressed
as a pair: [0,1]
Given the total number of courses and a list of prerequisite pairs, is it possible for you to finish all courses? """

from collections import defaultdict, deque
import unittest2 as unittest


# Video explanation: https://www.youtube.com/watch?v=EgI5nU9etnU
def can_finish_dfs(num_courses, prerequisites):
    """ We can see that we have been given certain courses with some dependencies between them. The dependencies are
         expressed as pairs, which provides some hints for framing the problem in terms of a graph.

         The problem could be modeled as a graph traversal problem, where each course can be represented as a vertex in
        a graph and the dependency between the courses can be modeled as a directed edge between two vertex.

        A topological sort or topological ordering of a directed graph is a linear ordering of its vertices such that
        for every directed edge u -> v from vertex u to vertex v, u comes before v in the ordering.

        This problem a direct application of topological sort. Note that this type of sort can only be applied on
        Directed Acyclic Graphs (DAG). A Directed cyclic graph fails to yield a topological sort because of the
        presence of a cycle. This property is the intuition of this question's algorithm.

        Therefore, whether we could build a valid schedule of courses that satisfies all the dependencies
        (i.e. constraints) is reduced to determining if the corresponding graph is a DAG, i.e. there is no cycle in the
        graph.

        The general idea here is that we could enumerate each course (vertex) to check if it could form cyclic
        dependencies (i.e. a cyclic path) starting from this course. The check of cyclic dependencies for each course
        could be done via backtracking/DFS.

        In DFS, we use a recursive function to explore nodes as far as possible along each branch. Upon reaching the end
        of a branch, we backtrack to the previous node and continue exploring the next branches.
        Once we encounter an unvisited node, we will take one of its neighbor nodes (if exists) as the next node on this
        branch. Recursively call the function to take the next node as the 'starting node' and solve the sub-problem.

        A node remains in the DFS recursion stack until all of its branches (all nodes in its subtree) have been
        explored. When we have examined all of a node's branches, i.e. visited all the nodes in its subtree, the node
        is removed from the DFS recursive stack.

        If the graph has a cycle, we must have a back edge connecting a node to one of its ancestors while traversing
        nodes in the DFS manner.

        To detect the cycle, we must keep track of the visited nodes (like in a normal DFS) and also the nodes in the
        function's recursion call stack for DFS traversal. The nodes in the stack store the current path that we are on.
        There is a cycle in the graph if a node is reached that is already in the recursion stack.

        This is also known as Graph Coloring Algorithm.

            - We build a graph data structure from the given list of course dependencies. Here we adopt the adjacency
               list data structure to represent the graph, which can be implemented using a hashmap. Each entry in the
               adjacency list represents a node which consists of a node index and a list of neighbors nodes that follow
               from the node.

            - We then enumerate each node (course) in the constructed graph, to check if we could form a dependency
               cycle starting from the node.

            - We check if the current node has been explored before, otherwise we enumerate through its child nodes via
               backtracking, where we bread-crumb our path (i.e. mark the nodes we visited) to detect if we come across
               a previously visited node (hence a cycle detected). We also remove the breadcrumbs for each iteration.

            - Once we visited all the child nodes, we mark the current node as checked.

        Recall that DFS maintains a color for each vertex. Initially, all vertices are white (0). When a vertex is
        first discovered, it is colored gray (1). When DFS finishes processing a vertex and all its neighbors, that
        vertex is colored black (2). As soon as we discover an edge from a gray vertex back to a gray vertex, a cycle
        exists, and we can stop.

        If node course has not been visited, then mark it as 0.
        If node course is being visited, then mark it as 1. If we find a vertex marked as 1 during DFS, then this
        vertex is part of a cycle.
        If node course has been visited, then mark it as 2. If a vertex was marked as 2, then no cycle contains course
        or its successors.

        1 means this node is part of the current trip, and either all of its descendants are not processed or it's still
        in the function call stack. If you see it again, it's a cycle.
        2 means the node and all its descendants were processed, and no cycle was found. if we hit this, going down this
        path won't find any cycles.

        In summary, a cycle exists if and only if DFS discovers an edge from a gray (1) vertex to a gray vertex.

        Because the tree is a connected graph, we can start from any node. The graph is possibly not connected, so need
        to check every node.

    Time complexity: O(|V| + |E|), where V is the number of vertices/courses and E is the number of edges/dependencies.
    It would take ∣E∣ time complexity to build the graph in the first step. Since we perform a postorder DFS traversal
    on the graph, we visit each vertex and each edge once and only once in the worst case, i.e. ∣V∣+∣E∣.
    Space complexity: O(|V| + |E|), we build a graph that would consume |V| + |E| space. Then, |V| is the maximum stack
    depth. If we go deeper than |V| calls, some vertex must repeat, implying a cycle in the graph, which leads to
    early termination.
    """
    def dfs(vertex):
        if visited[vertex] == 1:
            # If the current vertex is marked as being visited, then a cycle is found
            return False
        if visited[vertex] == 2:
            # If done exploring the current vertex, then do not visit again
            return True
        visited[vertex] = 1  # Mark the vertex as being visited during current recursion
        for neighbor in graph[course]:
            # Visit all the neighbours
            if not dfs(neighbor):
                return False
        visited[vertex] = 2  # After visiting all the neighbours, mark the vertex as done exploring
        return True

    graph = defaultdict(list)
    for course, prereq in prerequisites:  # Construct the graph
        graph[course].append(prereq)
    visited = [0] * num_courses
    for course in range(num_courses):
        # Visit each node. Since the graph may not be strongly connected, we must examine each vertex and run DFS
        # from it if it has not already been explored
        if not dfs(course):
            return False
    return True


def can_finish_bfs(numCourses, prerequisites):
    """ Kahn's algorithm for topological sorting.

        The problem is to find a global ordering for all nodes in a DAG (Directed Acyclic Graph) with regard to their
        dependencies.

        Kahn’s algorithm works by keeping track of the number of outgoing edges from each node (outdegree). It works by
        repeatedly visiting the nodes with an outdegree of zero and deleting all the edges associated with it leading to
        a decrement of outdegree for the nodes whose outgoing edges are deleted. This process continues until no
        elements with zero outdegree can be found.

        In our case, the nodes with zero outdegree correspond to the nodes which do not have any prerequisites:
        These can be started immediately.

        The algorithm terminates when we can no longer remove edges from the graph. There are two possible outcomes:

            1- If there are still some edges left in the graph, then these edges must have formed certain cycles, which
                 is similar to the deadlock situation. It is due to these cyclic dependencies that we cannot remove them
                 during the above processes.
            2- Otherwise, we have removed all the edges from the graph, and we got ourselves a topological order of the
                 graph.

        A better way to understand this algorithm is to draw the graph and remove edges each time the outdegree of a
        node is reduced, and remember to always start exploring from the nodes that have NO outgoing edges (outdegree=0)

    Time complexity: O(|V| + |E|), where V is the number of vertices/courses and E is the number of edges/prerequisites.
    It would take ∣E∣ time complexity to build the graph. Each queue operation takes O(1) time, and a single node will
    be pushed once, leading to O(|V|) operations. We iterate over the neighbors of each node that is popped out of the
    queue iterating over all the edges once. Since there are total of |E| edges, it would take O(|E|) time to iterate
    over the edges.
    Space complexity: O(|V| + |E|), the graph takes O(|E|) space. The outdegree array takes O(|V|) space. The queue can
    have no more than |V| elements in the worst-case scenario.
    """
    courses_that_depend_on = defaultdict(list)
    outdegree = [0] * numCourses
    for course, prereq in prerequisites:  # Build the graph
        # (courses_that_depend_on[prerq] = course) means 'prereq' is a prerequisite of 'course'
        courses_that_depend_on[prereq].append(course)
        # Record the number of prerequisites (outgoing edges) each course has
        outdegree[course] += 1
    # Iterate over the outdegrees list and find the node that has 0 outdegree, which maps to 0 prerequisites. If none
    # is found, then there must be a cycle.
    queue = deque(course for course in range(numCourses) if outdegree[course] == 0)
    # 'courses_finished' is initialized to len(queue) because the queue contains the courses that have 0
    # prerequisites, so they can be finished without any pre-processing
    courses_finished = len(queue)
    while queue and courses_finished != numCourses:  # adding courses_finished != numCourses to exit the loop early
        course = queue.popleft()
        courses_finished += 1 # One more course has been finished
        for neighbor in courses_that_depend_on[course]:  # Iterate over the courses that have 'course' as prerequisite
            # This is equivalent to removing the edge neighbor -> course, which in other words means taking course
            # 'course' and 'course' is no longer in the list of prerequisite of 'neighbor'
            outdegree[neighbor] -= 1
            if outdegree[neighbor] == 0:  # We've taken all the prerequisites of course 'neighbor'
                queue.append(neighbor)  # Now explore the courses that have 'neighbor' as prerequisite
    return courses_finished == numCourses


class Test(unittest.TestCase):
    data = [(2, [[1, 0]], True), (2, [[1, 0], [0, 1]], False)]

    def test_can_finish(self):
        for test_num_courses, test_prerequisites, result in self.data:
            self.assertEqual(result, can_finish_dfs(test_num_courses, test_prerequisites))
            self.assertEqual(result, can_finish_bfs(test_num_courses, test_prerequisites))


if __name__ == '__main__':
    unittest.main()
