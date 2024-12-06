import os
import win32com.client
import shutil

# Function to convert .docx to .pdf
def convert_docx_to_pdf(docx_path, pdf_path):
    docx_path = os.path.abspath(docx_path)
    pdf_path = os.path.abspath(pdf_path)
    if not os.path.exists(docx_path):
        print(f"Error: The file {docx_path} does not exist.")
        return
    try:
        word = win32com.client.Dispatch('Word.Application')
        doc = word.Documents.Open(docx_path)
        doc.SaveAs(pdf_path, FileFormat=17)  # FileFormat 17 is for PDF
        doc.Close()
    except Exception as e:
        print(f"An error occurred while converting {docx_path}: {e}")

# Function to read a folder with .docx files and convert them to PDFs
# def convert_folder_of_docx_to_pdf(docx_folder, pdf_folder):
#     if not os.path.exists(pdf_folder):
#         os.makedirs(pdf_folder)
    
#     for filename in os.listdir(docx_folder):
#         if filename.endswith(".docx"):
#             docx_path = os.path.join(docx_folder, filename)
#             pdf_filename = filename.replace(".docx", ".pdf")
#             pdf_path = os.path.join(pdf_folder, pdf_filename)
            
#             #print(f"Converting {docx_path} to {pdf_path}...")
#             convert_docx_to_pdf(docx_path, pdf_path)
    
#     #print("All files converted.")



def convert_folder_of_docx_to_pdf(docx_folder, pdf_folder):
    # Ensure the PDF folder exists, if not create it
    if not os.path.exists(pdf_folder):
        os.makedirs(pdf_folder)
    
    # Loop through all files and subfolders in the docx_folder using os.walk
    for root, dirs, files in os.walk(docx_folder):
        for filename in files:
            file_path = os.path.join(root, filename)  # Get full path of the file
            
            # If it's a DOCX file, convert it to PDF
            if filename.endswith(".docx"):
                pdf_filename = filename.replace(".docx", ".pdf")
                pdf_path = os.path.join(pdf_folder, pdf_filename)  # Save PDF in the flat folder
                convert_docx_to_pdf(file_path, pdf_path)
            
            # If it's already a PDF, just copy it to the destination folder
            elif filename.endswith(".pdf"):
                pdf_path = os.path.join(pdf_folder, filename)  # Save PDF in the flat folder
                copy_pdf(file_path, pdf_path)


# Function to copy a PDF file to the destination folder
def copy_pdf(source, destination):
    try:
        # Check if file already exists and append "_number" if needed
        if os.path.exists(destination):
            base_name, ext = os.path.splitext(destination)
            counter = 1
            # Increment the number until we find a unique filename
            while os.path.exists(f"{base_name}_{counter}{ext}"):
                counter += 1
            # Update destination to the new unique filename
            destination = f"{base_name}_{counter}{ext}"

        print(f"Copying {source} to {destination}...")
        shutil.copy(source, destination)  # Copy the PDF file
        print(f"Copied {source} to {destination}")
    except Exception as e:
        print(f"Error copying {source} to {destination}: {e}")
