""" Given a list of folders, remove all sub-folders in those folders and return in any order the folders after removing.

If a folder[i] is located within another folder[j], it is called a sub-folder of it.

The format of a path is one or more concatenated strings of the form: / followed by one or more lowercase English
letters. For example, /leetcode and /leetcode/problems are valid paths while an empty string and / are not. """


def remove_sub_folders_v1(folder):
    """" Strings with sub-folders will always be longer than the ones that include their parents.
         When the input is sorted, all we need to do is iterate through all the input strings and look at the last found
         parent which will be the only viable candidate to be a parent. If it's not, then the current string is a
         parent. Since the instructions state that the folders are unique, we don't need to check the if there are
         multiple same parents.
         We use these observations to form the solution.
    Time complexity: O(N logN + N * M), where N is the size of 'folder' and M is the length of longest path in 'folder'
    Space complexity: O(N), dominated by sort
    """
    folder.sort()
    parent_folders = []
    for f in folder:
        if not parent_folders or not f.startswith(parent_folders[-1] + '/'):
            # Need '/' to ensure a parent. Example: /a/b is NOT parent of /a/bc
            parent_folders.append(f)
    return parent_folders


class Trie(object):
    def __init__(self):
        self.children = dict()
        self.path_index = -1


def remove_sub_folders_v2(folder):
    """ Use 'path_index' to save each folder path's index in a trie node. When we search the trie, if we find a parent
        folder (path_index >= 0), we append it to the result. Otherwise, we keep exploring all the parent folders on
        the current trie branch.
    Time complexity: O(N + M), where N is the number of folders and M is the length of longest path in 'folder'.
    O(N) to create the trie and O(M) to find parent folders.
    Space complexity: O(N), where N is the number of folders
    """

    def insert_folders(root):
        for i, path in enumerate(folder):
            cur = root
            for part in path.split('/')[1:]:  # When we split a path by '/', the first part is an empty string
                if part not in cur.children:
                    cur.children[part] = Trie()
                cur = cur.children[part]
            cur.path_index = i

    def dfs(root):
        if root.path_index != -1:
            res.append(folder[root.path_index])
        else:
            for child in root.children.values():
                dfs(child)

    root = Trie()
    insert_folders(root)
    res = []
    dfs(root)
    return res



