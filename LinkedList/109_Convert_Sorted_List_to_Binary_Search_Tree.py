""" Given a singly linked list where elements are sorted in ascending order, convert it to a height balanced BST.
For this problem, a height-balanced binary tree is defined as a binary tree in which the depth of the two subtrees of
every node never differ by more than 1. """

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
    """ The main idea in this approach is that the middle element of the given list would form the root of the binary
        search tree. All the elements to the left of the middle element would form the left subtree recursively.
        Similarly, all the elements to the right of the middle element will form the right subtree of the binary search
        tree. This would ensure the height balance required in the resulting binary search tree.
        Since we are given a linked list and not an array, we don't really have access to the elements of the list
        using indexes. We want to know the middle element of the linked list.
        We can use the two pointer approach to find the middle element of the linked list. For an even sized list,
        any of the two middle elements can act as the root of the BST.
        Once we have the middle element of the linked list, we disconnect the portion of the list to the left of the
        middle element. The way we do this is by keeping a 'prev' pointer as well which points to one node before the
        'slow' pointer, i.e. prev.next = slow. For disconnecting the left portion we simply do prev.next = None.
        We only need to pass the head of the linked list to the function that converts it to a height balanced BST. So,
        we recurse on the left half of the linked list by passing the original head of the list and on the right half
        by passing slow.next as the head.
    Time complexity: O(N logN), suppose our linked list consists of N elements. For every list we pass to our recursive
    function, we have to calculate the middle element for that list. For a list of size N, it takes N/2 steps to find
    the middle element i.e. O(N) to find the middle. We do this for every half of the original linked list:
                                                      logN
        N/2 + 2 N/4 + 4 N/8 + .. = N/2 + N/2 + N/2 + .. =  Σ    N/2 = N logN
                                                      i=1
    Space complexity: O(logN), since we are resorting to recursion, there is always the added space complexity of the
    recursion stack that comes into picture. This could have been O(N) for a skewed tree, but the question clearly
    states that we need to maintain the height balanced property. This ensures the height of the tree to be bounded by
    O(logN)
    """
    if not head:
        return None
    if not head.next:  # Base case where there is just one element in the linked list
        return TreeNode(head.val)
    slow, fast, prev = head, head, None  # 'prev' is the pointer used to disconnect the left half from the mid node
    while fast and fast.next:
        prev = slow
        slow = slow.next
        fast = fast.next.next
    if prev:  # Handling the case where 'slow' was equal to head ('prev' is then null)
        prev.next = None
    root = TreeNode(slow.val)  # The mid becomes the root of the BST
    # Recursively form balanced BSTs using the left and right halves of the original list
    root.left = sorted_list_to_bst_v1(head)
    root.right = sorted_list_to_bst_v1(slow.next)
    return root


def sorted_list_to_bst_v2(head):
    """ This approach is a classic example of the time-space trade-off: We can get the time complexity down by using
        more space. Essentially, we will convert the given linked list into a (sorted) array and then use that array to
        form our binary search tree. In an array, fetching the middle element is an O(1) operation and this will bring
        down the overall time complexity.
    Time complexity: O(N), since we convert the linked list to an array initially and then convert the array to a
    binary search tree
    Space complexity: O(N)
    """

    def construct_tree(left, right):
        if left > right:
            return None
        mid = (left + right) // 2
        root = TreeNode(values[mid])
        # Recursively form binary search trees on the two halves of the array
        root.left = construct_tree(left, mid - 1)
        root.right = construct_tree(mid + 1, right)
        return root

    values, cur = [], head
    while cur:
        values.append(cur.val)
        cur = cur.next
    return construct_tree(0, len(values) - 1)


def sorted_list_to_bst_v3(head):
    """ The critical idea based on the in-order traversal that we will exploit to solve this problem is: We know that
        the leftmost element in the in-order traversal has to be the head of our given linked list. Similarly, the next
        element in the in-order traversal will be the second element in the linked list and so on. This is made
        possible because the initial list given to us is sorted in ascending order.
        Now that we have an idea about the relationship between the in-order traversal of a binary search tree and the
        numbers being sorted in ascending order, let's get to the algorithm.
        In order to build a height-balanced binary search tree, we need to ensure that roughly half of the total number
        of nodes are on either side of the root, and the only way to know what half of the total number of nodes is
        requires finding the total number of nodes first.
        Iterate over the linked list to find out its length.
        We will make use of two different pointer variables here to mark the beginning and the end of the list. Let's
        call them 'left' and 'right' with their initial values being 0 and (length - 1) respectively.
        Remember, we have to simulate the in-order traversal here. We can find out the middle element by using
        (left + right) / 2.
        Recurse on the left half by using (left, mid - 1) as the starting and ending points.
        The invariance that we maintain in this algorithm is that whenever we are done building the left half of the
        BST, the head pointer in the linked list will point to the root node. So, we simply use the current value
        pointed to by head as the root node and progress the head node by once i.e. head = head.next.
        We recurse on the right hand side using (mid + 1, right) as the starting and ending points.
        We also keep one more piece of information: 'head' as a global variable, which will help us have quick access
        to the desired elements: On step i in in-order traversal, 'head' will point to the ith element of linked list.
        More precisely, after we run in_order(start, end), 'head' points to the element at index (end + 1) in the
        linked list. This is the invariant of the in_order() function.
        Even though we won't be able to access the list nodes directly by index number, we can take advantage of the
        in-order tree traversal to force our access to go in iterative order.
    Time complexity: O(N), since we still have to process each of the nodes in the linked list once and form
    corresponding BST nodes.
    Space complexity: O(logN), since now the only extra space is used by the recursion stack and since we are
    building a height-balanced BST, the height is bounded by logN.
    """

    def in_order(left, right):
        if left > right:
            return None
        mid = (left + right) // 2
        left = in_order(left, mid - 1)  # First step of simulated in-order traversal. Recursively form the left half.
        root = TreeNode(cur[0].val)  # Once left half is traversed, process the current node
        root.left = left
        cur[0] = cur[0].next  # Maintain the invariance
        root.right = in_order(mid + 1, right)  # Recurse on the right hand side and form BST out of them
        return root

    if not head:
        return None
    size, cur = 0, head
    while cur:
        size += 1
        cur = cur.next
    cur = [head]  # Avoid the use of a global 'head' variable
    return in_order(0, size - 1)


def sorted_list_to_bst_v4(head):
    """ Same idea as the first solution, but without modifying the input linked list's structure. We use two pointers
        'head' and 'tail' as delimiters to mark the boundaries of head and tail of the current sub linked list being
        processed in each recursive call.
    Time complexity: O(N logN)
    Space complexity: O(logN)
    """

    def construct_tree(head, tail):  # Note that 'head' is inclusive and 'tail' is exclusive
        if head == tail:
            return None
        slow, fast = head, head
        while fast != tail and fast.next != tail:  # Similar to 'while fast and fast.next' when tail == None
            slow, fast = slow.next, fast.next.next
        root = TreeNode(slow.val)
        root.left = construct_tree(head, slow)
        root.right = construct_tree(slow.next, tail)
        return root

    if not head:
        return None
    if not head.next:
        return TreeNode(head.val)
    return construct_tree(head, None)







