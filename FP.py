"""
FP.py
===============================
Contains the classes required to prepare a FPtree.

"""

class FPNode:

    """
    Defines the nodes of the FPtree. Following are its attributes:

    - value: contains the item represented by the node.
    - count: the frequency of the item along that edge of the tree.
    - next_nodes: it is a dictionary of all the children of the current node.
    - parent: a pointer to the parent of the current node.

    """

    def __init__(self,value,parent):

        self.value = value
        self.count = 1
        self.next_nodes = {}
        self.parent = parent

class FPTree:

    """
    Defines the structure of the FPtree. Following are its attributes:

    - root: pointer to the root of the FPtree.
    - curr_node: pointer to the current node of the tree.
    - total_count: a dictionary containing the total frequency of each item in the dataset.

    """

    def __init__(self):

        self.root = FPNode(None,None)
        self.curr_node = self.root
        self.total_count = {}

    def initialize_curr_node(self):
        """
        Makes the curr_node point to the root of the tree.
        """

        self.curr_node = self.root

    def construct_tree(self,transactions):
        """
        Accepts the list of transactions as an argument and constructs a FPtree.
        """

        self.initialize_curr_node()
        for transaction in transactions:
            for i in range(len(transaction)):

                item = transaction[i]
                if item not in self.curr_node.next_nodes:
                    new_node = FPNode(item,self.curr_node)
                    self.curr_node.next_nodes[item] = new_node

                else:
                    self.curr_node.next_nodes[item].count +=1

                self.curr_node = self.curr_node.next_nodes[item]

                if item not in self.total_count:
                    self.total_count[item] = 1
                else:
                    self.total_count[item] += 1

            self.initialize_curr_node()


class FPLists:
    """
    Contains the following attributes:

    - tree: an FPtree of the transactions.
    - lists: a list of pointers to the leaf nodes of the FPtree.
    """

    def __init__(self,FPTree):

        self.tree = FPTree
        self.lists = []

    def dfs(self,curr_node):

        if not curr_node.next_nodes:

            self.lists.append(curr_node)
            return

        else:

            for node in curr_node.next_nodes:
                next_node = curr_node.next_nodes[node]
                self.dfs(next_node)

            return

    def create_lists(self):

        """
        Creates the list of pointers to the leaf nodes of FPtree.
        """

        tree = self.tree
        tree.initialize_curr_node()
        self.dfs(tree.root)

        return
