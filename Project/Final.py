import numpy as np
import pandas as pd

def main():
    df = pd.read_csv('Groceries_dataset.csv')
    data = preprocess(df)



    
def preprocess(df):
    data = {}
    grouped = df.groupby(['Member_number', 'itemDescription'])
    print(grouped.first())
    for name, group in grouped['Member_number']:
        key = name[0]
        value = name[1]
        print(key)
        print(value)
        if key in data.keys():
            data[key].append(value)
        else:
             data[key] = [value]
    return data



    

if __name__ == "__main__":
    main()