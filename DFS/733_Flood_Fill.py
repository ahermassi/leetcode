""" Check problem description on leetcode.com """

import unittest2 as unittest


def flood_fill(image, sr, sc, new_color):
    """ The idea is simple. Simply perform a DFS on the source cell. Continue the DFS if:
        1- Next cell is within bounds.
        2- Next cell is the same color as source cell.
        There is a tricky case where the new color is the same as the original color and if the DFS is done on it,
        there will be an infinite loop. If new color is same as current cell's color, there is nothing to be done and
        we can simply return the image.
    Time complexity: O(N) where N is the number of pixels in the image. We might process every pixel
    Space complexity: O(N), the size of the implicit call stack when calling fill()
    """
    def get_adjacent(i, j):
        adjacent = [(i - 1, j), (i + 1, j), (i, j - 1), (i, j + 1)]
        return [adj for adj in adjacent if 0 <= adj[0] < rows and 0 <= adj[1] < columns]

    def fill(sr, sc):
        if image[sr][sc] == new_color:
            return
        image[sr][sc] = new_color
        adjacent = get_adjacent(sr, sc)
        for adj in adjacent:
            r, c = adj[0], adj[1]
            if image[r][c] == starting_color:
                fill(r, c)

    rows, columns, starting_color = len(image), len(image[0]), image[sr][sc]
    fill(sr, sc)
    return image


class Test(unittest.TestCase):
    data = [([[1, 1, 1], [1, 1, 0], [1, 0, 1]], 1, 1, 2, [[2, 2, 2], [2, 2, 0], [2, 0, 1]])]

    def test_flood_fill(self):
        for test_image, sr, sc, new_color, result in self.data:
            self.assertEqual(result, flood_fill(test_image, sr, sc, new_color))


if __name__ == '__main__':
    unittest.main()
