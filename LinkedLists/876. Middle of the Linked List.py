# Definition for singly-linked list.
class ListNode:
    def __init__(self, x):
        self.val = x
        self.next = None


class Solution:
    @staticmethod
    def middle_node(head: ListNode) -> ListNode:
        slow = fast = head
        while fast and fast.next:
            slow = slow.next
            fast = fast.next.next
        return slow


def print_list(head):
    if not head:
        print('List is empty.')
        return
    while head:
        print(head.val, end=' ')
        head = head.next
    print()


if __name__ == '__main__':
    head = ListNode(1)
    head.next = ListNode(2)
    head.next.next = ListNode(3)
    head.next.next.next = ListNode(4)
    head.next.next.next.next = ListNode(5)
    print('List:', end=' ')
    print_list(head)
    print('Middle of list:', end=' ')
    print_list(Solution.middle_node(head))
    head.next.next.next.next.next = ListNode(6)
    print('Added node 6 ..')
    print('Middle of list:', end=' ')
    print_list(Solution.middle_node(head))
