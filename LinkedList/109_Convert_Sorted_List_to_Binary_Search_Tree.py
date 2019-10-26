""" Given a singly linked list where elements are sorted in ascending order, convert it to a height balanced BST.
For this problem, a height-balanced binary tree is defined as a binary tree in which the depth of the two subtrees of
every node never differ by more than 1. """

import unittest2 as unittest

# Definition for singly-linked list.


class ListNode(object):
    def __init__(self, x):
        self.val = x
        self.next = None

# Definition for a binary tree node.


class TreeNode(object):
    def __init__(self, x):
        self.val = x
        self.left = None
        self.right = None


def sorted_list_to_bst_v1(head):
    """ Essentially, we will convert the given linked list into an array and then use that array to form our binary
        search tree. In an array fetching the middle element is a O(1)O(1) operation and this will bring down the
        overall time complexity.
    Time complexity: O(N), since we convert the linked list to an array initially and then we convert the array into BST
    Space complexity: O(N)
    """

    def helper(left, right):
        if left > right:
            return None
        mid = (left + right) // 2
        root = TreeNode(vals[mid])
        # Recursively form binary search trees on the two halves of the array
        root.left = helper(left, mid - 1)
        root.right = helper(mid + 1, right)
        return root

    vals = []
    temp = head
    while temp:
        vals.append(temp.val)
        temp = temp.next
    return helper(0, len(vals) - 1)



