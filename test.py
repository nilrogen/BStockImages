from items import ItemContainer, Item

class Node(object):
    def __init__(self, value):
        self.value = value
        self.next = None
        self.prev = None

    def __str__(self):
        return '<({}) {} ({})>'.format(repr(self.prev), repr(self.value),repr(self.next))

class ItemLinkedList(ItemContainer):

    def __init__(self):
        self.head = None
        self.length = 0

    def add(self, other): 
        if type(other) is not Item:
            return

        node = Node(other)
        if self.length == 0:
            self.head = node
        else:
            node.next = self.head
            node.next.prev = node
            self.head = node 
        self.length += 1

    def remove(self, node):
        if self.length == 0:
            return None
        if self.head == node:
            if node.next != None:
                node.next.prev = None
            self.head = node.next
        else: 
            tmp = node.prev
            node.prev.next = node.next
            if node.next != None:
                node.next.prev = tmp
        self.length -= 1
        return node

    def pop(self):
        return self.remove(self.head)

    def __len__(self):
        return self.length

    def __str__(self):
        cur = self.head
        s = ''
        while cur != None:
            s += '{}'.format(cur.value)
            cur = cur.next
        return s

class LinkedListIterator:
    def __init__(self, ll):
        self.list = ll
        self.current = ll.head



if __name__ == '__main__':
    t = ItemLinkedList()

    t.add(Item(123, 'Test'))
    print(str(t))
    t.add(Item(2312454, 'Test'))
    print(str(t))

    t.pop()
    print(str(t))

    t.pop()
    print(str(t))


