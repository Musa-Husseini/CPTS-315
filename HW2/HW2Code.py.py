import numpy as np
from itertools import combinations

def main():
    x = parser()
    print("hi")

def parser():
    with open("ratings.csv", "r") as file:
        data = file.readlines()
    return data[1:]


if __name__ == "__main__":
    main()