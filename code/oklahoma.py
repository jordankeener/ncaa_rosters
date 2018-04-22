from urllib.request import urlopen
from urllib.request import FancyURLopener
from bs4 import BeautifulSoup
import pandas as pd
import os
import _proj_functions as proj
import _lookups as lookups
import re

class MyOpener(FancyURLopener):
	version = 'Mozilla/5.0 (Windows; U; Windows NT 5.1; it; rv:1.8.1.11)'
myopener = MyOpener()

outdir = '../output'


##### oklahoma ###########################
full_df = pd.DataFrame()
school = 'oklahoma'
def_gender = 'N/A'

sports_dict = lookups.get_sports_dict()
# {'sport_id' : ['full sport url']}
sports_dict['baseball'] = ['http://www.soonersports.com/SportSelect.dbml?DB_OEM_ID=31000&SPID=127257&SPSID=750376&DB_OEM_ID=31000']
sports_dict['mens basketball'] = ['http://www.soonersports.com/SportSelect.dbml?DB_OEM_ID=31000&SPID=127260&SPSID=750394&DB_OEM_ID=31000']
sports_dict['mixed cross country'] = ['http://www.soonersports.com/SportSelect.dbml?DB_OEM_ID=31000&SPID=127258&SPSID=750386&DB_OEM_ID=31000']
sports_dict['football'] = ['http://www.soonersports.com/SportSelect.dbml?DB_OEM_ID=31000&SPID=127245&SPSID=750326']
sports_dict['mens golf'] = ['http://www.soonersports.com/SportSelect.dbml?DB_OEM_ID=31000&SPID=127252&SPSID=750359&DB_OEM_ID=31000']
sports_dict['mens gymnastics'] = ['http://www.soonersports.com/SportSelect.dbml?DB_OEM_ID=31000&SPID=127248&SPSID=750349&DB_OEM_ID=31000']
sports_dict['mens tennis'] = ['http://www.soonersports.com/SportSelect.dbml?DB_OEM_ID=31000&SPID=127253&SPSID=750366&DB_OEM_ID=31000']
sports_dict['mixed track'] = ['http://www.soonersports.com/SportSelect.dbml?DB_OEM_ID=31000&SPID=127250&SPSID=779713&DB_OEM_ID=31000']
sports_dict['wrestling'] = ['http://www.soonersports.com/SportSelect.dbml?DB_OEM_ID=31000&SPID=127240&SPSID=780015&DB_OEM_ID=31000']
sports_dict['womens basketball'] = ['http://www.soonersports.com/SportSelect.dbml?DB_OEM_ID=31000&SPID=127261&SPSID=750396&DB_OEM_ID=31000']
sports_dict['womens golf'] = ['http://www.soonersports.com/SportSelect.dbml?DB_OEM_ID=31000&SPID=127242&SPSID=779918&DB_OEM_ID=31000']
sports_dict['womens gymnastics'] = ['http://www.soonersports.com/SportSelect.dbml?DB_OEM_ID=31000&SPID=127243&SPSID=750312&DB_OEM_ID=31000']
sports_dict['womens rowing'] = ['http://www.soonersports.com/SportSelect.dbml?DB_OEM_ID=31000&SPID=127244&SPSID=750322&DB_OEM_ID=31000']
sports_dict['womens soccer'] = ['http://www.soonersports.com/SportSelect.dbml?DB_OEM_ID=31000&SPID=127246&SPSID=750337&DB_OEM_ID=31000']
sports_dict['softball'] = ['http://www.soonersports.com/SportSelect.dbml?DB_OEM_ID=31000&SPID=127251&SPSID=779811&DB_OEM_ID=31000']
sports_dict['womens tennis'] = ['http://www.soonersports.com/SportSelect.dbml?DB_OEM_ID=31000&SPID=127254&SPSID=780010&DB_OEM_ID=31000']
sports_dict['womens volleyball'] = ['http://www.soonersports.com/SportSelect.dbml?DB_OEM_ID=31000&SPID=127256&SPSID=779912&DB_OEM_ID=31000']

# remove empty sports
for (key, value) in sports_dict.copy().items():
	if value == []:
		del sports_dict[key]

for (sport_id, sporturl) in sports_dict.items():
    cur_gender = def_gender
    url = sporturl[0]
    grid = proj.get_grid(url, 'roster-grid-layout')
    players = grid.find_all('div')
    roster = []
    for player in players:
        try:
            x = player.get_text().strip()
            if x == 'Men':
                cur_gender = 'Men'
            elif x == 'Women':
                cur_gender = 'Women'
            else:
                pass
            gender = cur_gender
        except:
            try:
                gender = cur_gender
            except:
                gender = def_gender
        lev1 = player.find_all('div')
        for div in lev1:
            try:
                name = div.find('div', class_ = 'player-name').find('a').get_text().strip()
                lev2 = div.find('div', class_ = 'info')
                hometown = lev2.find('div', class_ = 'hometown')
                hometown = hometown.find('span', class_ = 'data').get_text().strip()
                row = [name, hometown, gender]
                roster.append(row)
            except:
                continue

    x = pd.DataFrame(roster, columns = ['name', 'hometown', 'gender'])
    x['sport'] = sport_id
    x['school'] = school
    full_df = full_df.append(x)

csvname = school + '_rosters.csv'
full_df.to_csv(os.path.join(outdir, csvname))
