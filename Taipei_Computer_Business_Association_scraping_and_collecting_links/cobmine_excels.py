import pandas as pd
import os

def combine_excel_files(folder_path):
    # List all files in the directory
    all_files = [f for f in os.listdir(folder_path) if f.endswith('.xlsx')]
    
    # Initialize an empty list to store DataFrames
    dataframes = []
    
    # Loop through all files and read them into DataFrames
    for file in all_files:
        file_path = os.path.join(folder_path, file)
        df = pd.read_excel(file_path, engine='openpyxl')
        # Add a column to identify the source file
        df['Source File'] = file
        dataframes.append(df)
    
    # Combine all DataFrames into a single DataFrame
    combined_df = pd.concat(dataframes, ignore_index=True)
    
    return combined_df

# Path to the folder containing the Excel files
folder_path = r'台北市電腦商業同業公會'  # Replace with your folder path

# Combine Excel files and save to a new Excel file
combined_df = combine_excel_files(folder_path)
combined_df.to_excel('combined_excel_files.xlsx', index=False)

print("Data has been combined and saved to 'combined_excel_files.xlsx'.")
