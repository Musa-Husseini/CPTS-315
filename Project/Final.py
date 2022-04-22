import pandas as pd
import itertools as it
import time 

def main():
    start = time.time()
    support = 18
    df = pd.read_csv('Groceries_dataset.csv')
    itemOccurence = occurences(df, support)
    customerItems = preprocess(df, support)
    p1Data = pass1(itemOccurence, customerItems, support)
    print("Pass 1 took: ", time.time() - start)
    
    p2Data = pass2(itemOccurence, customerItems, p1Data,support)
    print("Pass 2 took: ", time.time() - start)

    p3Data = pass3(itemOccurence, customerItems, p2Data, support)
    print("Pass 3 took: ", time.time() - start)

    pairs = pairConfidence(itemOccurence, p1Data)
    triples = tripleConfidence(itemOccurence, p1Data, p2Data)
    quads = quadConfidence(itemOccurence, p1Data, p2Data, p3Data)
    print("end")
    


def occurences(df, support):
    data = {}

    count = df['itemDescription'].value_counts(ascending=False)
    for key, value in count.iteritems():
        if value > support:
            data[key] = value
    return data



def preprocess(df, support):
    data = {}
    finalData = {}
    grouped = df.groupby(['Member_number', 'itemDescription'])
    for name, group in grouped['Member_number']:
        key = name[0]
        value = name[1]
        # print(key)
        # print(value)
        if key in data.keys():
            data[key].append(value)
        else:
             data[key] = [value]
    for key, value in data.items():
        if len(value) > support:
            finalData[key] = value

    return finalData


def pass1(itemOccurence, customerItems, support):
    counter = {}
    finalCounter = {}
    combos = list(it.combinations(itemOccurence.keys(), 2))

    for key in combos:
        for value in customerItems.values():
            if key[0] in value and key[1] in value:
                if key not in counter.keys():
                    counter[key] = 1
                else:
                    counter[key] += 1
    for key, value in counter.items():
        if value > support:
            finalCounter[key] = value
    return finalCounter

def pass2(itemOccurence, customerItems, p1Data, support):
    counter = {}
    finalCounter = {}
    combos = list(it.combinations(itemOccurence.keys(), 3))

    for key in combos:
        a = key[0]
        b = key[1]
        c = key[2]

        if (a,b) not in p1Data.keys() or (a,c) not in p1Data.keys() or (b,c) not in p1Data.keys():
            continue
        else:
            for value in customerItems.values():
                if a in value and b in value and c in value:
                    if key not in counter.keys():
                        counter[key] = 1
                    else:
                        counter[key] += 1



    for key, value in counter.items():
        if value > support:
            finalCounter[key] = value
    return finalCounter


def pass3(itemOccurence, customerItems, p2Data, support):
    counter = {}
    finalCounter = {}
    combos = list(it.combinations(itemOccurence.keys(), 4))

    for key in combos:
        a = key[0]
        b = key[1]
        c = key[2]
        d = key[3]
        if (a,b,c) not in p2Data.keys() or (a,b,d) not in p2Data.keys() or (a,c,d) not in p2Data.keys() or (b,c,d) not in p2Data.keys():
            continue
        else:
            for value in customerItems.values():
                if a in value and b in value and c in value and d in value:
                    if key not in counter.keys():
                        counter[key] = 1
                    else:
                        counter[key] += 1



    for key, value in counter.items():
        if value > support:
            finalCounter[key] = value
    return finalCounter



    
def pairConfidence(p1, p2):
    confidence = {}
    for key in p2.keys():
        confidence[(key[0], key[1])] =  p2[key] / p1[key[0]]

        confidence[(key[1], key[0])] =  p2[key] / p1[key[1]]
    return dict(sorted(confidence.items(), key = lambda x:x[1],reverse=True))

def tripleConfidence(p1, p2, p3):
    confidence = {}
    for key in p3.keys():
        d = p2.get((key[0], key[2])) or p2.get((key[2], key[0]))
        confidence[(key[0],key[2],key[1])] = p3[key] / d

        d = p2.get((key[0], key[1])) or p2.get((key[1], key[0]))
        confidence[(key[0],key[1],key[2])] = p3[key] / d

        d = p2.get((key[1], key[2])) or p2.get((key[2], key[1]))
        confidence[(key[1],key[2],key[0])] = p3[key] / d


    return dict(sorted(confidence.items(), key = lambda x:x[1],reverse=True))

def quadConfidence(p1,p2, p3, p4):
    confidence = {}
    for key in p4.keys():
        d = p3.get((key[0], key[2], key[3])) or p3.get((key[2], key[0], key[3])) or p3.get((key[3], key[2], key[0]))
        confidence[(key[0],key[2],key[3],key[1])] = p4[key] / d

        d = p3.get((key[0], key[1], key[3])) or p3.get((key[1], key[0], key[3])) or p3.get((key[3], key[1], key[0]))
        confidence[(key[0],key[1],key[3],key[2])] = p4[key] / d

        d = p3.get((key[1], key[2], key[3])) or p3.get((key[2], key[1], key[3])) or p3.get((key[3], key[2], key[1]))
        confidence[(key[1],key[2],key[3],key[0])] = p4[key] / d

        d = p3.get((key[0], key[1], key[2])) or p3.get((key[1], key[0], key[2])) or p3.get((key[2], key[0], key[1]))
        confidence[(key[0],key[1],key[2],key[3])] = p4[key] / d

    return dict(sorted(confidence.items(), key = lambda x:x[1],reverse=True))

if __name__ == "__main__":
    main()