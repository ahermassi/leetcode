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
