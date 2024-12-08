import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt


# Tuple to store results: [(month_name, popular_category, category spending, total_spending)]
results = []

# Filepath to the dataset
filepath = 'Annual_Budget.csv'
pd.options.display.max_rows = 9999  # Display the entire DataFrame

#Loading the data
try:
    df = pd.read_csv(filepath)
    print(df)
except FileNotFoundError:
    print(f"File: '{filepath}' could not be located.")
    exit()  # Exit if the file is not found
except pd.errors.ParserError:
    print(f"Filepath: '{filepath}' couldn't be parsed successfully.")
    exit()
except Exception as e:
    print(f"An unexpected error occurred while loading the file: {e}")
    exit()


#Cleaning the data
try:
    # Remove non-numeric characters (except periods) from all columns except "Category"
    df.loc[:, df.columns != 'Category'] = df.loc[:, df.columns != 'Category'].replace({r'[^\d.]': ''}, regex=True)

    # Convert cleaned columns to numeric values, replacing invalid entries with NaN
    df.loc[:, df.columns != 'Category'] = df.loc[:, df.columns != 'Category'].apply(pd.to_numeric, errors='coerce')

    # Replace NaN with 0 for consistency
    df.fillna(0, inplace=True)

    # Round numeric values to 1 decimal place
    df.loc[:, df.columns != 'Category'] = df.loc[:, df.columns != 'Category'].round(1)

    print('\nCleaned data:\n', df)

except ValueError as e:
    print(f"Error while cleaning the data: {e}")
    exit()
except Exception as e:
    print(f"An unexpected error occurred while cleaning: {e}")
    exit()

print('\n\n\n')

#Calculate monthly total spending
monthly_columns = df.loc[:, df.columns != 'Category']  # Exclude the "Category" column

#Find the most popular category each month
categories = df["Category"]
print(categories)

# Iterate over monthly columns to determine the top category per month
for month in monthly_columns:
    max_spending_index = df[month].idxmax()  # Index of the maximum spending in the current month
    popular_category = categories[max_spending_index]  # Corresponding category name
    category_spending = df[month].iloc[max_spending_index]  # Spending in the most popular category for the current month
    total_spending = df[month].sum()  # Total spending in the current month

    # Append the result as a tuple (month, category, total_spending)
    results.append((month, popular_category, category_spending, total_spending))

#Display the results
print("\nMost Popular Category Each Month:")
for month, category, cat_spending, total in results:
    print(f"In {month}: {category}({cat_spending}) was the top category with total monthly spending of ${total:.1f}")
