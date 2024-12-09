import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st
import plotly.express as px
import numpy as np
from sklearn.linear_model import LinearRegression
import plotly.graph_objects as go
from prophet import Prophet


# Tuple to store results: [(month_name, popular_category, category spending, total_spending)]
results = []

#array to store months that have more spending than needed
alert_months = []

#predefined needs & wants
needs = {"Education", "Rent", "Groceries", "Utilities", "Gas/Car Wash"}
wants = {"Restaurants", "Shopping", "Clothes/Shoes", "Clothing", "Entertainment", "Subscriptions", "Hair/Beauty", "Flights/Hotels", "Vacation"}

# Welcome message and instructions
st.write("""
### Welcome to the Expense Analysis Dashboard!
To begin, please upload a file in **.csv** format. You can download our sample file below.  
**Important**:  
- Do not change the column names in the file.  
- You are free to change the row values and column attributes.  
""")

# File download section
SAMPLE_FILE_PATH = "sample_file.csv"
with open(SAMPLE_FILE_PATH, "rb") as file:
    sample_file_data = file.read()

TEST_FILE_PATH = "testfile.csv"
with open(TEST_FILE_PATH, "rb") as file:
    test_file_data = file.read()

st.write("#### Download the sample file or test file here:")

# Download button for samplefile.csv
st.download_button(
    label="Download Sample File",
    data=sample_file_data,
    file_name="sample_file.csv",
    mime="text/csv"
)

# Download button for testfile.csv
st.download_button(
    label="Download Test File",
    data=test_file_data,
    file_name="testfile.csv",
    mime="text/csv"
)

# File upload section
st.write("#### Upload Your File:")
uploaded_file = st.file_uploader(
    "Upload your expense file (CSV format):", 
    type=["csv"]
)

if uploaded_file:
    # Filepath to the dataset
    # filepath = 'Annual_Budget.csv'
    pd.options.display.max_rows = 9999  # To Display the entire DataFrame

    #Loading the data
    try:
        df = pd.read_csv(uploaded_file, encoding="ISO-8859-1")
    except FileNotFoundError:
        st.error(f"File: '{uploaded_file}' could not be located.")
        st.stop()  # Exit if the file is not found
    except pd.errors.ParserError:
        st.error(f"Filepath: '{uploaded_file}' couldn't be parsed successfully.")
        st.stop()
    except Exception as e:
        st.error(f"An unexpected error occurred while loading the file: {e}")
        st.stop()

    user_monthly_income = st.number_input("Please enter your approximate monthly income: ", min_value= 0)
    st.write("Your income(monthly): ", user_monthly_income)
    percentage_needs = st.number_input("What percentage of your monthly budget do you plan to allocate to needs (e.g., Rent, Utilities, Groceries, Education)?",min_value = 0, max_value=100)
    st.write("Your budget(monthly) Needs percentage: ", percentage_needs)
    percentage_wants = st.number_input("What percentage of your monthly budget do you plan to allocate to wants (e.g., Shopping, Dining, Entertainment)?",min_value = 0, max_value=100)
    st.write("Your budget(monthly) Wants percentage: ", percentage_wants)

    # Filter out columns where all values are zero
    df_filtered = df.loc[:, (df != 0).any(axis=0)]
    #Cleaning the data
    try:
    # Explicitly replace commas with an empty string
        df.loc[:, df.columns != 'Category'] = df.loc[:, df.columns != 'Category'].replace(r',', '', regex=True)

        # Remove currency symbols (e.g., $, £, ¥, ₹) and commas from the numeric columns
        df.loc[:, df.columns != 'Category'] = df.loc[:, df.columns != 'Category'].replace(r'[\$\£\¥\₹,]', '', regex=True)

        # Remove any remaining non-numeric characters except for periods
        df.loc[:, df.columns != 'Category'] = df.loc[:, df.columns != 'Category'].replace(r'[^\d.]', '', regex=True)

        # Convert cleaned columns to numeric values, replacing invalid entries with NaN
        df.loc[:, df.columns != 'Category'] = df.loc[:, df.columns != 'Category'].apply(pd.to_numeric, errors='coerce')

        # Replace NaN with 0 for consistency
        df.fillna(0, inplace=True)

        # Round numeric values to 2 decimal place
        df.loc[:, df.columns != 'Category'] = df.loc[:, df.columns != 'Category'].round(2)
        
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
        popular_category_spending = df[month].iloc[max_spending_index]  # Spending in the most popular category for the current month
        total_spending = df[month].sum()  # Total spending in the current month

        #Calculate which months, total spending is more than needed
        threshold = ((percentage_needs + percentage_wants) / 100) * user_monthly_income
        if(total_spending > threshold):
            alert_months.append(month)
        # Append the result as a tuple (month, category, total_spending)
        results.append((month, popular_category, popular_category_spending, total_spending))

    # Convert the list of tuples into a DataFrame
    results_df = pd.DataFrame(results, columns=["Month", "Popular Category", "Category Spending", "Total Spending"])

    top_categories = pd.DataFrame()

    # Extract top 3 categories for the year
    category_spending_per_category = df.groupby('Category').sum().sum(axis=1)  # This sums across all columns for each category
    sorted_data = category_spending_per_category.sort_values(ascending=False) #sorts in decending order(high-low category spending)
    top_categories = sorted_data.head(5)  # Append top 3 rows

    # Create a DataFrame for top categories
    top_categories_df = pd.DataFrame({
        "Category": top_categories.index,
        "Spending": top_categories.values
    })

                                                        #Display the results


    if(len(alert_months) == 0):
        st.markdown("<h3 style='color: green;'>Great work! You managed to stay under your budget the whole year.</h3>", unsafe_allow_html=True)
    else:
        st.markdown("<h3 style='color: red;'>You exceeded your spending expectation these months:  </h3>", unsafe_allow_html=True)
        st.markdown(f"<h4 style='color: yellow;'> {','.join(alert_months)} </h4>", unsafe_allow_html=True)



    # Graph1 : Total Monthly Spending Overview
    st.markdown("""
    ### Total Monthly Spending Overview
    This chart provides an overview of the total spending for each month. The values are aggregated from the data, showing how spending has varied month by month. The x-axis represents each month, while the y-axis shows the total amount spent for that particular month.
    """)
    monthly_totals = df.sum(numeric_only=True)

    fig1 = px.bar(
        x=monthly_totals.index,
        y=monthly_totals.values,
        title="Total Monthly Spending",
        labels={"x": "Month", "y": "Total Spending"}
    )

    # Add a horizontal line at the threshold value
    fig1.add_hline(
        y=threshold,
        line_dash="dot",
        line_color="yellow",
        annotation_text="Goal",
        annotation_position="top right"
    )

    st.plotly_chart(fig1)

    fig1_line = px.line(
        x=monthly_totals.index,
        y=monthly_totals.values,
        title="Total Monthly Spending Trend",
        labels={"x": "Month", "y": "Total Spending"},
    )
    # Update the line color to red 
    fig1_line.update_traces(line=dict(color='red'))

    st.plotly_chart(fig1_line)

    # order of the months 
    month_order = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']

    #custom color sequence 
    color_sequence = px.colors.qualitative.Plotly

    # Graph2 : Most Popular Cateogry Each Month
    st.markdown("""
    ### Most Popular Category Per Month
    This chart shows the most popular category each month, with the corresponding spending amounts. The x-axis represents the months, and the y-axis shows the spending of the most popular category. Different colors indicate the most popular category for each month, and the color legend helps identify them.
    """)
    fig2 = px.bar(
        results_df,
        x="Month",
        y="Category Spending",
        color="Popular Category",
        title="Most Popular Category Per Month",
        labels={"Category Spending": "Spending"},
        category_orders={"Month": month_order},
        color_discrete_sequence = color_sequence #the custom color sequence
    )
    st.plotly_chart(fig2)

    #Graph3: Annual Category Spending
    st.markdown("""
    ### Annual Spending in Each Category
    This bar chart provides a breakdown of total spending of each category for the entire year. Each bar represents the total spending for a particular category, helping to visualize which categories have the highest spending. The color of each bar corresponds to its respective category.
    """)
    category_total = df.set_index("Category").sum(axis=1).reset_index() #sum across all rows(axis=1)
    category_total.columns = ["Category", "Total Spending"]

    fig3_horizontal = px.bar(
        category_total,
        x="Total Spending",
        y="Category",
        orientation='h',  # Horizontal bars
        color="Category",
        title="Annual Spending in Category",
        labels={"Total Spending": "Spending"},
        color_discrete_sequence=color_sequence  # the custom color sequence
    )
    st.plotly_chart(fig3_horizontal)



    #PieChart1: Top 5 Categories Annually 
    st.markdown("""
    ### Top 5 Categories Annually
    This pie chart displays the top 5 spending categories for the entire year. The slices represent the proportion of total spending allocated to each category. The color legend shows the respective category names, and hovering over the slices reveals the spending amounts for each category.
    """)
    fig4 = px.pie(
        top_categories_df,
        names="Category",  # The "Category" column will be used for the slices
        values="Spending",  # The "Spending" column will be used to size the slices
        title="Top 5 Categories Annually",
        color="Category",
        color_discrete_sequence=color_sequence,  
        hover_data=["Spending"],  # Hover data to include spending values
    )
    # Update the text on pie slices
    fig4.update_traces(textinfo="percent+label", insidetextorientation='radial')

    st.plotly_chart(fig4)

    #LineGraph2: Predict Spending for Future Months Based on Current Trends
    st.markdown("""
    ### Spending Analysis for Future Months
    This will analyze future months spending prediction based on current trends. Makes use of Linear Regression to help predict. 
    """)


        # Prepare data for linear regression
    month_numbers = np.array(range(len(monthly_totals))).reshape(-1, 1)  # Months as numeric values (0, 1, 2, ...)
    spending_values = monthly_totals.values.reshape(-1, 1)  # Total spending for each month

    # Apply Linear Regression
    model = LinearRegression()
    model.fit(month_numbers, spending_values)

    # Predict future months (next 12 months)
    future_months = np.array(range(len(monthly_totals), len(monthly_totals) + 12)).reshape(-1, 1)
    future_predictions = model.predict(future_months)

    # Ensure predicted values are >= 0
    future_predictions = np.maximum(future_predictions, 0)  # Replace any negative values with 0

    # Create a new DataFrame for plotting
    forecast_months = [*monthly_totals.index, *[f"Future Month {i+1}" for i in range(12)]]
    forecast_spending = np.concatenate([monthly_totals.values, future_predictions.flatten()])

    forecast_df = pd.DataFrame({
        "Month": forecast_months,
        "Spending": forecast_spending
    })

    # Plot the data
    fig = px.line(
        forecast_df,
        x="Month",
        y="Spending",
        title="Spending Analysis & Future Trends",
        labels={"Month": "Month", "Spending": "Total Spending"},
        markers=True
    )

    # Show the plot
    st.plotly_chart(fig)

    # Initialize an empty list to store the total spending on needs/wants for each month
    monthly_needs_spending_list = []
    monthly_wants_spending_list = []

    # Iterate through each month in the monthly columns
    for month in monthly_columns:
        # Initialize total spending for this month
        total_needs_spending = 0
        total_wants_spending = 0
        # Iterate through each category in the "needs" set (e.g., Education, Rent, Groceries, etc.)
        for need_category in needs:
            # Check if the current need category exists in the DataFrame
            if need_category in df['Category'].values:
                # Add the total spending for the current need category in this month to the total_needs_spending
                total_needs_spending += df.loc[df['Category'] == need_category, month].sum()
        
        # Append the total spending for the current month to the monthly_needs_spending_list
        monthly_needs_spending_list.append(total_needs_spending) #Now, monthly_needs_spending_list contains the total spending for each month on needs (Jan = index 0, Dec = index 11)

        for want_category in wants:
            if want_category in df['Category'].values:
                total_wants_spending += df.loc[df['Category'] == want_category, month].sum()

        monthly_wants_spending_list.append(total_wants_spending)


    #Stacked Bar Chart: Needs Vs Wants
    st.markdown("""
    ### Needs Vs Wants
    This will analyze your spending on Needs and Wants for each month and give you suggestions and alerts to save money! 
    """)

    # Create a stacked bar chart using Plotly
    fig = go.Figure()

    fig.add_trace(go.Bar(
        x=month_order,
        y=monthly_needs_spending_list,
        name='Needs',
        marker_color='yellow'
    ))

    fig.add_trace(go.Bar(
        x=month_order,
        y=monthly_wants_spending_list,
        name='Wants',
        marker_color='purple'
    ))

    # Update the layout for the chart
    fig.update_layout(
        title="Needs vs Wants Spending",
        xaxis_title="Month",
        yaxis_title="Spending ($)",
        barmode='stack',  # This makes the bars stacked
        xaxis=dict(tickmode='array', tickvals=month_order),  # Ensure months appear as labels
        legend_title="Category"
    )

    # Display the Plotly chart
    st.plotly_chart(fig)

    # st.write("Based on your inputs, ")
else:
    st.info("Please upload a file to proceed.")
