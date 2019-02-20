"""
FPGrowth.py
=============================
Contains the  method  FPGrowthAlgo and related methods required to create FPtree for getting
the frequent sets.

"""

import csv
import copy
from FP import *
import Preprocess
from HashTree import createHTs,HTree,HTNode


def sort_items_by_support(transactions,items_dict):

    """
    Accepts two arguments,the list of transactions and a dictionary of items. It counts the frequency
    of each item in the transaction and returns a list sorted in descending order of the frequency
    of items.

    """

    items = {}

    for transaction in transactions:
        for item in transaction:
            item_index = items_dict[item]
            if item_index not in items:
                items[item_index] = 1
            else:
                items[item_index] += 1

    items = sorted(items.items(), key=lambda kv: kv[1], reverse = True)
    return items


def update_transactions(transactions,items_dict,item_list_sorted):

    """
    Changes the order of the items present in a transaction based on the
    order of items given in the list item_list_sorted.

    """

    for transaction in transactions:
        for i in range(len(transaction)):
            item = transaction[i]
            transaction[i] = items_dict[item]


    for i in range(len(transactions)):
        new_transaction = []
        transaction = transactions[i]

        for x in item_list_sorted:
            if x[0] in transaction:
                new_transaction.append(x[0])

        for x in transaction:
            if x not in new_transaction:
                new_transaction.append(sx)

        transactions[i] = new_transaction

    return transactions


def process(tree_lists,items,index,frequent_sets,temp_list,len_trans,min_sup,HTs):

    """

    It is a recursive function that checks whether a given sequence of items
    is a frequent set. If it is appends the sequence into the list frequent_sets.

    """

    item = items[index][0]
    #print(tree_lists.tree.total_count)
    if tree_lists.tree.total_count[item]/len_trans < min_sup:
        return
    else:
        temp_list.append(item)
        frequent_sets.append(temp_list)
        # for i in range(len(tree_lists.lists)):
        #     node = tree_lists.lists[i]
        #     if node == None:
        #         print(None)
        #     else:
        #         print(node.value)
        #
        # print("temp_list = ",temp_list)
        # print(tree_lists.tree.total_count)
        # print("\n");
        HTs[len(temp_list)-1].insert(temp_list,tree_lists.tree.total_count[item])

        if index == 0:                                      # if last item is inserted , return
            return

        for x in tree_lists.tree.total_count:                # make total count zero for every item
            tree_lists.tree.total_count[x] = 0

        for i in range(len(tree_lists.lists)):

            if tree_lists.lists[i] == None:
                continue

            ptr = tree_lists.lists[i]
            while ptr.value != None:
                if ptr.value == item:
                    break
                else:
                    ptr = ptr.parent

            if ptr.value != item:
                tree_lists.lists[i] = None
            else:
                tree_lists.lists[i] = ptr                   # make first node of the path item

        count_list = []

        for i in range(len(tree_lists.lists)):
            curr_node = tree_lists.lists[i]

            if curr_node == None:
                count_list.append(0)
                continue

            else:
                count_list.append(curr_node.count)
                while(curr_node.value != None):
                    curr_node.count = 0
                    curr_node = curr_node.parent                              # make every node value zero


        for i in range(len(tree_lists.lists)):

            curr_node = tree_lists.lists[i]
            if curr_node ==  None or curr_node.count != 0:
                tree_lists.lists[i] = None
                continue

            else:
                freq = count_list[i]
                while(curr_node.value != None):
                    curr_node.count += freq
                    tree_lists.tree.total_count[curr_node.value] += freq
                    curr_node = curr_node.parent            # update count of nodes in the paths


        path_count_list = []
        for i in range(len(tree_lists.lists)):
            if tree_lists.lists[i] == None:
                path_count_list.append(None)
                continue
            else:
                path_count = []
                curr_node = tree_lists.lists[i]
                while(curr_node.value != None):
                    path_count.append(curr_node.count)
                    curr_node = curr_node.parent

                path_count_list.append(path_count)


        total_count_copy = copy.deepcopy(tree_lists.tree.total_count)
        for i in range(index-1,-1,-1):

            #tree_lists_copy = copy.deepcopy(tree_lists)

            temp_list_copy = copy.deepcopy(temp_list)

            jumps = []

            next_item = items[i][0]
            diff = index - i

            for j in range(len(tree_lists.lists)):
                ptr = tree_lists.lists[j]
                if ptr == None:
                    jumps.append(None)
                    continue
                else:
                    jumps.append(ptr)
                    for k in range(diff):
                        ptr = ptr.parent
                        if ptr.value == next_item or ptr.value == None:
                            break

                    if ptr.value != next_item:
                        tree_lists.lists[j] = None
                    else:
                        tree_lists.lists[j] = ptr          # prepare tree for next item appended

            process(tree_lists,items,i,frequent_sets,temp_list_copy,len_trans,min_sup,HTs)

            for i in range(len(tree_lists.lists)):
                tree_lists.lists[i] = jumps[i]

            for i in range(len(tree_lists.lists)):
                if tree_lists.lists[i] == None:
                    continue
                else:
                    curr_node = tree_lists.lists[i]
                    for j in range(len(path_count_list[i])):
                        curr_node.count = path_count_list[i][j]
                        curr_node = curr_node.parent


            for x in tree_lists.tree.total_count:
                tree_lists.tree.total_count[x] = total_count_copy[x]

        return


def get_frequent_sets(tree_lists,frequent_sets,item_list_sorted,len_trans,min_sup,HTs):

    """
    calls the method process 'n' number of times where 'n' is the
    number of items present in the list item_list_sorted. The method is
    called for the item with minimum frequency first and so on until
    the item with maximum frequency.

    """

    for i in range(len(item_list_sorted)-1,-1,-1):

        temp_list = []

        tree_lists_copy = copy.deepcopy(tree_lists)
        process(tree_lists_copy,item_list_sorted,i,frequent_sets,temp_list,len_trans,min_sup,HTs)


def fPGrowthAlgo(filename, min_sup = 0.02):

    """
    It accepts the file of transactions and the value of minimum support and
    returns a list of frequent sets obtained from the FPtree.

    """

    transactions = Preprocess.get_transactions(filename)
    items_dict = Preprocess.get_items_dict(transactions)
    item_list_sorted = sort_items_by_support(transactions,items_dict)
    transactions = update_transactions(transactions,items_dict,item_list_sorted)

    tree = FPTree()
    tree.construct_tree(transactions)

    tree_lists = FPLists(tree)
    tree_lists.create_lists()
    HTs = createHTs(filename)
    frequent_sets = []
    get_frequent_sets(tree_lists,frequent_sets,item_list_sorted,len(transactions),min_sup,HTs)

    for freq_set in frequent_sets:
        freq_set.sort()

    frequent_sets.sort(key = len)

    return frequent_sets,list(items_dict.keys())
