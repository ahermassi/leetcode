""" Given an absolute path for a file (Unix-style), simplify it. Or in other words, convert it to the canonical path.
In a UNIX-style file system, a period . refers to the current directory. Furthermore, a double period .. moves the
directory up a level """

import unittest2 as unittest


def simplify_path(path):
    """ The main idea is to push to the stack every valid folder name (not in {'','.','..'}), popping only if there's
        something to pop and we meet '..'
    Time complexity: O(N)
    Space complexity: O(N)
    """
    folders = [folder for folder in path.split('/') if folder and folder != '.']
    stack = []
    for folder in folders:
        if folder == '..':
            if stack:
                stack.pop()
        else:
            stack.append(folder)
    return '/' + '/'.join(stack)


class Test(unittest.TestCase):
    data = [('/home/', '/home'), ('/../', '/'), ('/home//foo/', '/home/foo'), ('/a/./b/../../c/', '/c')]

    def test_simplify_path(self):
        for test_path, result in self.data:
            self.assertEqual(result, simplify_path(test_path))


if __name__ == '__main__':
    unittest.main()