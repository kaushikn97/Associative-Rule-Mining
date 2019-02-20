"""
AssocRuleMining.py
=======================
This is the main python file which runs an Apriori algorithm as well as a FP-Growth algorithm on the given dataset.
It outputs a list of frequent itemsets, maximal itemsets, closed frequent itemsets and mines list of association rules.
"""
import Preprocess
import Apriori
import FPGrowth
import FrequentSetOps
import pickle
import os
import HashTree
import timeit
import argparse

data_folder = 'Data/'

def parseArguements():
    """
    This function gets the list of all arguments from the command line.
    It extracts the filename of the dataset, the algorithm to be used to generate frequent sets, the minimum support and
    confidence values to be used for mining the association rules.
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("filename",help="name of dataset file in Data folder")
    parser.add_argument("algo",help="use \'ap\' for Apriori and \'fp\' for FPGrowth",choices=['ap','fp'])
    parser.add_argument("-p",help="use previously generated frequent sets",
                        action="store_true",default= False)
    parser.add_argument("min_sup",help="minimum support",type=float)
    parser.add_argument("confidence",help="confidence",type=float)

    args = parser.parse_args()

    return args.confidence, args.min_sup, args.filename, args.algo, args.p

def getPickledData(filename,min_sup,confidence):
    """
    This function retrieves the data, if it exists, stored to the pickle file.
    It gets the list of frequent itemsets, hashtrees and a list of items from the stored pickle files.
    """
    pickle_in = open(os.getcwd() + "/Pickles/freq_sets_" + filename + str(min_sup) + ".pickle","rb")
    freq_sets = pickle.load(pickle_in)

    pickle_in = open(os.getcwd() + "/Pickles/HTs_" + str(min_sup) + ".pickle","rb")
    HTs = pickle.load(pickle_in)

    pickle_in = open(os.getcwd() + "/Pickles/item_list_" + str(min_sup) + ".pickle","rb")
    item_list = pickle.load(pickle_in)

    return freq_sets, HTs, item_list

def pickleData(filename,min_sup,confidence,HTs,item_list,freq_sets):
    """
    This function writes data to a pickle file to be re-used later so as to decrease runtime and make the program efficient.
    It writes all the constructed hashtrees, list of frequent itemsets and list of items to their respective pickle files.
    """

    pickle_out = open(os.getcwd() + "/Pickles/HTs_" + filename + str(min_sup) + ".pickle","wb")
    pickle.dump(HTs, pickle_out)
    pickle_out.close()

    pickle_out = open(os.getcwd() + "/Pickles/freq_sets_" + filename + str(min_sup) + ".pickle","wb")
    pickle.dump(freq_sets,pickle_out)
    pickle_out.close()

    pickle_out = open(os.getcwd() + "/Pickles/item_list_" + filename + str(min_sup) + ".pickle","wb")
    pickle.dump(item_list,pickle_out)
    pickle_out.close()

if __name__ == '__main__':


    confidence, min_sup, filename, algo, use_pickled = parseArguements()

    if use_pickled:

        try:

            freq_sets,HTs,item_list = getPickledData(filename,min_sup,confidence)

        except (OSError, IOError) as e:
            use_pickled = False

    if not use_pickled:

        if algo is 'ap':

            freq_sets,item_list = Apriori.aprioriAlgo(data_folder + filename,min_sup)

        else:

            freq_sets,item_list = FPGrowth.fPGrowthAlgo(data_folder + filename,min_sup)

        HTs = HashTree.generateHTs(data_folder+filename, freq_sets, min_sup)

    max_freq_sets = FrequentSetOps.getMaxFreqSets(freq_sets)

    closed_freq_sets = FrequentSetOps.getClosedFreqSets(freq_sets,HTs)

    print(len(max_freq_sets))
    print(len(closed_freq_sets))

    rules = FrequentSetOps.findRules(freq_sets,HTs,confidence)

    HashTree.documentFreqSets(HTs,item_list,min_sup,filename)

    HashTree.documentRules(HTs,item_list,rules,min_sup,confidence,filename)

    pickleData(filename,min_sup,confidence,HTs,item_list,freq_sets)
