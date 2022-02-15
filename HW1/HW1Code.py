from ast import operator
from asyncio.windows_events import NULL
from contextlib import suppress
import enum
from itertools import count
from black import NewLine
import numpy as np
import pandas as pd
from sqlalchemy import true
import itertools as it

def main():
    f = open("50basketans.txt", "w")
    data = parser()
    support = 100
    p1Data = pass1(data, support)
    p2Data = pass2(data, p1Data, support)
    p3Data = pass3(data, p1Data, support)
    printToFile(p1Data,f)
    printToFile(p2Data,f)
    printToFile(p3Data,f)
    pairs = pairConfidence(p1Data, p2Data)
    triples = tripleConfidence(p1Data, p2Data, p3Data)
    printToFile(pairs, f)
    printToFile(triples, f)



    f.close()


def parser():
    data_file = "browsing-data.txt"

    data_file_delimiter = ','

    largest_column_count = 0

    with open(data_file, 'r') as temp_f:
        lines = temp_f.readlines()
        for l in lines:
            column_count = len(l.split(data_file_delimiter)) + 1
            
            largest_column_count = column_count if largest_column_count < column_count else largest_column_count

    column_names = [i for i in range(0, largest_column_count)]

    df = pd.read_csv(data_file, header=None, delimiter=data_file_delimiter, names=column_names)
    newLine = [lines[i].strip().split() for i in range(len(lines))]
    return newLine


def pass1(data, support):
    counter = {}
    finalCounter = {}
    for row in data:
        for i in row:
            if i not in counter:
                counter[i] = 1
            else:
                counter[i] +=  1
    
    for key, value in counter.items():
        if value >= support:
            finalCounter[key] = value
        
    return finalCounter

def pass2(data, p1data, support):
    counter = {}
    finalCounter = {}

    combo = list(it.combinations(p1data.keys(), 2))
    for c in combo:
        counter[c[0], c[1]] = 0


    for key in counter.keys():
        for row in data:
            if (key[0] in row) and (key[1] in row):
                counter[key] += 1

    for key, value in counter.items():
        if value >= support:
            finalCounter[key] = value


    return finalCounter

def pass3(data, p2data, support):
    counter = {}
    finalCounter = {}

    combo = list(it.combinations(p2data.keys(), 3))
    for c in combo:
        counter[c[0], c[1], c[2]] = 0

    for key in counter.keys():
        for row in data:
            if (key[0] in row) and (key[1] in row) and (key[2] in row):
                counter[key] += 1

    for key, value in counter.items():
        if value >= support:
            finalCounter[key] = value


    return finalCounter


def printToFile(data, f):

    for key, value in data.items():
        f.write("%s,%s\n"  % (key,value))
    f.write("\n")

def pairConfidence(p1, p2):
    confidence = {}
    for key in p2.keys():
        confidence[(key[0], key[1])] =  p2[key] / p1[key[0]]

        confidence[(key[1], key[0])] =  p2[key] / p1[key[1]]
    return dict(sorted(confidence.items(), key = lambda x:x[1],reverse=True)[:5])

def tripleConfidence(p1, p2, p3):
    confidence = {}
    for key in p3.keys():
        d = p2.get((key[0], key[2])) or p2.get((key[2], key[0]))
        confidence[(key[0],key[2],key[1])] = p3[key] / d

        d = p2.get((key[0], key[1])) or p2.get((key[1], key[0]))
        confidence[(key[0],key[1],key[2])] = p3[key] / d

        d = p2.get((key[1], key[2])) or p2.get((key[2], key[1]))
        confidence[(key[1],key[2],key[0])] = p3[key] / d
    return dict(sorted(confidence.items(), key = lambda x:x[1],reverse=True)[:5])



if __name__ == "__main__":
    main()