import pandas as pd
from fastapi import FastAPI, Request, UploadFile
import openpyxl
import json

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.post('/project/validate-boq-sheet')
async def validateBOQSheet(file: UploadFile):
    try:
        # if file.content_type == 'application/json':
        #     return {'err': 'Invalid content type'}  
        sheet = file.file.read()  # Read raw bytes of the Excel file  
      
        if not sheet: 
            print("Sheet not exist") 
            # TODO:
        else:
            print('in sheet')
            save_binary_data_to_file(sheet, 'dummycopy2.xlsx')

        # Load the Excel file into a DataFrame
        file_path_new = 'dummycopy2.xlsx'
        file_path_new = sheet
        df_new = pd.read_excel(file_path_new)

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

        # # Displaying the results
        return missing_data_df.head()  # Displaying the first few rows of the result (if any)
        # return {"message": "Hello World"}
    except Exception as e:
        print("An error occurred:",e)
        return {"message": "Something went wrong during processing","error": e}  # Return error message
    
def save_binary_data_to_file(response, file_path):
    """
    Saves binary data from a response to a file.

    Args:
        response: The response object containing binary data.
        file_path: The path to the file where the data will be saved.
    """

    with open(file_path, 'wb') as f:  # Open file in binary write mode
        # f.write(response.content)  # Write binary content to file
        f.write(response)  #