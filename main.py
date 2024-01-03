from fastapi import FastAPI
import pandas as pd
from fastapi import FastAPI, File

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.post('/upload/doq')
def process_data(sheet: bytes = File(...)):
    try:
        api_url = "https://services.smartjoules.org/m2/driver/v2/devices"  # Replace with the actual API endpoint URL
        # Authentication (if required)
        headers = {
            "Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6Im5hbWFua3VtYXJAc21hcnRqb3VsZXMuaW4iLCJfcm9sZSI6ImFkbWluIiwibmFtZSI6Ik5hbWFuIEt1bWFyIiwiX3NpdGUiOiJzam8tZGVsIiwidW5pdFByZWYiOnsidGVtcGVyYXR1cmUiOiJkZWdDIiwiZGVsVGVtcGVyYXR1cmUiOiJkZWxDIiwicHJlc3N1cmUiOiJwc2kiLCJsZW5ndGgiOiJtIiwiY29ucyI6Imt2YWgiLCJmbG93IjoiZ2FsbG9uIC8gbWluIn0sIl9oXyI6InNqby1kZWxfMzZkNGY3MTJhYTM4MzFkZDVkN2U1MDc3ZTUzZjlkNmQiLCJpYXQiOjE3MDQzMTM1NjQsImV4cCI6MTcwNDQ4NjM2NH0.lMGAPvzPjVoeufkrVKEhALwvV22wusr6aTiCq8kzuPY"  # Replace with your API token or other credentials
        }


    
        # sheet = requests.get(api_url, headers=headers)
        if not sheet:
            print("Sheet not exist:", sheet.text)
        else:
            save_binary_data_to_file(sheet, 'output.xlsx')



        # print('This is response')
        # print(response)
        # return json.dumps(response)

        # Load the Excel file into a DataFrame
        file_path_new = 'dummycopy2.xlsx'
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
        print(f"An error occurred: {e}")
        return {"message": "Something went wrong during processing","error": e}  # Return error message
    
def save_binary_data_to_file(response, file_path):
    """
    Saves binary data from a response to a file.

    Args:
        response: The response object containing binary data.
        file_path: The path to the file where the data will be saved.
    """

    with open(file_path, 'wb') as f:  # Open file in binary write mode
        f.write(response.content)  # Write binary content to file