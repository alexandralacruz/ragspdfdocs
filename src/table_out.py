import pdfplumber
import os
import pandas as pd

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


