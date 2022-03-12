from cmath import sqrt
import profile
import numpy as np
from itertools import combinations, count
from numpy import linalg
import pandas as pd
import time
from sklearn.neighbors import NearestNeighbors
from sqlalchemy import true


def main():

    #Getting centered cosine
    data = parser()
    table = createTable(data)
    centeredTable = centeredCosine(table)
    similarity = computeSimilarity(centeredTable)
    printToFile(similarity)

def parser():
    with open("ratings.csv", "r") as file:
        data = file.readlines()
    return data[1:]

def createTable(data):
    movie_ids = []
    user_ids = []
    ratingDict = {}
    for row in data:
        line = row.split(",")
        curUser = int (line[0])
        curMovie = int (line[1])
        user_ids.append(curUser)
        movie_ids.append(curMovie)
        curRating = float (line[2])
        ratingDict[curUser, curMovie] = curRating
        
    userSet = set(user_ids)
    movieSet = set(movie_ids)  

    userList = list(userSet)
    movieList = list(movieSet)

    rowCount = len(userSet)
    colCount = len(movieSet)

    table = [ [ 0.0 for i in range(colCount) ] for j in range(rowCount) ]

    for row in range(len(table)):
        for col in range(len(table[row])):
            curUserList = int (userList[row])
            curMovieList = int (movieList[col])
            if (userList[row], movieList[col]) in ratingDict.keys():
                table[row][col] = ratingDict[curUserList, curMovieList]
    
    return table



def centeredCosine(table):
    return np.apply_along_axis(rowMean, 1, table)

def rowMean(row):
    mean = row.mean()
    #mean = np.nanmean(row)
    return np.subtract(row, mean)

def computeSimilarity(table):

    similarity_scores = np.zeros((table.shape[1], table.shape[1]))

    combos = list(combinations([i for i in range(table.shape[1])], 2))

    counter = 0


    startTime = time.time()
    for pair in combos:
        print(counter)
        counter += 1
        vector_1 = table[:,pair[0]]
        vector_2 = table[:,pair[1]]

        similarity_scores[pair]  = np.dot(vector_1, vector_2)/(linalg.norm(vector_1)*linalg.norm(vector_2))
        
    print("---- %s seconds ----" % (time.time() - startTime))

    recommended = {}
    user = 0
    for row in similarity_scores:
        recommended[user] = tuple(sorted(row, reverse=True)[:5])
        user+=1

    return recommended




def printToFile(data):
     f = open("output.txt", "w")
     for key, value in data.items():
         f.write("User: %s, Movies: %s\n" % (key, value))


if __name__ == "__main__":
    main()