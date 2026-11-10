import readerswriters as rewri

linklist = rewri.scraper("https://www.fsd.tuni.fi/pohtiva/ohjelmalistat")
rewri.savelinklist(linklist, "datasources/pohtiva_address_list_2.txt")
all_links = []
for line in linklist:
    all_links.append(str(rewri.scraper(line)))

party_links = []
for x in all_links:
    y = x.split(",")
    for z in y:
        
        if "/ohjelmalistat/" in z:
            print(z)
            z = z.strip("[")
            z = z.strip("]")
            z = z.strip("'")
            party_links.append(z)

rewri.savelinklist(party_links, "datasources/pohtiva_address_list_3.txt")
# read the list of addresses