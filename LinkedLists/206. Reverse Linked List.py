# Definition for singly-linked list.
class ListNode:
    def __init__(self, x):
        self.val = x
        self.next = None


class Solution:
    @staticmethod
    def reverse_list(head: ListNode) -> ListNode:
        if not head or not head.next:
            return head
        stack = []
        while head:
            stack.append(ListNode(head.val))
            head = head.next
        for i in reversed(range(1, len(stack))):
            stack[i].next = stack[i - 1]
        stack[0].next = None
        return stack[-1]

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
    print('Reversed list:', end=' ')
    print_list(Solution.reverse_list(head))
