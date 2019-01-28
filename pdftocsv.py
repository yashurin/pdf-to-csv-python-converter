"""PDF to CSV file converter.

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
"""

import sys
import csv
import PyPDF2


# The number of columns we expect to find in a document. Can be changed if necessary.
N = 6

def pdf_to_csv(filename):
	"""
	The function to parse a PDF document and create a CSV document with the same data.

	Args:
		filename (string): The name of the pdf file.

	"""
	# The list to store text content of all pages.
	pages = []
	# Parse text content from each page, add to the list.
	pdf_reader = PyPDF2.PdfFileReader(filename)
	for i in range(pdf_reader.numPages):
		page_obj = pdf_reader.getPage(i)
		pages.append(page_obj.extractText())

	pages_list = []
	# Split text content by new line breaks, strip resulting strings of empty spaces.
	for page in pages:
		pages_list.append([elt.strip() for elt in page.split('\n')])

	titles = []
	data_chunks = []
	# Break a list with data for each page into chunks containing N elements.
	# The first N elements from the first page are assumed to be titles, to be stored separately.
	# The rest of the chunks are added to the data_chunks list.
	# Each chunk will represent a row in a resulting CSV file.
	for i, pg in enumerate(pages_list):
		chunks = [pg[x:x+N] for x in xrange(0, len(pg), N)]
		if i == 0:
			titles = chunks[0]
			data_chunks.extend(chunks[1:])
		else:
			data_chunks.extend(chunks)

	csv_filename = '{}_converted.csv'.format('.'.join(filename.split('.')[:-1]))

	with open(csv_filename, 'wb') as csvfile:
		# Use csv DictWriter to create field names and assign data for each field.
		# Write in binary mode to avoid extra lines.
		writer = csv.DictWriter(csvfile, fieldnames=titles)
		writer.writeheader()
		for row in data_chunks:
			# Write only rows of N elements, ignore incomplete chunks.
			if len(row) == 6:
				# UTF-8 encode text strings in a row to avoid errors.
				row = [s.encode('utf-8') for s in row]
				# Map title name to a record in a row, then write.
				record = dict(zip(titles, row))
				writer.writerow(record)
			else:
				continue


if __name__ == "__main__":
	pdf_to_csv(sys.argv[1])
