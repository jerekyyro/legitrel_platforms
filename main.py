import poht_read as pore
import readerswriters as rewri 
import pandas as pd
import time

#linklist = rewri.scraper("https://www.fsd.tuni.fi/pohtiva/ohjelmalistat")
#rewri.savelinklist(linklist, "datasources/pohtiva_address_list_2.txt")
# read the list of addresses

starttime = time.time()
print("Starting time at", time.ctime(starttime))


#addr_list = rewri.readlines("datasources/pohtiva_address_list.txt")
addr_list = rewri.readlines("datasources/pohtiva_address_list_3.txt")

old_sents = pd.read_excel("poht_data/programmes.xlsx", index_col=0)
old_addresses = list(old_sents['url'])

# run poht_read for each address in the list, unless already in the file
i = 1
for address in addr_list:
    print("Address "+str(i)+" of "+str(len(addr_list)))
    time_now = ((time.time()-starttime)/i)*len(addr_list)-i
    time_now = time.strftime("%H:%M:%S", time.gmtime(time_now))
    print("Estimated time: "+f"{time_now}")
    i = i + 1

    if address in old_addresses:
        print("Url already in dataset, skipping.")
    else:
        pore.poht_read(address)
        

elapsed_time = time.time() - starttime
print("Elapsed time (HH:MM:SS): ", time.strftime("%H:%M:%S", time.gmtime(elapsed_time)))