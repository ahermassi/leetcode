""" You need to construct a binary tree from a string consisting of parenthesis and integers.

The whole input represents a binary tree. It contains an integer followed by zero, one or two pairs of parenthesis.
The integer represents the root's value and a pair of parenthesis contains a child binary tree with the same structure.

You always start to construct the left child node of the parent first if it exists. """

# Definition for a binary tree node


class TreeNode(object):
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


def str2tree_v1(s):
    """ The idea here is very simple. An opening bracket represents the start of a new tree (subtree in fact). Thus,
        whenever we encounter a new opening bracket, we make a new recursion call. A recursion call to our function
        will essentially return the root of a properly built tree with all the required TreeNode objects and proper
        connections set up between them. Thus, making a new recursive call upon encountering an opening bracket is
        essentially calling our function to build the subtree and return the root node.
        We know when to make a new recursive call, but, when do we stop? We stop when we encounter a closing bracket.
        That's because a closing bracket will be the end of the most recent subtree that we're building in our
        recursion. We assume that a particular closing bracket matches with the nearest opening bracket we would have
        encountered previously when we made the recursive call.
        build_tree(index) does all the heavy lifting for us. It takes the index of the current character as input and
        returns a pair of the TreeNode representation of the current subtree and also the index of the next character
        to be processed in the string. This index manipulation is important because we don't want to parse the string
        twice to figure out the boundaries for the children subtrees.
        Whenever the function build_tree(index) is called, we expect that the current subtree will all its children and
        descendants will be constructed and returned. There are 4 steps we take inside this function:
            1- Firstly we check for the termination condition i.e. if there are no more characters left in the string
               to process or the character at the current index is a closing bracket.
            2- Next, we get the value for the root node of this tree. This is an invariant here. We will never find
               any brackets before we get the value for the root node.
            3- Once we have the value, we form the root node.
            4- Then, we check for an opening bracket (make sure to check for the end of string conditions always). If
               there is one, we make a recursive call and use the node returned as the left child of the current node.
            5- Finally, we check if there's another opening bracket. If there is one, then it represents our right
               child and we again make a recursive call to construct that and make the right connection.
            6- We return the constructed root node and also the next index to process.
    Time complexity: O(N), where N represents the number of characters in the string representation. This is because
    each character is processed exactly once and we need to process the entire string to form our tree
    Space complexity: O(h), where h represents the height of the tree. We don't have any information about if the tree
    is balanced or not and so, in the worst case when the tree would be skewed left (can't be right according to the
    problem), we will have a recursion stack consisting of N calls and hence the overall space complexity can be O(N)
    """

    def build_tree(index):
        if index == n:
            return None, -1
        if s[index] == ')':
            return None, index + 1  # Subtree ends here. Return the following index to process
        num, next_index = get_number(index)
        root = TreeNode(num)
        if next_index < n and s[next_index] == '(':
            # If there is any data left, we check for the first subtree which, according to the problem statement,
            # will always be the left child
            root.left, next_index = build_tree(next_index + 1)
        if next_index < n and s[next_index] == '(':
            root.right, next_index = build_tree(next_index + 1)
        return root, next_index + 1  # Subtree construction done. Return the following index to process

    def get_number(index):
        i = index
        while i < n and s[i] not in ('(', ')'):
            i += 1
        return int(s[index:i]), i

    n = len(s)
    return build_tree(0)[0]


def str2tree_v2(s):
    """ The main problem with a recursive solution is the stack limitation. We might run into stack-overflow problems
        if the tree is too tall and the system's stack is low on resources. Hence, we prefer to use our own stack and
        that is the variation which we will explore in this solution.
        We iterate over the string. If we meet an opening bracket, we move on. If we encounter a minus sign or a digit,
        we extract the decimal value and create a new node for that number that we push to the stack. If we meet a
        closing bracket, the element we pop should be left child of the element on top of the stack if there is no left
        child yet, otherwise it will be the right child.
    Time complexity: O(N), where N represents the number of characters in the string representation. This is because
    each character is processed exactly once and we need to process the entire string so as to form our tree.
    Space complexity: O(h)
    """
    if not s:
        return None
    stack = []
    i, n = 0, len(s)
    while i < n:
        c = s[i]
        if c == '(':
            i += 1
        elif c.isdigit() or c == '-':
            j = i
            while i < n and s[i] not in ('(', ')'):
                i += 1
            num = int(s[j:i])
            node = TreeNode(num)
            stack.append(node)
        else:  # c == ')'
            node = stack.pop()
            if stack[-1].left:
                stack[-1].right = node
            else:
                stack[-1].left = node
            i += 1
    return stack.pop()
