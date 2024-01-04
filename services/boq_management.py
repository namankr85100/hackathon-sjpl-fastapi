import pandas as pd
from fastapi import FastAPI, Request, UploadFile, Form

def validate_boq_file(filePath, configuration):
    df_new = pd.read_excel(filePath)

    # # Define the relevant columns
    quantity_columns = ['Lower Basement', 'Upper Basement', 'GF', '1F', '2F', '3F', '4F', '5F', '6F', 'Terrace', 'Unit']
    check_columns = ['Supply Rate (INR)', 'Installation Rate (INR)', 'Supply Amount (INR)',
                    'Installation Amount (INR)', 'Total Amount (INR)']
    display_columns = ['S.No', 'Category', 'Item Code', 'Description of Item']

    # # Check for rows where quantity columns have values
    rows_with_quantity = df_new[quantity_columns].notnull().any(axis=1)

    # # Creating a smaller DataFrame with only the rows that have quantities
    df_with_quantities = df_new[rows_with_quantity]

    # # List to store the results
    results = []

    # # Iterating through the rows of the DataFrame with quantities
    for index, row in df_with_quantities.iterrows():
        # Check if any of the check_columns are missing in the current row
        if row[check_columns].isnull().any():
            # Extracting the display columns data
            display_data = row[display_columns].tolist()
            # Identifying the missing columns
            missing_cols = [col for col in check_columns if pd.isnull(row[col])]
            # Appending the result
            results.append(display_data + [missing_cols])

    # # Converting the results list to a DataFrame
    missing_data_df = pd.DataFrame(results, columns=display_columns + ['Missing Columns'])
    print (missing_data_df)
    print (missing_data_df.head())
    # # Displaying the results
    # return missing_data_df.head()  # Displaying the first few rows of the result (if any)
    return True