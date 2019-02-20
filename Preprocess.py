"""
Preprocess.py
===================
Contains methods required ofr certain pre-processing operations on given transaction dataset.
"""

import csv

def binarizeTransactions(file_name):
    """
    Converts the textual data of transactions into binary format after arranging the items in the transaction in lexicographical order and returns the binarized transaction data along with the list of items.
    """
    item_list = []
    with open(file_name) as file:
        reader = csv.reader(file,delimiter=',')
        for line in reader:
            for item in line:
                if item not in item_list:
                    item_list.append(item)

    item_list.sort()

    dataset = []

    with open(file_name) as file:
        reader = csv.reader(file,delimiter=',')

        for line in reader:
            temp = []
            for item in item_list:
                if item in line:
                    temp.append(1)
                else:
                    temp.append(0)

            dataset.append(temp)

    return dataset,item_list

def get_transactions(filename):
    """
    Returns the raw data of the transactions
    """
    transactions = []

    with open(filename) as file:

        data = csv.reader(file,delimiter = ',')
        for row in data:
            transactions.append(row)

    return transactions


def get_items_dict(transactions):
    """
    Returns a dictionary of all items along with it's binarized index.
    """
    all_items = []
    items = {}
    count = 0
    for transaction in transactions:
        for i in range(len(transaction)):
            all_items.append(transaction[i])

    all_items.sort()

    for item in all_items:
        if item not in items:
            items[item] = count
            count = count + 1

    return items
