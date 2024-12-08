import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import streamlit as st
import plotly.express as px


# Tuple to store results: [(month_name, popular_category, category spending, total_spending)]
results = []

# Filepath to the dataset
filepath = 'Annual_Budget.csv'
pd.options.display.max_rows = 9999  # To Display the entire DataFrame

#Loading the data
try:
    df = pd.read_csv(filepath)
except FileNotFoundError:
    st.error(f"File: '{filepath}' could not be located.")
    st.stop()  # Exit if the file is not found
except pd.errors.ParserError:
    st.error(f"Filepath: '{filepath}' couldn't be parsed successfully.")
    st.stop()
except Exception as e:
    st.error(f"An unexpected error occurred while loading the file: {e}")
    st.stop()


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

    st.write('### Cleaned Data:')
    st.write(df)

except ValueError as e:
    st.error(f"Error while cleaning the data: {e}")
    st.stop()
except Exception as e:
    st.error(f"An unexpected error occurred while cleaning: {e}")
    st.stop()

#Calculate monthly total spending
monthly_columns = df.loc[:, df.columns != 'Category']  # Exclude the "Category" column

#Find the most popular category each month
categories = df["Category"]

# Iterate over monthly columns to determine the top category per month
for month in monthly_columns:
    max_spending_index = df[month].idxmax()  # Index of the maximum spending in the current month
    popular_category = categories[max_spending_index]  # Corresponding category name
    category_spending = df[month].iloc[max_spending_index]  # Spending in the most popular category for the current month
    total_spending = df[month].sum()  # Total spending in the current month

    # Append the result as a tuple (month, category, total_spending)
    results.append((month, popular_category, category_spending, total_spending))

# Convert the list of tuples into a DataFrame
results_df = pd.DataFrame(results, columns=["Month", "Popular Category", "Category Spending", "Total Spending"])

#Display the results

# Graph1 : Total Monthly Spending Overview
monthly_totals = df.sum(numeric_only=True)
fig1 = px.bar(
    x=monthly_totals.index,
    y=monthly_totals.values,
    title="Total Monthly Spending",
    labels={"x": "Month", "y": "Total Spending ($)"}
)
st.plotly_chart(fig1)

# order of the months 
month_order = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']

#custom color sequence 
color_sequence = px.colors.qualitative.Plotly


# Graph2 : Most Popular Cateogry Each Month
fig2 = px.bar(
    results_df,
    x="Month",
    y="Category Spending",
    color="Popular Category",
    title="Most Popular Category Spending Per Month",
    labels={"Category Spending": "Spending ($)"},
    category_orders={"Month": month_order},
    color_discrete_sequence = color_sequence #the custom color sequence
)
st.plotly_chart(fig2)