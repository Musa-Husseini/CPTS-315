import numpy as np
import pandas as pd

def main():
    trainlabels = read_data("trainlabels.txt")
    traindata = read_data("traindata.txt")
    testlabels = read_data("testlabels.txt")
    testdata = read_data("testdata.txt")
    stoplist = read_data("stoplist.txt")
    ocrtest = read_data("ocr_test.txt")
    ocrtrain = read_data("ocr_train.txt")



    vocab = vocabulary(traindata, stoplist)
    trainfeature = features(traindata, vocab)
    testfeature = features(testdata, vocab)
    weight, accuracy, bias = perceptronTrain(trainfeature, trainlabels, 20) 
    testResults = perceptronTest(weight, bias, testlabels, testfeature)

    printToFile(accuracy, testResults)

def read_data(filename):
    with open(filename, "r") as text_file:
        data = text_file.read().splitlines()
    return data

def vocabulary(traindata, stoplist):
    return sorted(list(set([word for line in traindata for word in line.split() if word not in stoplist])))

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

#follow algorithm 5 from textbook 
def perceptronTrain(features, trainlabels, iterations):

    weight = [0]  * len(features[0])
    ans = {}
    bias = 0

    for i in range(iterations):

        correct = 0
        incorrect = 0
        featureList = list(range(len(features)))

        for j in featureList:

            sumi = predictWeights(weight , features[j], bias) 

            if int(trainlabels[j]) == 1:
                correct = int(trainlabels[j])
            else:
                correct = -1


            
            if  correct * sumi <= 0:
                #print(weight)
                weight = updateWeights(weight, features[j], correct)
                #print(weight)
                incorrect += 1
                bias += correct
            else:
                correct += 1
        ans[i] = {"Correct" : correct, "Incorrect" : incorrect, "Accuracy" : correct/(correct+incorrect)}
    return weight, ans, bias
   


def predictWeights(weight, feature, bias):
    vsum = 0
    n = len(feature)
    for i in range(n):
        vsum+=feature[i]*weight[i]
    vsum += bias
    return vsum

def updateWeights(weight, feature, correct):
    weight2 =  [0] * len(weight)
    for i in range(len(weight)):
        weight2[i] = weight[i] + (correct * feature[i])
    return weight2


#follow algorithm 6 from textbook
def perceptronTest(weight, bias, trainlabels, traindata):
    traindatalist = list(range(len(traindata)))
    correct = 0
    incorrect = 0
    i = 0
    for row in traindatalist:
        prediction = predictWeights(weight, traindata[i], bias)


        if prediction <= 0:
            prediction = 0
        else:
            prediction = 1
        correct = int(trainlabels[row])

        if prediction == correct:
            correct += 1
        else:
            incorrect += 1
        i += 1
    ans =  {"Correct" : correct, "Incorrect" : incorrect, "Accuracy" : correct/(correct+incorrect)}
    return ans





def printToFile(train , test):

    f = open("output.txt", "w")
    for key, value in train.items():
        f.write(f"Iteration{key} {value['Incorrect']}\n")
    f.write("\n")

    for key, value in train.items():
        f.write(f"Iteration{key} {value['Accuracy']} {test['Accuracy']}\n")

    f.close()







if __name__ == '__main__':
    main()