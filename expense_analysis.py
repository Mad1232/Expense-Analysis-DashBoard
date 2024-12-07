import pandas as pd 



#loading the data
filepath = 'Annual_Budget.csv'
pd.options.display.max_rows = 9999 #To Increase the maximum number of rows to display the entire DataFrame
df = pd.read_csv(filepath) 
print(df)





#cleaning the data
df.fillna(0,inplace=True) #replace all empty cells with value 0:
print('the information: \n')
print(df)

