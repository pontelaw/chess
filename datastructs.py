global head
head = None

class LinkNode:
    def __init__(self, next, prev, value):
        self.next = next
        self.prev = prev
        self.value = value

def add(node, value):
    while node != None:
        if value >= node.value:
            if node.next == None:
                node.next = LinkNode(None, node, value)
                break
            elif value < node.next.value:
                node.next = LinkNode(node.next, node, value)
                node.next.next.prev = node.next
                break
            else:
                node = node.next

def print_list(node):
    while node != None:
        print(node.value)
        node = node.next

def remove(node, value):
    while node != None:
        if node.value == value:
            if node.prev == None and node.next == None:
                node = None
                break
            elif node.prev == None:
                node.next.prev = None
                node = node.next
                break
            elif node.next == None:
                node.prev.next = None
                break
            else:
                node.prev.next = node.next
                node.next.prev = node.prev
                break
        else:
            node = node.next
    return "not found"

class TreeNode:
    def __init__(self, value, left, right):
        self.value = value
        self.left = left
        self.right = right

def addT(node, value):
    if node == None:
        return TreeNode(value, None, None)
    elif value < node.value:
        node.left = addT(node.left, value)
        return node
    else:
        node.right = addT(node.right, value)
        return node

def printT(node):
    if node == None:
        return
    printT(node.left)
    print(node.value)
    printT(node.right)

def removeT(node, value):
    if node == None:
        return None
    elif value == node.value:
        if node.left == None and node.right == None:
            return None
        elif node.left == None:
            return node.right
        elif node.right == None:
            return node.left
        else:
            node.value = findMin(node.right)
            node.right = removeT(node.right, node.value)
            return node
    elif value < node.value:
        node.left = removeT(node.left, value)
        return node
    else:
        node.right = removeT(node.right, value)
        return node
    
def findMin(node):
    if node == None:
        return None
    elif node.left == None:
        return node.value
    else:
        return findMin(node.left)
    
def findT(node, value):
    if node == None:
        return None
    elif node.value == value:
        return node
    elif value < node.value:
        return findT(node.left, value)
    else:
        return findT(node.right, value)