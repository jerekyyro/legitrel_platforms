'''Module for reading and writing to and from different sources '''

import urllib.request
import re
from bs4 import BeautifulSoup
import ssl

ssl._create_default_https_context = ssl._create_unverified_context

__author__ = "Jere Kyyrö"
__version__ = "0.1"

def readtxtcsv(fname):
    '''Reads text or csv containing words separated by lines and returns a list of words''' 
    f = open(fname,"r")
    contents = f.read()
    wordlist = contents.splitlines()
    return wordlist

def readlines(fname):
    '''Reads text containing lines (e. g. url's) separated by line break and returns a list of lines''' 
    f = open(fname,"r")
    contents = f.read()
    linelist = contents.splitlines()
    return linelist

def readhtml(address):
    '''Reads an online html page and returns a string'''
    fp = urllib.request.urlopen(address)
    mybytes = fp.read()
    mystr = mybytes.decode("utf8")
    fp.close()
    return [str(mystr), mybytes]

def readhtml_file(file_location):
    '''Reads an html file and returns a string'''
    myfile = open(file_location, encoding="utf-8").read()
    
    return myfile

def lineitersearch(inp_str, searched, endtrim):
    '''Gets a string and searchable string as input, if searchable is found, removes searchable and endtrim form the line and returns it'''
    lines = inp_str.splitlines()
    for i in range(len(lines)):
        if searched in lines[i]:
            line = lines[i]
            line = line.replace(searched, '')
            line = line.replace(endtrim, '')
            return line

def cleanhtml(html_txt):
    '''Gets string containing html tags and returns a string without html tags '''
    htag = re.compile('<.*?>')
    clean = re.sub(htag, '', html_txt)
    return clean

def cleanemptylines(txt):
    '''Gets string containing lines and returns a string without without 2 or more line breaks'''
    htag = re.compile('(\n){1,}')
    clean = re.sub(htag, '', txt)
    return clean

# encapsulate the shared part of save...'s
def savetxtfile(mybytes, partyname, progyear, progtype, progtitle, extension, path):
    '''Saves a programme as file, requires string to be saved, partyname, progyear, progtype, progtitle and extension (e. g. ".txt") as parameters, composes them into filename.'''
    savename = path+"/"+partyname+"_"+str(progyear)+"_"+progtype+"_"+extension
    #savename was left out to avoid bad filenames!
    text_file = open(savename, "w")
    # mystr = mystr.decode("utf-8")
    mystr = str(mybytes)
    try:
        n = text_file.write(mystr)
    except Exception as inst:
        n = text_file.write(("Exception while writing file. Exception information:"))
    text_file.close()
    return savename

def savelinklist(linklist, filename):
    '''Saves a list (of links) as a text file'''
    linkstring = ""
    for link in linklist:
        linkstring = linkstring + link + "\n"
    savename = filename
    text_file = open(savename, "w")
    n = text_file.write(linkstring)
    text_file.close()
    print("Saved "+savename)


def scraper(mainurl):
    '''scrapes all links from a given url '''
    mystr = readhtml(mainurl)
    parser = BeautifulSoup(str(mystr), 'html.parser')
    links = parser.find_all("a")
    linklist = []
    for link in links:
        linklist.append(link.get('href'))
    return linklist
    
