from tracemalloc import stop
import numpy as np
import pandas as pd
from pkg_resources import VersionConflict

def main():
    trainlabels = read_data("trainlabels.txt")
    traindata = read_data("traindata.txt")
    testlabels = read_data("testlabels.txt")
    testdata = read_data("testdata.txt")
    stoplist = read_data("stoplist.txt")
    vocab = vocabulary(traindata, stoplist)
    feature = features(traindata, vocab)
    print(feature)
    classifier(feature, trainlabels, 20)

def read_data(filename):
    with open(filename, "r") as text_file:
        data = text_file.read().splitlines()
    return data

def vocabulary(traindata, stoplist):
    vocab = sorted(list(set([word for line in traindata for word in line.split() if word not in stoplist])))
    return vocab

def features(data, vocab):
    feature = []

    lines = [line.split() for line in data]

    for line in lines:
        cur = []
        for word in vocab:
            if word in line:
                cur.append(1)
            else:
                cur.append(0)
        feature.append(cur)
    return feature

def classifier(features, trainlabels, iterations):

    w = [0]  * len(features[0])

    for i in range(iterations):
            correct = 0
            incorrect = 0

    pass

if __name__ == '__main__':
    main()