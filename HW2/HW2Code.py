import numpy as np
from itertools import combinations

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
    userHigh = 0
    movieHigh = 0

    for row in data:
        line = row.split(",")
        user = int(line[0])
        movie = int(line[1])

        if user > userHigh:
            userHigh = user
        if movie > movieHigh:
            movieHigh = movie
    table = np.zeros((userHigh, movieHigh), dtype=float)

    for row in data:
        line = row.split(",")
        user = int(line[0])
        movie = int(line[1])
        rating = float(line[2])

        table[user-1][movie-1] = rating
    return table

def centeredCosine(table):
    return np.apply_along_axis(rowMean, 1, table)

def rowMean(row):
    mean = row.mean()
    return np.subtract(row, mean)

def computeSimilarity(table):
    pass

if __name__ == "__main__":
    main()