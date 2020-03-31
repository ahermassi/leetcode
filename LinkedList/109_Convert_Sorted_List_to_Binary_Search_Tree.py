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
    """ The middle element of the given list would form the root of the binary search tree. All the elements to the
        left of the middle element would form the left subtree recursively. Similarly, all the elements to the right
        of the middle element will form the right subtree of the binary search tree. This would ensure the height
        balance required in the resulting binary search tree.
        We can use the two pointer approach to find the middle element of the linked list. For an even sized list,
        any of the two middle elements can act as the root of the BST.
        Once we have the middle element of the linked list, we disconnect the portion of the list to the left of the
        middle element. The way we do this is by keeping a 'prev' pointer as well which points to one node before the
        'slow' pointer, i.e. prev.next = slow. For disconnecting the left portion we simply do prev.next = None.
        We only need to pass the head of the linked list to the function that converts it to a height balances BST. So,
        we recurse on the left half of the linked list by passing the original head of the list and on the right half
        by passing slow.next as the head.
    Time complexity: O(N logN), suppose our linked list consists of N elements. For every list we pass to our recursive
    function, we have to calculate the middle element for that list. For a list of size N, it takes N/2 steps to find
    the middle element i.e. O(N) to find the middle. We do this for every half of the original linked list
    Space complexity: O(logN), since we are resorting to recursion, there is always the added space complexity of the
    recursion stack that comes into picture. This could have been O(N) for a skewed tree, but the question clearly
    states that we need to maintain the height balanced property. This ensures the height of the tree to be bounded by
    O(logN)
    """
    if not head:
        return None
    if not head.next:  # Base case when there is just one element in the linked list
        return TreeNode(head.val)
    slow, fast, prev = head, head, None  # 'prev' is the pointer used to disconnect the left half from the mid node
    while fast and fast.next:
        prev = slow
        slow = slow.next
        fast = fast.next.next
    if prev:  # Handling the case when 'slow' was equal to head ('prev' is then null)
        prev.next = None
    root = TreeNode(slow.val)  # # The mid becomes the root of the BST
    # Recursively form balanced BSTs using the left and right halves of the original list
    root.left = sorted_list_to_bst_v1(head)
    root.right = sorted_list_to_bst_v1(slow.next)
    return root


def sorted_list_to_bst_v2(head):
    """ This approach is a classic example of the time-space trade-off. WE can get the time complexity down by using
        more space.
        Essentially, we will convert the given linked list into an array and then use that array to form our binary
        search tree. In an array fetching the middle element is a O(1) operation and this will bring down the overall
        time complexity.
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


def sorted_list_to_bst_v3(head):
    """ The critical idea based on the in-order traversal that we will exploit to solve this problem is: We know that
        the leftmost element in the in-order traversal has to be the head of our given linked list. Similarly, the next
        element in the in-order traversal will be the second element in the linked list and so on. This is made
        possible because the initial list given to us is sorted in ascending order.
        Iterate over the linked list to find out its length.
        We will make use of two different pointer variables here to mark the beginning and the end of the list. Let's
        call them 'left' and 'right' with their initial values being 0 and length - 1 respectively.
        Remember, we have to simulate the in-order traversal here. We can find out the middle element by using
        (left + right) / 2.
        Recurse on the left half by using (left, mid - 1) as the starting and ending points.
        The invariance that we maintain in this algorithm is that whenever we are done building the left half of the
        BST, the head pointer in the linked list will point to the root node. So, we simply use the current value
        pointed to by head as the root node and progress the head node by once i.e. head = head.next.
        We recurse on the right hand side using (mid + 1, right) as the starting and ending points.
    Time complexity: O(N), since we still have to process each of the nodes in the linked list once and form
    corresponding BST nodes.
    Space complexity: O(logN) since now the only extra space is used by the recursion stack and since we are building a
    height balanced BST, the height is bounded by logN.
    """

    def in_order(left, right):
        if left > right:
            return None
        nonlocal head
        mid = (left + right) // 2
        left = in_order(left, mid - 1)  # First step of simulated in-order traversal. Recursively form the left half.
        root = TreeNode(head.val)  # Once left half is traversed, process the current node.
        root.left = left
        head = head.next  # Maintain the invariance mentioned in the algorithm.
        root.right = in_order(mid + 1, right)  # Recurse on the right hand side and form BST out of them.
        return root

    if not head:
        return None
    size, temp = 0, head
    while temp:
        size += 1
        temp = temp.next
    return in_order(0, size - 1)







