import numpy as np
import pandas as pd

def main():
    trainlabels = read_data("trainlabels.txt")
    traindata = read_data("traindata.txt")
    testlabels = read_data("testlabels.txt")
    testdata = read_data("testdata.txt")
    stoplist = read_data("stoplist.txt")
    vocab = vocabulary(traindata, stoplist)
    trainfeature = features(traindata, vocab)
    testfeature = features(testdata, vocab)
    weight, accuracy, sumi = classifier(trainfeature, trainlabels, 20)
    print("Training Accuracy: ", accuracy)


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
    ans = {}
    correctSum = 0
    print(features[0][0])
    for i in range(iterations):

        correct = 0
        incorrect = 0
        sumi = predictWeights(w, features[i]) + correctSum
        if int(trainlabels[i]) == 1:
            correct = 1
        else:
            correct = -1

        for j in range(len(features)):
            if  correct * sumi <= 0:
                w = updateWeights(w, features[j], correct)
                incorrect += 1
                sumi += correct
            else:
                correct += 1
        ans[i] = {"Correct" : correct, "Incorrect" : incorrect, "Accuracy" : correct/(correct+incorrect)}
    return w, ans, sumi


def predictWeights(weight, feature):
    vsum = 0
    n = len(feature)
    for i in range(n):
        vsum+=feature[i]*weight[i]
    return vsum

def updateWeights(weight, feature, correct):
    n = len(feature)
    for i in range(n):
        weight[i] += correct * feature[i]
    return weight

if __name__ == '__main__':
    main()