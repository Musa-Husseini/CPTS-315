import numpy as np
from scipy.sparse import csr_matrix
from itertools import combinations
from numpy import linalg

def main():
    data = parser()
    table = createTable(data)
    centeredTable = centeredCosine(table)
    similarity = computeSimilarity(centeredTable)
    print(table)

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


def movieParser(data):
    movie_ids = []
    for row in data:
        line = row.split(",")
        movie_ids.append(line[1])

    return set(movie_ids)

def centeredCosine(table):
    return np.apply_along_axis(rowMean, 1, table)

def rowMean(row):
    mean = row.mean()
    return np.subtract(row, mean)

def computeSimilarity(table):

    similarity_scores = np.zeros((table.shape[1], table.shape[1]))

    # combos = list(combinations([i for i in range(table.shape[1])], 2))

    # for pair in combos:

    #     list1 = table[:,pair[0]]
    #     list2 = table[:,pair[1]]
    #     similarity_scores[pair] = list1.dot(list2)/ (np.linalg.norm(list1) * np.linalg.norm(list2))

    # return similarity_scores



    #similarity_scores = {}


    # testing for only the first 50 movies
    combos = combinations([i for i in range(50)], 2)


    for pair in combos:

        vector_1 = table[:,pair[0]]
        vector_2 = table[:,pair[1]]

        similarity_scores[pair] = np.dot(vector_1, vector_2)/(linalg.norm(vector_1)*linalg.norm(vector_2))
    
    return similarity_scores


if __name__ == "__main__":
    main()