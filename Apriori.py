"""
Apriori.py
===============
Contains the functions required to generate frequent itemsets by pruning and using the apriori algorithm.
"""
import itertools
from HashTree import *

def prune(dataset, curr_freq_sets, total_transactions,HTs,min_sup):
    """
    Function which takes all the candidates and counts support count of each itemset to remove the itemsets which do not cross
    the minimum support threshold. It returns all the itemsets whose support count is greater than minimum support.
    """
    curr_pruned = []
    for curr_set in curr_freq_sets:
        count = 0
        for transaction in dataset:
            temp = []
            count1 = 0
            for item in transaction:
                if item == 1:
                    temp.append(count1)

                count1 += 1

            if set(curr_set) <= set(temp):
                count += 1
        if count/total_transactions >= min_sup:
            curr_pruned.append(curr_set)

    return curr_pruned

def generateCandidates(prev_freq_sets):
    """
    Function which generates all the candidates of itemsets for next generation, i.e., if given a set of frequent itemsets each of length k,
    the function returns a list of all itemsets of size k+1 that can be generated from given set.
    """
    candidates = []
    for i in range(len(prev_freq_sets)-1):
        for j in range(i+1,len(prev_freq_sets)):
            count = 0
            for (item1,item2) in zip(prev_freq_sets[i],prev_freq_sets[j]):
                if item1 != item2:
                    count = prev_freq_sets[i].index(item1)
                    break

            if count == len(prev_freq_sets[i])-1:
                candidates.append(list(set(prev_freq_sets[i])|set(prev_freq_sets[j])))

    return candidates

def aprioriAlgo(filename, min_sup):
    """
    Function which implements the apriori algorithm by using candidate generation and pruning iteratively. It returns a list of frequent itemsets,
    given a set of transactions.
    """
    dataset,item_list = Preprocess.binarizeTransactions(filename)

    freq_sets = []

    k = 0
    total_items = len(dataset[0][:])
    total_transactions = len(dataset)
    curr_freq_sets = []

    HTs = createHTs(filename)

    for i in range(total_items):
        curr_freq_sets.append([i])
    curr_pruned = prune(dataset,curr_freq_sets,total_transactions,HTs,min_sup)

    for set in curr_pruned:
        freq_sets.append(set)

    while curr_pruned and k < findMaxItems(dataset)-1:

        k = k + 1

        curr_freq_sets = generateCandidates(curr_pruned)

        curr_pruned = prune(dataset,curr_freq_sets,total_transactions,HTs,min_sup)

        for set in curr_pruned:
            freq_sets.append(set)

    return freq_sets,item_list
