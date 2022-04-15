import numpy as np
import pandas as pd

def main():
    data = pd.read_csv('Groceries_dataset.csv')
    allProducts = data['itemDescription'].value_counts()
    print(allProducts)




if __name__ == "__main__":
    main()