""" There are a total of n courses you have to take, labeled from 0 to n-1.
Some courses may have prerequisites, for example to take course 0 you have to first take course 1, which is expressed
as a pair: [0,1]
Given the total number of courses and a list of prerequisite pairs, return the ordering of courses you should take to
finish all courses.
There may be multiple correct orders, you just need to return one of them. If it is impossible to finish all courses,
return an empty array. """

from collections import defaultdict, deque

# Video explanation: https://www.youtube.com/watch?v=Akt3glAwyfY
# Refer to this excellent article for both solutions: https://leetcode.com/articles/course-schedule-ii/


def find_order_v1(num_courses, prerequisites):
    """ We can represent the information provided in the question in the form of a graph.

        Each course would represent a vertex in the graph. The edges are modeled after the prerequisite relationship
        between courses. So, we are given that a pair such as [a, b] in the question means the course b is a
        prerequisite for the course a. This can be represented as a directed edge a ➔ b in the graph.

        There is a possibility of a cycle in the graph. If the graph was acyclic, then an ordering of subjects as
        required in the question would always be possible. Since it's mentioned that such an ordering may not always be
        possible, that means we have a cyclic graph.

        Such an ordering of subjects is referred to as a Topological Sort and this is a common algorithmic problem in
        the graph domain. There are two approaches to solve this problem. One of them is DFS approach. Same logic as
        207- Course Schedule.

        Suppose we are at a node in our graph during the depth first traversal. Let's call this node A.

        The way DFS would work is that we would consider all possible paths stemming from A before finishing up the
        recursion for A and moving onto other nodes. All the nodes in the paths stemming from the node A would have A
        as an ancestor. The way this fits in our problem is, all the courses in the paths stemming from the course A
        would have A as a prerequisite.

        Now we know how to get all the courses that have a particular course as a prerequisite. If a valid ordering of
        courses is possible, the course A would come before all the other set of courses that have it as a prerequisite.
        This idea for solving the problem can be explored using depth-first search.

        For each of the nodes in our graph, we will run a depth-first search in case that node was not already visited
        in some other node's DFS traversal. Suppose we are executing the depth-first search for a node N. We will
        recursively traverse all the neighbors of node N which have not been processed before. Once the processing of
        all the neighbors is done, we will add the node N to the result list.

        Recall that DFS maintains a color for each vertex. Initially, all vertices are white (0). When a vertex is
        first discovered, it is colored gray (1). When DFS finishes processing a vertex and all its neighbors, that
        vertex is colored black (2). As soon as we discover an edge from a gray vertex back to a gray vertex, a cycle
        exists, and we can stop.

        visited[node] == 1 means this node is part of the current trip, and either all of its descendants are not
        processed or it's still in the function call stack. If you see it again, it's a cycle.
        visited[node] == 2: means the node and all its descendants were processed, and no cycle was found. if we hit
        this, going down this path won't find any cycles.

        Another way to think about it is the last few in the order must be those which are not prerequisites of other
        courses. Thinking it recursively means if one node has unvisited child node, we should visit them first before
        we put this node down in the final order array. This sounds like a postorder DFS.

        An important thing to note about Topological Sort is that there won't be just one ordering of nodes (courses).
        There can be multiple.

    Time complexity: O(|V| + |E|), where V is the number of vertices and E is the number of edges. Essentially we
    iterate through each node and each vertex in the graph once and only once.
    Space complexity: O(|V| + |E|), we use the adjacency list to represent our graph initially. The space occupied is
    defined by the number of edges because for each node as the key, we have all its adjacent nodes in the form of a
    list as the value.
    """

    def dfs(node):
        if visited[node] == 1:  # Don't recurse further if we found a cycle already
            return False
        if visited[node] == 2:
            return True
        visited[node] = 1  # Start the recursion
        for neighbor in graph[node]:
            if not dfs(neighbor):
                return False
        res.append(node)
        visited[node] = 2
        return True

    graph = defaultdict(list)
    visited = [0] * num_courses
    for course, prereq in prerequisites:
        graph[course].append(prereq)
    res = []
    for course in range(num_courses):
        # If a cycle exists, no topological ordering exists, and therefore it will be impossible to take all courses.
        if not dfs(course):
            return None
    return res


def find_order_v2(numCourses, prerequisites):
    """ BFS using node in-degree. Very similar to 207- Course Schedule. This is called Kahn's algorithm for topological
        sorting.
        The first node in the topological ordering will be the node that doesn't have any incoming edges. Essentially,
        any node that has an in-degree of 0 can start the topologically sorted order. If there are multiple such nodes,
        their relative order doesn't matter and they can appear in any order.
        We first process all the nodes/courses with 0 in-degree implying no prerequisite courses required. If we remove
        all these courses from the graph, along with their outgoing edges, we can find out the courses/nodes that
        should be processed next. These would again be the nodes with 0 in-degree. We can continuously do this until
        all the courses have been accounted for.
    Time complexity: O(|V| + |E|)
    Space complexity: O(N), where N is the number of courses, since we use an intermediate queue to keep all the nodes
    with 0 in-degree
    """
    graph, indegree = defaultdict(list), [0] * numCourses
    for course, prereq in prerequisites:
        graph[prereq].append(course)  # Create graph, better seen as is_prerequisite_of graph: graph[prepreq] = course
        # means 'prereq' is a prerequisite of 'course'
        indegree[course] += 1  # Recording the number of prerequisites each course has
    queue = deque(course for course in range(numCourses) if indegree[course] == 0)  # Iterate the in-degree list and
    # find the nodes that have 0 in-degree, which maps to 0 prerequisites. If none is found, then there must be a cycle
    # and a topological ordering is not possible.
    res = []
    while queue:
        course = queue.popleft()
        res.append(course)
        for neighbor in graph[course]:
            indegree[neighbor] -= 1
            if indegree[neighbor] == 0:
                queue.append(neighbor)
    return res if len(res) == numCourses else []


