## Convert several RAES reports and generata an analyis of them

The structure is somethig like:

RAG PDF/
├── .venv
├── dataset/
├── pdfs/
├── sources/
├── src/
├── config.py
├── converter.py
├── donwload_file.py
├── table_out.py
.gitgitignore
RAGPdfs.ipynb
README.md
requirements.txt

## dataset/

## pdfs/ 
In this folder we leave all pdfs documents to process, already gotten from the proceess of convertion all documents in sources, where are the originals files submitted by professors

## sources/ 
In this folder we must leave all documents to process, they can be in pdf or docx format. The whole content of this folder would be converted to pdf and sabe it in pdfs folder

## src
src contains the whole source for read - convert - exrtact - transform - plot

## tables
Thif folder contains all the csv generated from extract each table where professor report the RAES per Competences applied and performance from students in group of level performance like:

Inaceptable
Necesita mejorar
Adecuado/aceptable
Bueno
Excelente


