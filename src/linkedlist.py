import math

class Node:
    def __init__(self, value=None, next=None):
        """Initialize a node with document ID, next pointer, and skip pointer"""
        self.value = value  
        self.next = next    
        self.skip = None    
        self.score = 0.0    

class LinkedList:
    def __init__(self):
        """Initialize an empty linked list with skip pointers"""
        self.start_node = None
        self.end_node = None
        self.length = 0
        self.n_skips = 0
        self.idf = 0.0      
        self.skip_length = None

    def traverse_list(self):
        """Traverse the linked list normally and return all values"""
        traversal = []
        head = self.start_node
        while head is not None:
            traversal.append(head.value)
            head = head.next
        return traversal

    def traverse_skips(self):
        """Traverse the linked list using skip pointers"""
        traversal = []
        head = self.start_node
        while head:
            if head.skip:
                traversal.append(head.value)
                head = head.skip
                if head.skip is None:
                  traversal.append(head.value)
            else:
                head = head.next
        return traversal


    def add_skip_connections(self):
        """Add skip pointers to the linked list for faster traversal"""
        if self.length <= 2:
            return

        # Calculate number of skips
        self.n_skips = int(math.floor(math.sqrt(self.length)))
        if self.n_skips * self.n_skips == self.length:
            self.n_skips -= 1
        # print(f'there are {self.n_skips} skips')
        # Calculate skip length
        self.skip_length = round(math.sqrt(self.length))

        
        head = self.start_node
        count = 0
        prev_skip = None
        # print(f'each skip length is {self.skip_length}')
        while head is not None:
            if count % self.skip_length == 0 and count + self.skip_length < self.length:
                skip_to = head
                for r in range(self.skip_length):
                    skip_to = skip_to.next
                head.skip = skip_to

                if prev_skip is not None:
                    prev_skip.skip = head
                prev_skip = head

            head = head.next
            count += 1



    def insert_at_end(self, value):
        """Insert a new node at the end of the list and maintain sorting"""
        new_node = Node(value)
        self.length += 1

        
        if self.start_node is None:
            self.start_node = new_node
            self.end_node = new_node
            return

       
        if value < self.start_node.value:
            new_node.next = self.start_node
            self.start_node = new_node
            return

        
        head = self.start_node
        while head.next is not None and head.next.value < value:
            head = head.next

       
        new_node.next = head.next
        head.next = new_node

        if new_node.next is None:
            self.end_node = new_node


    def rare_term(self, total_docs):
        """Finds how rare the term is dividing total documents by total docs with term """
        self.idf = total_docs / self.length



if __name__ == '__main__':
    linked_list =LinkedList()
    linked_list.insert_at_end(3)
    print(linked_list.traverse_list())
    print(linked_list.end_node.value)
    linked_list.insert_at_end(1)
    print(linked_list.traverse_list())
    print(linked_list.end_node.value)
    linked_list.insert_at_end(4)
    print(linked_list.traverse_list())
    print(linked_list.end_node.value)
    linked_list.add_skip_connections()
    print(linked_list.traverse_skips())