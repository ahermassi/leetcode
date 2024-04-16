""" You are given a stream of points on the X-Y plane. Design an algorithm that:

Adds new points from the stream into a data structure. Duplicate points are allowed and should be treated as different
points.
Given a query point, counts the number of ways to choose three points from the data structure such that the three points
and the query point form an axis-aligned square with positive area.
An axis-aligned square is a square whose edges are all the same length and are either parallel or perpendicular to the
x-axis and y-axis.

Implement the DetectSquares class:

DetectSquares() Initializes the object with an empty data structure.
void add(int[] point) Adds a new point = [x, y] to the data structure.
int count(int[] point) Counts the number of ways to form axis-aligned squares with point = [x, y] as described above. """

from collections import defaultdict, Counter


class DetectSquaresV1:
    """ The idea is to keep two pieces of information:

            - Counter of points, that is how many times we have each of them
            - List of corresponding y coordinates for each x coordinate, that is given x we can quickly find all points
               that share this x coordinate

        What we need to do:

            - add(point): increment the points counter and append the y coordinate to its respective list

            - count(point): we need to find all points with the same x coordinate, i.e. points in the form (x, y1),
               and then reconstruct the square. There will be two ways to do it: one above the x-axis and one below it.
               Here we need to take into account the count of the points, so we use the counter map for that.

        For a query point p1 = (x, y), we try all the points p2 which have the same x coordinate as p1, i.e. p1.x = p2.x
        Since we now have two points p1 and p2, we can form a square by calculating the positions of the remaining two
        points, p3 and p4.

            - Calculate the square side length: side_length = abs(p1.y - p2.y)

            - Case 1: p3 and p4 are on the left side of the vertical line [p1, p2]:
               p3 = (p1.x - side_length, p2.y)
               p4 = (p1.x - side_length, p1.y)

            - Case 2: p3 and p4 are on the right side of the vertical line [p1, p2]:
               p3 = (p1.x + side_length, p2.y)
               p4 = (p1.x + side_length, p1.y)

    Time complexity: O(1) for add(point), O(N) for count(point) but in practice it is less because usually we do not
    have many points on the same line.
    Space complexity: O(N)
    """

    def __init__(self):
        self.points = defaultdict(int)
        self.x_axis = defaultdict(list)

    def add(self, point):
        x, y = point
        self.points[(x, y)] += 1
        self.x_axis[x].append(y)

    def count(self, point):
        x, y = point
        squares = 0
        for y1 in self.x_axis[x]:
            if y1 == y:
                continue
            side_length = abs(y - y1)
            squares += self.points[(x - side_length, y)] * self.points[(x - side_length, y1)]
            squares += self.points[(x + side_length, y)] * self.points[(x + side_length, y1)]
        return squares


class DetectSquaresV2:
    """ We can apply the same idea but using a single hashmap.

        We store the COUNT of all the points lying on x-axis with x coordinate, and for each point on x-axis, we have
        its corresponding y coordinate such as:

                    x_axis[x][y] = count of points with coordinate (x, y)

        Notice how x_axis map gives us access to the count of points with coordinates (x, y) AND immediate access to all
        points that share the same x coordinate, thus combining the 2 hashmaps of the previous solution.

        For count(point), we need to pick all the points that have the same x coordinate of the query point. For each of
        these points, we calculate the square side length and find remaining two points at same distance on the left and
        right sides of x.

        For a query point p1 = (x, y), we try all the points p2 which have the same x coordinate as p1, i.e. p1.x = p2.x
        Since we now have two points p1 and p2, we can form a square by computing the positions of the remaining two
        points, p3 and p4.

        To get the count of all possible squares, we need to multiply the count of all possible p2, p3, and p4 points.

            - Count of right side squares = count(p3') * count(p4')
            - Count of left side squares = count(p3'') * count(p4'')
            => Result = count(p2) * (count of left side squares + count of right side squares)

    Time complexity: O(1) for add(point), O(N) for count(point)
    Space complexity: O(N)
    """

    def __init__(self):
        self.x_axis = defaultdict(Counter)

    def add(self, point):
        x, y = point
        self.x_axis[x][y] += 1

    def count(self, point):
        x, y = point
        res = 0
        for y1 in self.x_axis[x]:
            if y1 == y:
                continue
            side_length = abs(y - y1)
            squares = 0
            squares += self.x_axis[x - side_length][y] * self.x_axis[x - side_length][y1]
            squares += self.x_axis[x + side_length][y] * self.x_axis[x + side_length][y1]
            squares *= self.x_axis[x][y1]
            res += squares
        return res


# Video explanation: https://youtu.be/bahebearrDc
class DetectSquaresV3:
    """ Similar to the first solution, we maintain a counter of points, that is how many times we have each of them, in
        a hashmap.

        However, for a query point p1 = (x, y), we try all the points p2 which together with p1 form the diagonal of
        a non-empty square, i.e. abs(p1.x - p2.x) == abs(p1.y - p2.y) and p1.x != p2.x

        Since we now have two points p1 and p2, we can form a square by calculating the positions of the two remaining
        points, p3 and p4:

                    p3 = (p1.x, p2.y)
                    p4 = (p2.x, p1.y)

    Time complexity: O(1) for add(point), O(N) for count(point)
    Space complexity: O(N)
    """

    def __init__(self):
        self.points = defaultdict(int)

    def add(self, point):
        x, y = point
        self.points[(x, y)] += 1

    def count(self, point):
        x, y = point
        res = 0
        # Attempting to access a non-existent key in a defaultdict will add that key (with a value of zero in this
        # case). This causes the dictionary to mutate during iteration, which throws an error.
        # Therefore, we have to 1) make a copy of the list of keys before iterating, and 2) include the diagonal
        # point's count in the multiplication before adding to the result. This is because the call to .keys() will
        # never include duplicates, whereas iterating over a list will allow us to come across multiple copies of
        # the diagonal point.
        keys = list(self.points.keys())
        for x1, y1 in keys:
            # Skip empty square or invalid square point. Diagonal points CAN NOT lie on the same x-axis.
            if x1 != x and abs(x1 - x) == abs(y1 - y):
                res += self.points[(x1, y1)] * self.points[(x, y1)] * self.points[(x1, y)]
        return res
