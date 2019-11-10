""" Check problem description on leetcode """

import unittest2 as unittest


def flood_fill_v1(image, sr, sc, new_color):
    """ The idea is simple. Simply perform a DFS on the source cell. Continue the DFS if:
        1- Next cell is within bounds.
        2- Next cell is the same color as source cell.
        Use a 'visited' set to avoid infinite looping and visiting cells for ever.
    Time complexity: O(N * M) where N is the number of lines and M is the number of columns
    Space complexity: O(N * M), the size of the implicit call stack when calling fill()
    """
    def fill(i, j):
        if not 0 <= i < n or not 0 <= j < m or (i, j) in visited or image[i][j] != starting_color:
            return
        image[i][j] = new_color
        visited.add((i, j))
        for x, y in (i - 1, j), (i + 1, j), (i, j - 1), (i, j + 1):
            fill(x, y)

    n, m = len(image), len(image[0])
    starting_color = image[sr][sc]
    visited = set()
    fill(sr, sc)
    return image


def flood_fill_v2(image, sr, sc, new_color):
    """ Exact same as previous solution but without using 'visited' set.
        There is a tricky case where the new color is the same as the original color and if the DFS is done on it,
        there will be an infinite loop. If new color is same as current cell's color, there is nothing to be done and
        we can simply return.
    Time complexity: O(N * M)
    Space complexity: O(N * M)
    """

    def fill(i, j):
        if not 0 <= i < n or not 0 <= j < m or image[i][j] != starting_color or image[i][j] == new_color:
            return
        image[i][j] = new_color
        for x, y in (i - 1, j), (i + 1, j), (i, j - 1), (i, j + 1):
            fill(x, y)

    n, m = len(image), len(image[0])
    starting_color = image[sr][sc]
    fill(sr, sc)
    return image


class Test(unittest.TestCase):
    data = [([[1, 1, 1], [1, 1, 0], [1, 0, 1]], 1, 1, 2, [[2, 2, 2], [2, 2, 0], [2, 0, 1]])]

    def test_flood_fill(self):
        for test_image, sr, sc, new_color, result in self.data:
            self.assertEqual(result, flood_fill_v1(test_image, sr, sc, new_color))
            self.assertEqual(result, flood_fill_v2(test_image, sr, sc, new_color))


if __name__ == '__main__':
    unittest.main()
