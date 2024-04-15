""" The string "PAYPALISHIRING" is written in a zigzag pattern on a given number of rows like this: (you may want to
display this pattern in a fixed font for better legibility)

P   A   H   N
A P L S I I G
Y   I   R
And then read line by line: "PAHNAPLSIIGYIR"

Write the code that will take a string and make this conversion given a number of rows. """

import unittest2 as unittest


def convert(s, num_rows):
    """ Construct the final string line by line and then join the lines together.

         We start with a variable 'row_index' set to 0, 'direction' with the value 1. Each consequent character is
         added to a specific line. When we are in the first row, the direction should move down, i.e. direction = 1.
         When it's the last row, the direction should go back up, i.e. direction = -1.

            - We start with variable 'row_index' with the value 0, 'direction' set to 1 (or -1).

            - Each character is appended to the line pointed to by 'row_index'.

            - If we reach the bottom row, we need to go back up to the row above, so we change 'direction' value to -1
               and start moving up. We keep 'direction' value unchanged until we reach the top row.

            - Again, if we reach the top row, we need to reset 'direction' value to 1 and start moving down.

        What we need to remember is: the zigzag pattern is just a pictorial image for us to have a better understanding.
        The trick of the algorithm is actually adding the next character of the string to different rows.

        Don't think about how to move the cursor in the matrix. It's really a misleading way of thinking. Even if it
        works, it's not efficient.

        This can be better understood by looking at the contents of 'rows' list in each iteration. Take the string
        "PAYPALISHIRING" for example:

            P ['P', '', '']
            A ['P', 'A', '']
            Y ['P', 'A', 'Y']
            P ['P', 'AP', 'Y']
            A ['PA', 'AP', 'Y']
            L ['PA', 'APL', 'Y']
            I ['PA', 'APL', 'YI']
            S ['PA', 'APLS', 'YI']
            H ['PAH', 'APLS', 'YI']
            I ['PAH', 'APLSI', 'YI']
            R ['PAH', 'APLSI', 'YIR']
            I ['PAH', 'APLSII', 'YIR']
            N ['PAHN', 'APLSII', 'YIR']
            G ['PAHN', 'APLSIIG', 'YIR']

    Time complexity: O(N)
    Space complexity: O(N)
    """
    if num_rows == 1:
        return s
    rows = [''] * num_rows # This list will hold num_rows rows that will be joined together to form the final result
    row_index = 0
    # 'direction' is initially set to -1 (go up) so that it's reset to 1 (go down) the first time the loop runs. If we
    # want to initialize direction = 1, we would need to have 2 checks:
    # if row_index == 0: direction = 1
    # elif row_index == num_rows - 1: direction = -1
    direction = -1
    for c in s:
        rows[row_index] += c # Append the current character to the corresponding line
        if row_index == 0 or row_index == num_rows - 1:
            # If we are at the first line, move down (append to the next (+1) line in the next iteration).
            # # If we are at the last line, move up (append to the previous line in the next iteration)
            direction *= -1
        row_index += direction # This is what determines which line to append to next: following (+1) or previous (-1)
    return ''.join(rows)
    # Note: Python string is immutable and appending a character to it can cause a new allocation of the whole string.
    # Therefore, 'rows' list can be a list of character lists.
    # rows = [[] for _ in range(numRows)]
    # rows[row_index].append(c)
    # chars = [c for row in rows for c in row]
    # return ''.join(chars)
    # Or simply return ''.join(''.join(row) for row in rows)


class Test(unittest.TestCase):
    data = [('PAYPALISHIRING', 3, 'PAHNAPLSIIGYIR'), ('PAYPALISHIRING', 4, 'PINALSIGYAHRPI')]

    def test_convert(self):
        for test_string, test_rows, result in self.data:
            self.assertEqual(result, convert(test_string, test_rows))


if __name__ == '__main__':
    unittest.main()