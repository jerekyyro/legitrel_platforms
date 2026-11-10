# legitrel_platforms
Codes for retrieving and processing politcal platforms from fsd.pohtiva.tuni.fi.

## Code

**main.py** -- run other modules from here

**poht_read.py** -- reads single html pages from pohtiva and turns them into dataframe -- runnable by itself but also from main.py

**readerswriters.py** -- module including functions for reading comma separated files -> list of words and html pages -> string and much more

**cleaning.py** -- data cleaning module

**read_address_list.py** -- reads address list

## Folders and files for input and output (not included here):

### **./wordlists/** -- put wordlists and read them from here

**keywords.txt** -- includes keywords, line separated, to be used in the searches

**stopwords.txt** -- includes words, line separated, to be excluded from the searches

### **./datasources/** -- a folder for storing address lists etc.

**pohtiva_address_list.txt** -- file for a list of pohtiva url's

## **./poht_data/** -- a folder for saving the Pohtiva dataframe and the programmes in .txt and .html

**poht_data.xlsx** -- file for storing the dataframes -- remove this later

**mentions.xlsx** -- for storing sentences that mention keywords

**programmes.xlsx** -- for storing individual programmes -- condensed from sentences (stored poht_data.xlsx)

+ individual platforms stored as .txt and .html
