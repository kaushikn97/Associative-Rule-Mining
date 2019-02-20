"""
HashTree.py
===============
Contains the classes implementing a hash tree and the nodes in the tree along with the related methods.
"""
import Preprocess

class HTNode:
    """
    Class implementing the node in the hash tree.
    """
    def __init__(self):

        self.item_sets = []
        self.support_counts = []
        self.children = {}
        self.is_leaf = False

class HTree:
    """
    Class implementing the hash tree used to store frequent item sets along with their support counts.
    """

    def __init__(self,length,mod):

        self.root = HTNode()
        self.length = length
        self.mod = mod

    def insert(self,item_set,supp_count):
        """
        Method to insert a frequent item set into the hashtree along with its support count.
        """
        curr_node = self.root
        count = 0
        for item in item_set:
            count += 1

            remainder = item % self.mod

            if remainder in curr_node.children:

                curr_node = curr_node.children[remainder]

            else:

                curr_node.children[remainder] = HTNode()
                curr_node = curr_node.children[remainder]

            if count == self.length:
                curr_node.is_leaf = True
                if item_set in curr_node.item_sets:

                    curr_node.support_counts[curr_node.item_sets.index(item_set)] += supp_count
                    return

                else:

                    curr_node.item_sets.append(item_set)
                    curr_node.support_counts.append(supp_count)
                    return

    def getSupportCount(self,item_set):
        """
        Method to retrieve the support count of a given item set.
        """
        curr_node = self.root

        for item in item_set:
            if (item % self.mod) in curr_node.children:
                curr_node = curr_node.children[item % self.mod]
            else:
                return 0
        if item_set in curr_node.item_sets:
            return curr_node.support_counts[curr_node.item_sets.index(item_set)]

        else:
            return 0

def findMaxItems(dataset):
    """
    Utility method used to find the maximum number of items in one transaction.
    """
    max_items = 0
    for transaction in dataset:
        items = 0

        for item_present in transaction:
            items +=item_present

        if items > max_items:
            max_items = items

    return max_items

def createHTs(filename):
    """
    Method to create hash trees of all required lengths of item sets given the data file
    """
    dataset,_ = Preprocess.binarizeTransactions(filename)
    max_items = findMaxItems(dataset)
    HTs = []
    for tree_size in range(1,max_items+1):
        htree = HTree(tree_size,15)
        HTs.append(htree)
    return HTs

def generateHTs(filename,freq_sets,min_sup):
    """
    Method to generate hash trees given all frequent item sets along with their support counts.
    """
    HTs = createHTs(filename)
    transactions,_ = Preprocess.binarizeTransactions(filename)
    for curr_set in freq_sets:
        count = 0
        for transaction in transactions:
            temp = []
            count1 = 0
            for item in transaction:
                if item == 1:
                    temp.append(count1)
                count1 += 1
            if all(x in temp for x in curr_set):
                count += 1
        curr_set.sort()
        HTs[len(curr_set)-1].insert(curr_set,count)

    return HTs

def documentFreqSets(HTs,item_list,min_sup,filename):
    """
    Method used to document all the frequent sets found along with their support counts
    """
    f = open("Results/Freq_Items_" + filename + "_sup:" + str(min_sup) + ".txt",'w')

    for HT in HTs:

        writeSetsToFile(HT.root,item_list,f)

    f.close()

def writeSetsToFile(node,item_list,f):
    """
    Recursive method to travers a hash tree and write all item sets along with the support counts to a file.
    """
    curr_node = node
    if(curr_node.is_leaf):
        for item_set,support in zip(curr_node.item_sets,curr_node.support_counts):

            new_item_set = [item_list[index] for index in item_set]
            [f.write(item + ',') for item in new_item_set]
            f.write(str(support))
            f.write("\n")

    else:
        for i in range(15):
            if i in curr_node.children:
                writeSetsToFile(curr_node.children[i],item_list,f)

def documentRules(HTs,item_list,rules,min_sup, conf,filename):
    """
    Method to document all rules that have been found.
    """
    f = open("Results/Assn_Rules_" + filename + "_sup:" + str(min_sup) + "conf:" + str(conf) + ".txt",'w')

    for rule in rules:
        [f.write(item_list[index] + ', ') for index in rule[0]]
        f.write(str(HTs[len(rule[0])-1].getSupportCount(rule[0])) + "  ")
        f.write("---> ")
        [f.write(item_list[index] + ',') for index in rule[1]]
        f.write(str(HTs[len(rule[1])-1].getSupportCount(rule[1]))+ "  ")
        f.write(str(round(rule[2],3))+ "\n")

    f.close()
