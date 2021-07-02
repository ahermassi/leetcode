""" Given an absolute path for a file (Unix-style), simplify it. Or in other words, convert it to the canonical path.
In a UNIX-style file system, a period . refers to the current directory. Furthermore, a double period .. moves the
directory up a level """

import unittest2 as unittest


def simplify_path(path):
    """ Suppose that to a path like '/a/b/c', we add another component like '/a/b/c/..' Now, this is interesting
        because the '..' is no longer a sub-directory name. It has a special meaning and an indication to the operating
        system to move up one level in the directory structure thus transforming the overall path to just '/a/b'. It's
        as if we 'popped out' the subdirectory c from the overall path. That's the core idea of this problem.
        Split the input string using '/' as the delimiter.
        If the current component is a '.' or an empty string, we will do nothing and simply continue. Well if you
        think about it, the split string array for the string '/a//b' would be ['a','','b']. Yes, that's an empty
        string in between 'a' and 'b'. Again, from the perspective of the overall path, it doesn't mean anything.
        If we encounter a double-dot '..', we have to do some processing. This simply means go one level up in the
        current directory path. So, we will pop an entry from our stack if it's not empty.
        Finally, if the component we are processing right now is not one of the special characters, then we will simply
        add it to our stack because it's a legitimate directory name.
    Time complexity: O(N)
    Space complexity: O(N)
    """
    folders = [folder for folder in path.split('/')]
    stack = []
    for folder in folders:
        if folder == '..':
            if stack:
                stack.pop()
        elif folder and folder != '.':
            stack.append(folder)
    return '/' + '/'.join(stack)


class Test(unittest.TestCase):
    data = [('/home/', '/home'), ('/../', '/'), ('/home//foo/', '/home/foo'), ('/a/./b/../../c/', '/c')]

    def test_simplify_path(self):
        for test_path, result in self.data:
            self.assertEqual(result, simplify_path(test_path))


if __name__ == '__main__':
    unittest.main()
