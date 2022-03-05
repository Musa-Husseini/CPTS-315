import numpy as np
from scipy.sparse import csr_matrix
from itertools import combinations
from numpy import linalg

def main():
    data = parser()
    table = testTable(data)
    centeredTable = centeredCosine(table)
    similarity = computeSimilarity(centeredTable)
    print(table)

def parser():
    with open("ratings.csv", "r") as file:
        data = file.readlines()
    return data[1:]

def testTable(data):
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

def createTable(data):
    userHigh = 0
    movieHigh = 0


    # [id1, id2] : value


    ratingsDict = {} # [ [userId, movieId] : rating]
    movieDict = {} # [movieId : column] 
    userDict = {} # [userId : row]
    table = np.array([])
    curRow = 0
    curCol = 0

    for row in data:
        line = row.split(",")

        user = int(line[0])
        movie = int(line[1])
        rating = float(line[2])

        ratingsDict[user, movie] = rating
        if user not in userDict:   
            userDict[user] = curRow
            curRow += 1
        
        if movie not in movieDict:
            movieDict[movie] = curCol
            curCol+=1
    table = csr_matrix(curRow, curCol)





    # for row in data:
    #     line = row.split(",")
    #     user = int(line[0])
    #     movie = int(line[1])

    #     if user > userHigh:
    #         userHigh = user
    #     if movie > movieHigh:
    #         movieHigh = movie
    # table = np.zeros((userHigh, movieHigh), dtype=float)
    # movieSet = movieParser(data)


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



    # combos = combinations([i for i in range(table.shape[1])], 2)


    # for pair in combos:

    #     vector_1 = table[:,pair[0]]
    #     vector_2 = table[:,pair[1]]

    #     similarity_score[pair] = np.dot(vector_1, vector_2)/(linalg.norm(vector_1)*linalg.norm(vector_2))

    for i in range(table.shape[1]):
        for j in range(table.shape[1]):
            similarity_scores[i][j] = np.dot(table[:,i], table[:,j])/(linalg.norm(table[:,i])*linalg.norm(table[:,j]))



    return similarity_score

if __name__ == "__main__":
    main()