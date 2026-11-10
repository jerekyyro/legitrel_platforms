# -*- coding: utf-8 -*-
"""
Spyder Editor

Cleaning data loaded from Pohtiva

"""

#%%
import pandas as pd

#laoding all platforrms (= progs) and mentions

all_progs = pd.read_excel("C:/Users/jerek/Documents/GitHub/Rel-pol-texts/poht_data/programmes.xlsx")
all_ments = pd.read_excel("C:/Users/jerek/Documents/GitHub/Rel-pol-texts/poht_data/mentions.xlsx")

#%%

print(all_progs.info())
print(all_ments.info())

#%%

all_progs.drop_duplicates()
all_ments.drop_duplicates()

all_progs = all_progs.drop_duplicates(subset='url', keep="last")
all_ments = all_ments.drop_duplicates(subset=['url', 'sentence'], keep="last")

all_progs.to_excel("all_progs_no_dupl.xlsx") 
all_ments.to_excel("all_ments_no_dupl.xlsx") 



#%%
all_progs['year'] = all_progs['year'].fillna(0)
all_ments['year'] = all_ments['year'].fillna(0)


all_progs = all_progs.astype({"year": int})
all_ments = all_ments.astype({"year": int})


#%%

#loading data from 2010 to 2020 into own dfs

progs_2010_2020 = all_progs.loc[(all_progs['year'] >= 2010) & (all_progs['year'] <= 2020)]
ments_2010_2020 = all_ments.loc[(all_ments['year'] >= 2010) & (all_ments['year'] <= 2020)]

# Saving to xlsx
progs_2010_2020.to_excel("progs_2010_2020.xlsx") 
ments_2010_2020.to_excel("ments_2010_2020.xlsx") 


#%%
print(progs_2010_2020["year"].unique())
print(ments_2010_2020["year"].unique())

#%%
print(progs_2010_2020["pname"].unique())
#%%

# Loading parties in parliament into own df
edusk_puolueet_2010_20 = ['Kansallinen Kokoomus', 'Muutos 2011' ,'Ruotsalainen kansanpuolue','Suomen Keskusta','Suomen Sosialidemokraattinen Puolue','Vasemmistoliitto','Vihreä liitto','Kristillisdemokraatit','Perussuomalaiset','Sininen tulevaisuus','Seitsemän tähden liike','Liike Nyt']

edk_progs_2010_2020 = progs_2010_2020[progs_2010_2020['pname'].isin(edusk_puolueet_2010_20)]
edk_ments_2010_2020 = ments_2010_2020[ments_2010_2020['pname'].isin(edusk_puolueet_2010_20)]

print(edk_progs_2010_2020['pname'].unique())
print(edk_ments_2010_2020['pname'].unique())

# Saving to xlsx
edk_progs_2010_2020.to_excel("edk_progs_2010_2020.xlsx") 
edk_ments_2010_2020.to_excel("edk_ments_2010_2020.xlsx") 


#%%











