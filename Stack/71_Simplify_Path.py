""" Given an absolute path for a file (Unix-style), simplify it. Or in other words, convert it to the canonical path.
In a UNIX-style file system, a period . refers to the current directory. Furthermore, a double period .. moves the
directory up a level """

import unittest2 as unittest


# Video explanation: https://youtu.be/qYlHrAKJfyA
def simplify_path(path):
    """  Let's work our way through the problem to understand why a stack fits in here. Suppose that to a path like
         '/a/b/c', we add another component like '/a/b/c/..' Now, this is interesting because the '..' is no longer a
         subdirectory name. It has a special meaning and an indication to the operating system to move up one level in
         the directory structure thus transforming the overall path to just '/a/b'. It's as if we 'popped out' the
         subdirectory c from the overall path. That's the core idea of this problem.

         The only actionable special character is '..'. The single dot is kind of a no-op because it simply means the
         current directory, so nothing changes in the overall path as such.

            - Split the input string using '/' as the delimiter. This step is really important because no matter what,
               the given input is a valid path, and we simply have to shorten it. So, that means that whatever we have
               between two '/' characters is either a directory name or a special character, and we have to process them
               accordingly.

            - Once we are done splitting the input path, we will process one component at a time.

            - If the current component is a '.' or an empty string, we will do nothing and simply continue. If you think
               about it, the split string array for the string '/a//b' would be ['a','','b']. Yes, that's an empty
               string between 'a' and 'b'. Again, from the perspective of the overall path, it doesn't mean anything.

            - If we encounter a double-dot '..', we have to do some processing. This simply means go one level up in the
               current directory path. So, we will pop an entry from our stack if it's not empty.

            - If the current component is not one of the special characters, then we will simply add it to the stack
               because it's a legitimate directory name.

            - Once we are done processing all the components, we simply have to connect all the directory names in the
               stack together using '/' as delimiter, and we will have the shortest path that leads us to the same
               directory as the one provided as an input.

    Time complexity: O(N)
    Space complexity: O(N)
    """
    directories = [directory for directory in path.split('/')]
    stack = []
    for directory in directories:
        if directory == '..':
            if stack:
                stack.pop()
        elif directory and directory != '.':
            stack.append(directory)
    return '/' + '/'.join(stack)


class Test(unittest.TestCase):
    data = [('/home/', '/home'), ('/../', '/'), ('/home//foo/', '/home/foo'), ('/a/./b/../../c/', '/c')]

    def test_simplify_path(self):
        for test_path, result in self.data:
            self.assertEqual(result, simplify_path(test_path))


if __name__ == '__main__':
    unittest.main()
