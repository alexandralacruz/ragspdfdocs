import pdfplumber
import os
import pandas as pd
import tkinter as tk
from tkinter import filedialog, messagebox
import tabula
from docx import Document
import csv
import os
import matplotlib.pyplot as plt
import seaborn as sns

def clean_percentage(value):
    #print(f"value {value}")
    if isinstance(value, str):
        value = value.replace('%', '')  # Remove '%' symbol if it exists
        value = value.replace(',', '.')  # Remove '%' symbol if it exists
    try:
        #print(f"value {value}")
        return float(value)  # Convert the value to float
    except ValueError:
        #print(f"value except {value}")
        return None  # Return None for values that cannot be converted
    


def plot_performance_RAEC(df, filename, lineplot = False, barplot = True):
    for col in df.columns[3:]:
        #print(f"col {col}")
        df[col] = df[col].apply(clean_percentage)

    
    # Reshaping the DataFrame to long format
    df_long = df.melt(id_vars=['Categorías de notas', 'Desempeño'], 
                    value_vars=df.columns[3:],
                    var_name='RAEC', value_name='Porcentaje de estudiantes')

    # Clean up the 'RAEC' column to get the corresponding RAEC values
    df_long['RAEC'] = df_long['RAEC'].str.replace('Porcentaje de estudiantes-', '')

    # Plot
    plt.figure(figsize=(10, 6))
    if (barplot) or (not barplot and not lineplot):
        sns.barplot(data=df_long, x='Desempeño', y='Porcentaje de estudiantes', hue='RAEC')
    # Overlaying a line plot (you can change the style and markers for the line)
    if lineplot:
        sns.lineplot(data=df_long, x='Desempeño', y='Porcentaje de estudiantes', hue='RAEC', 
             markers='o', dashes=True, linewidth=2, markersize=8)
    # sns.lineplot(data=df_long, x='Desempeño', y='Porcentaje de estudiantes', hue='RAEC', 
    #          style='RAEC', markers='o', dashes=False, linewidth=2, markersize=8)
    # Labels and title
    plt.title(f'Porcentaje de Estudiantes por Desempeño y RAEC {filename}')
    plt.xlabel('Desempeño')
    plt.ylabel('Porcentaje de Estudiantes')
    plt.xticks(rotation=45)
    plt.tight_layout()

    plt.show()

def plot_all(folder_path, lineplot = False, barplot = True):
    csv_files = [file for file in os.listdir(folder_path) if file.endswith('.csv')]
    for csv_file in csv_files:
        file_path = os.path.join(folder_path, csv_file)
        #print(f"\nReading: {csv_file}")
        df = pd.read_csv(file_path)
        plot_performance_RAEC(df,csv_file, lineplot, barplot)


def read_and_show_csvs(folder_path):
    # Get a list of all CSV files in the folder
    csv_files = [file for file in os.listdir(folder_path) if file.endswith('.csv')]
    
    # Loop through each file, read and display the DataFrame
    for csv_file in csv_files:
        file_path = os.path.join(folder_path, csv_file)
        #print(f"\nReading: {csv_file}")
        df = pd.read_csv(file_path)
        #print(df.head())  # Show the first few rows of the DataFrame

        # Check if the first row has NaN values in the first two columns
        if pd.isna(df.iloc[0, 0]) and pd.isna(df.iloc[0, 1]):
            # Identify the columns after the second one as subcategories
            # sub_columns = df.columns[2:]
            # row_0_non_null_values = df.iloc[0].dropna().tolist()
            # df.drop(index=0, inplace=True)
            # #print(f'sub_columns {sub_columns}')
            # for i, sub_col in enumerate(sub_columns, start=1):
            #     #print(f"Processing sub-column: {sub_col} and {df.iloc[0, 1+i]}")  # Debugging line to see sub-column names
            #     sub_title = df.iloc[0, 1+i].replace("\n", " ")
            #     #print(f"Processing sub-title: {sub_title}") 
            #     new_col_name = f"Porcentaje de estudiantes-{str(sub_title)}"
            #     df.rename(columns={sub_col: new_col_name}, inplace=True)
            row_0_non_null_values = [str(val).replace("\n", "") for val in df.iloc[0].dropna().tolist()]
            #print(row_0_non_null_values)
            df.drop(index=0, inplace=True)
            df = df.dropna(axis=1, how='all')
            sub_columns = df.columns[2:]
            #print(f"sub_columns: {sub_columns}")
            for i, sub_col in enumerate(sub_columns, start=1):
                sub_title = row_0_non_null_values[i-1]
                new_col_name = f"Porcentaje de estudiantes-{str(sub_title)}"
                df.rename(columns={sub_col: new_col_name}, inplace=True)
        #df.drop(index=0, inplace=True)
        #df.reset_index(drop=True, inplace=True)  # Reset the index after dropping
        if 'Unnamed: 0' in df.columns:
            df = df.drop(columns=['Unnamed: 0'], inplace=True)
        df.to_csv(file_path)
        print(f"new columns {df.columns} in {file_path}")

# def read_and_show_csvs(folder_path):
#     # Get a list of all CSV files in the folder
#     csv_files = [file for file in os.listdir(folder_path) if file.endswith('.csv')]
    
#     # Loop through each file, read and display the DataFrame
#     for csv_file in csv_files:
#         file_path = os.path.join(folder_path, csv_file)
#         print(f"\nReading: {csv_file}")
#         df = pd.read_csv(file_path)
#         print(df.head())  # Show the first few rows of the DataFrame

#         # Check if the first row has NaN values in the first two columns
#         if pd.isna(df.iloc[0, 0]) and pd.isna(df.iloc[0, 1]):
#             # Identify the columns after the second one as subcategories
#             sub_columns = df.columns[3:]
#             for i, sub_col in enumerate(sub_columns, start=1):
#                 print(f"Processing sub-column: '{sub_col}'")  # Debugging line to see sub-column names
#                 if pd.isna(sub_col):
#                     print(f"Warning: Found NaN in column {i}, skipping.")  # Handle NaN or unexpected values
                
#                 else:
#                     # Clean and rename the sub-column
#                     if isinstance(sub_col, str):
#                         new_col_name = f'Porcentaje de estudiantes-{sub_col.replace("", "").replace("\n", "")}'
#                     else:
#                         print(f"Warning: Invalid sub_column value: {sub_col}")
#                         new_col_name = f"Porcentaje de estudiantes-{str(sub_col)}"  # Convert to string if invalid
#                     #new_col_name = f"Porcentaje de estudiantes-{sub_col.replace(' ', '').replace('\n', '')}"
                                        
#                     #new_col_name = f"Porcentaje de estudiantes-{sub_col.replace(' ', '').replace('\n', '')}"
#                     df.rename(columns={sub_col: new_col_name}, inplace=True)
#         df.drop(index=0, inplace=True)
#         df.reset_index(drop=True, inplace=True)  # Reset the index after dropping
#         # Display the updated DataFrame (first few rows)
#         print(df.head())  # Show the first few rows of the DataFrame
#         break
#         #input("\nPress Enter to continue to the next file...")

def extract_pdf_tables_old(filepath, output_folder):
    try:
        filename = get_filename_without_extension(filepath)
        print(filename)
        tables = tabula.read_pdf(filepath, pages='all', multiple_tables=True)
        for i, table in enumerate(tables):
            table.to_csv(os.path.join(output_folder, f'{filename}_{i}.csv'), index=False)
            #except UnicodeEncodeError as encode_err:
            #    print(f"Unicode encoding error: {encode_err}, trying again with 'utf-8'")
            #    table.to_csv(os.path.join(output_folder, f'{filename}_{i}.csv'), index=False, encoding='utf-8', errors='replace')  # Use 'replace' to avoid crashing
    except Exception as err:
        print(f"Unexpected {err=}, {type(err)=}")
        raise

def extract_pdf_tables(filepath, output_folder):
    #print(f"In extract pdf tables thi is the filepath: {filepath}")
    filename = filepath.split("\\")[-1]
    expected_columns = ['Categorías de notas', 'Desempeño','Porcentaje de Estudiantes']
    #print(f"In extract pdf tables thi is the filename: {filename}")
    #return
    try:
        with pdfplumber.open(filepath) as pdf:
            for i, page in enumerate(pdf.pages):
                print(f"Processing page {i+1}")
                tables = page.extract_tables()
                
                # Loop through each table and convert to DataFrame
                for j, table in enumerate(tables):
                    df = pd.DataFrame(table[1:], columns=table[0])  # Using first row as column names
                    #df.to_csv(f"{output_folder}/page_{i+1}_table_{j+1}.csv", index=False)
                    if any(column in df.columns for column in expected_columns):
                        print("The table is the correct one. Proceeding to save it.")
                        # You can save the DataFrame here
                        df.columns = df.columns.str.replace('\n', ' ')
                        df.to_csv(f"{output_folder}/{filename}_{j}.csv", index=False)
                    else:
                        print("The table is not the correct one. Skipping save.")
                    
    except Exception as err:
        print(f"Unexpected error: {err}")               

def extract_docx_tables(filepath, output_folder):
    try:
        doc = Document(filepath)
        filename = get_filename_without_extension(filepath)
        for i, table in enumerate(doc.tables):
            with open(os.path.join(output_folder, f'{filename}_{i}.csv'), 'w', newline='') as f:
                writer = csv.writer(f)
                for row in table.rows:
                    writer.writerow([cell.text for cell in row.cells])
    except Exception as err:
        print(f"Unexpected {err=}, {type(err)=}")
        raise

def get_filename_without_extension(file_path):
    # Obtiene el nombre del archivo con la extensión
    file_name_with_extension = os.path.basename(file_path)
    # Separa el nombre del archivo de su extensión
    file_name, _ = os.path.splitext(file_name_with_extension)
    return file_name

def process_files(input_folder, output_folder):
    for filename in os.listdir(input_folder):
        print(f'processing {filename}')
        filepath = os.path.join(input_folder, filename) 
        if os.path.isfile(filepath) and (filename.lower().endswith('.pdf') or filename.lower().endswith('.docx')):
            print(f"{filename} is a valid file.")
            try:
                print(f'processing {filepath}')
                if filename.lower().endswith('.pdf'):
                    extract_pdf_tables(filepath, output_folder)
                    #break
                elif filename.lower().endswith('.docx'):
                    extract_docx_tables(filepath, output_folder)
            except Exception as e:
                print(f"Error processing {filename}: {e}")

def process_files_old(input_folder, output_folder):
    for filename in os.listdir(input_folder):
        print(f'processing {filename}')
        if (os.path.isfile(filename)):
            print("it is a file")
        if (filename.lower().endswith('.pdf')):
            print("it is a pdf")
            
        if (filename.lower().endswith('.pdf') or filename.lower().endswith('.docx')):

            filepath = os.path.join(input_folder, filename)
            try:
                print(f'processing {filepath}')
                if filename.lower().endswith('.pdf'):
                    extract_pdf_tables(filepath, output_folder)
                elif filename.lower().endswith('.docx'):
                    extract_docx_tables(filepath, output_folder)
            except Exception as e:
                print(f"Error processing {filename}: {e}")
        else:
            print("No entro")
        break


def extract_tables_from_pdf(pdf_path, output_folder):
    try:
        # Open the PDF with pdfplumber
        with pdfplumber.open(pdf_path) as pdf:
            for page_num, page in enumerate(pdf.pages):
                # Extract tables from each page
                tables = page.extract_tables()
                
                # If tables are found, convert each table to a CSV file
                for table_index, table in enumerate(tables):
                    # Convert table to DataFrame
                    df = pd.DataFrame(table[1:], columns=table[0])  # Skip first row as it contains headers
                    
                    # Create a CSV filename (based on PDF filename and page number)
                    base_filename = os.path.splitext(os.path.basename(pdf_path))[0]
                    csv_filename = f"{base_filename}_page{page_num+1}_table{table_index+1}.csv"
                    csv_path = os.path.join(output_folder, csv_filename)
                    
                    # Save the DataFrame as CSV
                    df.to_csv(csv_path, index=False)
                    print(f"Table {table_index+1} from page {page_num+1} saved as {csv_filename}")

    except Exception as e:
        print(f"Error extracting tables from {pdf_path}: {e}")


