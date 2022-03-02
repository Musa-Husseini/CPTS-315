from logging import root
from typing import Text
import numpy as np
import pandas as pd
import itertools as it

def main():
    f = open("output.txt", "w")
    data = parser()
    support = 100
    print("Started Pass1")
    
    #printToFile(test, f)
    p1Data = pass1(data, support)
    print("Finished Pass1")
    #print(test(data, p1Data, support))
    print("Started Prune")
    pruned = prune(p1Data, support)
    print("Finished Prunes")
    print("Started Pass2")
    p2Data = pass2(data, p1Data, support)
    print("Finished Pass2")
    print("Started Pass3")
    p3Data = pass3(data, p1Data, support)
    print("Finished Pass3")
    # printToFile(p1Data,f)
    # printToFile(p2Data,f)
    # printToFile(p3Data,f)
    pairs = pairConfidence(p1Data, p2Data)
    triples = tripleConfidence(p1Data, p2Data, p3Data)
    f.write("OUTPUT A:\n")
    printToFile(pairs, f)
    f.write("OUTPUT B:\n")
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

def prune(data, support):
    ans = {}
    for key, value in data.items():
        if value >= support:
            ans[key] = value
    return sorted(ans)

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
    combos = list(it.combinations(p1data.keys(), 2)) 

    for key in combos:
        counter[key] = 0

                
    for row in data:
        rcombo = list(it.combinations(row, 2))
        for key in rcombo:
            if (key in counter.keys()):
                counter[key] += 1
            elif (key[::-1] in counter.keys()):
                counter[key[::-1]] += 1



    for key, value in counter.items():
        if value >= support:
            finalCounter[key] = value


    return finalCounter
            

def pass3(data, p1data, support):
    counter = {}
    finalCounter = {}
    combos = list(it.combinations(p1data.keys(), 3)) 

    for key in combos:
        counter[key] = 0

                
    for row in data:
        rcombo = list(it.combinations(row, 3))
        for key in rcombo:
            a = key[0]
            b = key[1]
            c = key[2]
            keycombo = [(a,b,c), (a,c,b), (b,a,c), (b,c,a), (c,a,b), (c,b,a)]
            for kc in keycombo:
                if (kc in counter.keys()):
                    counter[kc] += 1



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