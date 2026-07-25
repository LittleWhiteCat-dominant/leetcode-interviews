class Node:
    def __init__(self, key = 0, value = 0):
        self.key = key
        self.value = value
        self.prev = None
        self.next = None

class LRUCache:

    def __init__(self, capacity):
        self.capacity = capacity
        self.cache = {} # {key: Node(key, value)}
        self.head = Node()
        self.tail = Node()
        self.head.next = self.tail
        self.tail.prev = self.head

    def _disconnect_node(self, node):
        node.prev.next = node.next
        node.next.prev = node.prev

    def _remove_node(self, key):
        node = self.cache[key]
        self._disconnect_node(node)
        del self.cache[key]

    def _insertAtHead(self, node):
        node.prev = self.head
        node.next = self.head.next
        self.head.next.prev = node
        self.head.next = node

    def get(self, key):
        if key in self.cache:
            node = self.cache[key]
            self._disconnect_node(node)
            self._insertAtHead(node)
            return node.value
        return -1

    def put(self, key, value):
        if key in self.cache:
            node = self.cache[key]
            node.value = value
            self._disconnect_node(node)
            self._insertAtHead(node)
            return

        if len(self.cache) >= self.capacity:
            self._remove_node(self.tail.prev.key)

        newNode = Node(key, value)
        self.cache[key] = newNode
        self._insertAtHead(newNode)