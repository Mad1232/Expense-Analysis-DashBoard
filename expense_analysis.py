import pandas as pd

# loading the data
filepath = 'Annual_Budget.csv'
pd.options.display.max_rows = 9999  # To increase the maximum number of rows to display the entire DataFrame

try:
    df = pd.read_csv(filepath)
    print(df)
except FileNotFoundError:
    print(f"File: '{filepath}' could not be located.")
except pd.errors.ParserError:
    print(f"Filepath: '{filepath}' couldn't be parsed successfully due to incorrect/inconsistent format.")
except Exception as e:
    print(f"An unexpected error occurred while loading the file: {e}")

# cleaning the data
try:
    # returns all columns except "Months" with a numeric value (removes currency & commas)
    df.loc[:, df.columns != 'Months'] = df.loc[:, df.columns != 'Months'].replace({r'[^\d.]': ''}, regex=True)

    # Converts cleaned columns to numeric values, invalid entries (including wrong data like 'x'(Letters)) will become NaN
    df.loc[:, df.columns != 'Months'] = df.loc[:, df.columns != 'Months'].apply(pd.to_numeric, errors='coerce')

    # replace all empty cells (NaN) with value 0:
    df.fillna(0, inplace=True)

    print('\n')
    print(f'The data has been successfully converted:\n{df}')
    
except ValueError as e:
    print(f"Error while cleaning the data: {e}")
except Exception as e:
    print(f"An unexpected error occurred while cleaning: {e}")
