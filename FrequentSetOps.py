"""
FrequentSetOps.py
==========================
This file contains all the functions required to calculate maximal frequent sets, closed frequent sets
and association rules from the list of frequent itemsets and hashtrees.
"""
from HashTree import HTree, HTNode
import itertools

def getMaxFreqSets(freq_sets):
    """
    This function generates a list of Maximal frequent sets given a list of frequent itemsets.
    """
    max_freq_sets = []

    for freq_set in freq_sets:
        is_maximal = True
        for other_set in freq_sets:
            if all(x in other_set for x in freq_set) and len(other_set) == len(freq_set) + 1:
                is_maximal = False
                break
        if is_maximal :
            max_freq_sets.append(freq_set)

    return max_freq_sets


def getClosedFreqSets(freq_sets, HTs):
    """
    This function generates a list of Closed frequent sets given a list of frequent itemsets.
    """
    closed_freq_sets = []

    for freq_set in freq_sets:
        is_closed = True
        for other_set in freq_sets:
            if all(x in other_set for x in freq_set) and len(freq_set) == len(other_set) - 1 and HTs[len(freq_set)-1].getSupportCount(freq_set) == HTs[len(other_set)-1].getSupportCount(other_set):
                is_closed = False
                break
        if is_closed :
            closed_freq_sets.append(freq_set)

    return closed_freq_sets


def subsets(s):
    """
    This function generates a list of all subsets of a given set s.
    """
    all_subsets = []
    for cardinality in range(len(s) + 1):
        all_subsets += (itertools.combinations(s, cardinality))

    return all_subsets


def findRules(freq_sets,HTs,confidence):
    """
    This function generates a list of association rules given a list of frequent itemsets, hashtrees and a minimum confidence value.
    """
    rules = []

    for curr_set in freq_sets:
        sub_sets = [list(sub_set) for sub_set in subsets(curr_set)]

        for sub_set1 in sub_sets:
            for sub_set2 in sub_sets:
                if set(sub_set1).intersection(set(sub_set2)):
                    continue
                sub_set1.sort()
                sub_set2.sort()
                if HTs[len(sub_set1)-1].getSupportCount(sub_set1) != 0 and HTs[len(sub_set2)-1].getSupportCount(sub_set2) != 0:
                    union_set = list(set(sub_set1)|set(sub_set2))
                    union_set.sort()
                    if HTs[len(union_set)-1].getSupportCount(union_set)/HTs[len(sub_set1)-1].getSupportCount(sub_set1) > confidence:
                        rules.append(tuple((sub_set1,sub_set2,HTs[len(union_set)-1].getSupportCount(union_set)/HTs[len(sub_set1)-1].getSupportCount(sub_set1))))

    return rules
