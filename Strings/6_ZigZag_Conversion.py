""" The string "PAYPALISHIRING" is written in a zigzag pattern on a given number of rows like this: (you may want to
display this pattern in a fixed font for better legibility)

P   A   H   N
A P L S I I G
Y   I   R
And then read line by line: "PAHNAPLSIIGYIR"

Write the code that will take a string and make this conversion given a number of rows. """

import unittest2 as unittest


def convert(s, num_rows):
    """ Construct the final string line by line and then join the lines.
        We start with variable 'line' with the value 0, step with the value 1. Each consequent character is added to
        a specific line.  'step' step is more like a direction. When we are in the first row, the direction should move
        down, i.e. step = +1. When it's the last row, the direction should go up, i.e. step = -1.
    Time complexity: O(N)
    Space complexity: O(N)
    """
    if num_rows == 1 or num_rows >= len(s):
        return s
    ans = [''] * num_rows
    line, step = 0, 1
    for c in s:
        ans[line] += c  # Append character to current line
        if line == 0:  # If we are at the first line, move down (append to following (+1) line in the next iteration)
            step = 1
        elif line == num_rows - 1:   # If we are in the last line, move up (append to prev line in the next iteration)
            step = -1  # Moving backwards
        line += step  # This is what determines which line to append to next: following (+1) or previous (-1)
    return ''.join(ans)


class Test(unittest.TestCase):
    data = [('PAYPALISHIRING', 3, 'PAHNAPLSIIGYIR'), ('PAYPALISHIRING', 4, 'PINALSIGYAHRPI')]

    def test_convert(self):
        for test_string, test_rows, result in self.data:
            self.assertEqual(result, convert(test_string, test_rows))


if __name__ == '__main__':
    unittest.main()