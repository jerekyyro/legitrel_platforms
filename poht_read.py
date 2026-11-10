'''Module for reading form Pohtiva database and saving the data'''
import pandas as pd
import readerswriters as rds
import re
import ast

__author__ = "Jere Kyyrö"
__version__ = "0.1"


def poht_read(fname: str):
    '''Reads a given html page from pohtiva, 
    saves sentences containing keywords in to a 
    dataframe and appends the dataframe to an existing datafile '''
    fname = fname

    # creates the dataframe
    sents = pd.DataFrame(columns={"pname", "year", "progtype", "progtitle", "sentence", "totalwrds",
      "wrds", "totalchars", "chars", "ment_kw", "keywords", "kw_hits", "stopwords", "sw_hits", "url", 
      "filename_html", "filename_txt"})

    columns = sents.columns.tolist()
    
    # reads the dummy dataframe from file
    old_sents = pd.read_excel("poht_data/poht_data.xlsx", index_col=0)

    # set up a list of keywords from a text file
    kwrds = rds.readtxtcsv("wordlists/keywords.txt")
    
    # set up a list of stop words (exluded from selection) from a text file
    stopwrds = rds.readtxtcsv("wordlists/stopwords.txt")
    
    # read the file

    mydata = rds.readhtml(fname)
    mystr = str(mydata[0])
    mybytes = mydata[1]

    #metadata in following format:
    # <div class="large-12 columns">
    #   <ul class="no-bullet">
    #       <li><b>Puolue:</b> Kristillisdemokraatit</li>
    #      <li><b>Otsikko:</b> Kristillisdemokraattien maahanmuuttopoliittinen ohjelma 2016</li>
    #      <li><b>Vuosi:</b> 2016</li>
    #      <li><b>Ohjelmatyyppi:</b> erityisohjelma</li>
    #   </ul>

    # read the party name and save as string -- <h1>
    try:
        partyname = rds.lineitersearch(mystr, "<li><b>Puolue:</b>", "</li>").strip() 
    except:
        try:
            partyname = rds.lineitersearch(mystr, "<li>Puolue:", "</li>").strip()
        except:
            partyname = None

    # read the programme title and save as string -- <h2>
    
    try:
        progtitle = rds.lineitersearch(mystr, "<li><b>Otsikko:</b>", "</li>").strip()
    except:
        try:
            progtitle = rds.lineitersearch(mystr, "<li>Otsikko:", "</li>").strip()
        except:
            progtitle = None

    
    # read the programme type and save as string
    try:
        progtype = rds.lineitersearch(mystr, "<li><b>Ohjelmatyyppi:</b>", "</li>").strip()
    except:
        try:
            progtype = rds.lineitersearch(mystr, "<li>Ohjelmatyyppi:", "</li>").strip()
        except:
            progtype = None
    
    # read the programme year and save as int
    try:
        progyear = int(rds.lineitersearch(mystr, "<li><b>Vuosi:</b>", "</li>"))
    except:
        try:
            progyear = int(rds.lineitersearch(mystr, "<li>Vuosi:", "</li>"))
        except:
            progyear = None
    
    #save to .html
    try:
        savename_html = rds.savetxtfile(mybytes, partyname.strip(), progyear, progtype.strip(), "_", ".html", "poht_data")
    except:    
        try:
            savename_html = rds.savetxtfile(mystr, partyname.strip(), progyear, progtype.strip(), "_", ".html", "poht_data")
        except:
            savename_html = rds.savetxtfile(mystr, "None", progyear, "None", "_", ".html", "poht_data")
    

    #split the mystr form the <body> tag
    
    mystr_lst = mystr.split("<main>")
    mystr = mystr_lst[1]
    mystr_lst2 = mystr.split("</main>")
    mystr = mystr_lst2[0]

    # parser = BeautifulSoup(mystr, 'html.parser')
    # body = parser.find_all("main")
    # # useful stuff:
    # first_paragraph = parser.find_all("p", id="first")[0]
    # first_inner_paragraph = parser.find_all("p", class_="inner-text")[0]
    
    #clean the mystr: keep only the body and remove html tags
    mystr = rds.cleanhtml(mystr) 

    #remove more than 1 line breaks
    # mystr = rds.cleanemptylines(mystr)
    
    # set up a datafarame SENTS with columns [pname, progtitle, sentence, progtype, year, totalwrds, wrds, totalchars, chars, [KWRDS]]
    #sents = pd.read_excel("poht_data/poht_data.xlsx", header=0, index_col=0)
      
    
    # sents.set_index(0)

    # split mystr to a list of sentences
    # sent_list = re.split('\n|. ', mystr)
    sent_list = []
    mylines = mystr.splitlines()
    print(len(mylines))
    for line in mylines:
        sentences = line.split(".")
        for sentence1 in sentences:
            sent_list.append(sentence1)

    #string for all keywords found in the programme
    prog_kwords = ""
    #string for all keyword hits found in the programme
    prog_kword_hits = ""
    #string for all stopwords found in the programme
    prog_stopwords = ""
    #string for all stopword hits found in the programme
    prog_stopwor_hits = ""

    prog_ment_kw = False
    
    
    # go through the list of sentences
    for sentence in sent_list:
        # sentence = str(sentence)
        sentence = sentence.strip()
        sent = {"pname":partyname, "year":progyear, "progtitle":progtitle, "sentence": str(sentence), 
        "totalwrds":None,"wrds": None, "totalchars":None, "chars":None, "progtype":progtype, 
        "ment_kw":False, "keywords": "", "kw_hits":"", "stopwords":"", "sw_hits":"","url":fname, 
        "filename_html":savename_html, "filename_txt":None}
        sents  = sents.append(sent, ignore_index=True)

    # go through again, iterate the keywords and stopwords and add hits etc. to dataframe
    for index, row in sents.iterrows():
        row["sentence"] = str(row["sentence"])
        for keyword in kwrds:
            keyword = keyword.upper()
            if keyword in row["sentence"].upper():
                words = row["sentence"].split(" ")
                for word in words:
                    word = word.upper()
                    stopped = False
                    for stopword in stopwrds:
                        stopword = stopword.upper()
                        if stopword in word:
                            row["stopwords"] = row["stopwords"] +", "+ stopword.lower()
                            row["sw_hits"] = row["sw_hits"] +", "+ word.lower()
                            prog_stopwords = prog_stopwords + ", "+ stopword.lower()
                            prog_stopwor_hits = prog_stopwor_hits +", "+ word.lower()
                            print("stopword! ", stopword)
                            stopped = True
                    if keyword in word and not stopped:
                                print("keyword!", keyword)
                                row["keywords"] = row["keywords"] +", "+keyword.lower()
                                row["kw_hits"] = row["kw_hits"] +", "+word.lower()
                                prog_kwords = prog_kwords +", "+keyword.lower()
                                prog_kword_hits = prog_kword_hits +", "+word.lower()
                                prog_ment_kw = True
                                row["ment_kw"] = True
        len_row = row["sentence"].split(" ")
        row["wrds"] = len(len_row)
                                     
    # done reading here
    
    
    # add to each row the counts of wrds and chars in the programme -- do not include html tags etc!
    
    sents["chars"] = sents["sentence"].str.len()
    sents["totalchars"] = sents["chars"].sum()
    sents["totalwrds"] = sents["wrds"].sum()

    
    # programme level dataframe
    # read the old programmes dataframe from file
    #old_progs = pd.DataFrame()
    old_progs = pd.read_excel("poht_data/programmes.xlsx", index_col=0)

    prog = {"pname":partyname, "year":progyear, "progtitle":progtitle,  
        "totalwrds":sents["wrds"].sum(),"totalchars":sents["chars"].sum(),"progtype":progtype, 
        "ment_kw":prog_ment_kw, "keywords": prog_kwords, "kw_hits":prog_kword_hits, 
        "stopwords":prog_stopwords, "sw_hits":prog_stopwor_hits,"url":fname, 
        "filename_html":savename_html, "filename_txt":None}
    old_progs  = old_progs.append(prog, ignore_index=True)
    old_progs.to_excel("poht_data/programmes.xlsx")

    # save sentences mentioning keywords to own dataframe
    old_mentions = pd.read_excel("poht_data/mentions.xlsx", index_col=0)
    mentions = sents[sents["ment_kw"] == True]
    mentions = old_mentions.append(mentions)
    mentions.to_excel("poht_data/mentions.xlsx")
    
    # save the cleaned programme
    if prog_ment_kw == True:
        try:
            rds.savetxtfile(mystr, partyname.strip(), progyear, progtype.strip(), "_", ".txt", "poht_data")    
        except:
            try:
                rds.savetxtfile(mybytes, partyname.strip(), progyear, progtype.strip(), "_", ".txt", "poht_data")
            except:
                rds.savetxtfile(mybytes, None, progyear, None, "_", ".txt", "poht_data")

    
    # returns the original order of columns
    
    # combine old and new
    sents = sents.append(old_sents)
    sents = sents[columns]

    # save the dataframe
    # this can be removed when all works well!
    # sents.to_excel("poht_data/poht_data.xlsx")



    # print(sents)

if __name__ == "__main__":
    # these work if you run this module by itself
    # url where to fetch the data
    fname =  "https://www.fsd.tuni.fi/pohtiva/ohjelmalistat/EPV/288"

    # running the function
    poht_read(fname)
