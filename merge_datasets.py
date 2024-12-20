import pandas as pd
import glob
import os

csv_files = glob.glob("/Users/prakarsha/Desktop/Expense-Analysis-DashBoard/DataSets/*.csv")

mylist = [] #empty list
person_id = 0

for file in csv_files:
    df = pd.read_csv(file)

    person_id += 1
    df['PersonID'] = person_id #create a new column in the current dataframe to keep track of personID

    if "Unnamed: 2" in df.columns: #Drop column "Unnamed: 2"
        df = df.drop(columns=['Unnamed: 2'])

    mylist.append(df)

combined_df = pd.concat(mylist, ignore_index=True) #combined lists' dataframe

# Export the result to a new csv file
combined_df.to_csv( "combined_csv.csv", index=False, encoding='utf-8-sig')