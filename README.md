# PDF to CSV file converter.

This script allows the user to convert a PDF file into a CSV file.
It runs as a command line application, accepting the PDF file name
as a command line argument.

The script runs in Python 2.7 and requires the PyPDF2 library.

Example:

python pdftocsv.py Scrape.pdf

The name of the resulting file is Scrape_converted.csv

It is assumed that:

1) The PDF source file is in the same directory with this script,
2) Each page of the PDF document contains the table with N=6 columns,
2) The first row of the first page contains column titles,
3) Each row contains valid data.

In case of a diffenent number of columns, but the same document structure,
the value of N can be modified.
