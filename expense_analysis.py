import pandas as pd 

#loading the data
filepath = 'Annual_Budget.csv'
pd.options.display.max_rows = 9999 #To Increase the maximum number of rows to display the entire DataFrame
df = pd.read_csv(filepath) 
print(df)
#cleaning the data
print('\n')
#returns all columns except "Months" with a numeric value(removes currency & commas) 
df.loc[:, df.columns != 'Months'] = df.loc[:, df.columns != 'Months'].replace({r'[^\d.]': ''}, regex=True) #r'[^\d.]' regex: matches only digitd or period

# Converts cleaned columns to numeric values, invalid entries (including wrong data like 'x'(Letters)) will become NaN 
df.loc[:,df.columns != 'Months'] = df.loc[:,df.columns != 'Months'].apply(pd.to_numeric, errors='coerce') # Converts cleaned columns to numeric values, invalid entries (including wrong data like 'x'(Letters)) will become NaN 

#replace all empty cells(NaN) with value 0:
df.fillna(0,inplace=True) 
print('\n')
print(df)
