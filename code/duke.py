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

## Womens soccer roster unavailable on 4/14/2018

##### duke ###########################
full_df = pd.DataFrame()
school = 'duke'
def_gender = 'N/A'

sports_dict = lookups.get_sports_dict()
# {'sport_id' : ['full sport url']}
# ex. sports_dict['baseball'] = ['http://www.huskers.com/SportSelect.dbml?DB_OEM_ID=100&SPID=33&SPSID=104&DB_OEM_ID=100']
sports_dict['baseball'] = ['http://www.goduke.com/SportSelect.dbml?SPID=1850&SPSID=22852&DB_OEM_ID=4200']
sports_dict['mens basketball'] = ['http://www.goduke.com/SportSelect.dbml?SPID=1845&SPSID=22727&DB_OEM_ID=4200']
sports_dict['womens basketball'] = ['http://www.goduke.com/SportSelect.dbml?SPID=1846&SPSID=22763&DB_OEM_ID=4200']
sports_dict['mixed cross country'] = ['http://www.goduke.com/SportSelect.dbml?SPID=1831&SPSID=22403&DB_OEM_ID=4200']
sports_dict['mixed fencing'] = ['http://www.goduke.com/SportSelect.dbml?SPID=2028&SPSID=25950&DB_OEM_ID=4200']
sports_dict['womens field hockey'] = ['http://www.goduke.com/SportSelect.dbml?SPID=2029&SPSID=25945&DB_OEM_ID=4200']
sports_dict['football'] = ['http://www.goduke.com/SportSelect.dbml?SPID=1843&SPSID=22667&DB_OEM_ID=4200']
sports_dict['mens golf'] = ['http://www.goduke.com/SportSelect.dbml?SPID=1837&SPSID=22554&DB_OEM_ID=4200']
sports_dict['womens golf'] = ['http://www.goduke.com/SportSelect.dbml?SPID=1838&SPSID=22564&DB_OEM_ID=4200']
sports_dict['mens lacrosse'] = ['http://www.goduke.com/SportSelect.dbml?SPID=2027&SPSID=25941&DB_OEM_ID=4200']
sports_dict['womens lacrosse'] = ['http://www.goduke.com/SportSelect.dbml?SPID=1832&SPSID=22430&DB_OEM_ID=4200']
sports_dict['womens rowing'] = ['http://www.goduke.com/SportSelect.dbml?SPID=2031&SPSID=25949&DB_OEM_ID=4200']
sports_dict['mens soccer'] = ['http://www.goduke.com/SportSelect.dbml?SPID=1833&SPSID=22446&DB_OEM_ID=4200']
sports_dict['womens soccer'] = ['http://www.goduke.com/SportSelect.dbml?SPID=1842&SPSID=22660&DB_OEM_ID=4200']
sports_dict['softball'] = ['http://www.goduke.com/SportSelect.dbml?SPID=1851&SPSID=22879&DB_OEM_ID=4200']
sports_dict['mixed swimming'] = ['http://www.goduke.com/SportSelect.dbml?SPID=2182&SPSID=27950&DB_OEM_ID=4200']
sports_dict['mens tennis'] = ['http://www.goduke.com/SportSelect.dbml?SPID=1839&SPSID=22590&DB_OEM_ID=4200']
sports_dict['womens tennis'] = ['http://www.goduke.com/SportSelect.dbml?SPID=1840&SPSID=22608&DB_OEM_ID=4200']
sports_dict['mixed track'] = ['http://www.goduke.com/SportSelect.dbml?SPID=1835&SPSID=22497&DB_OEM_ID=4200']
sports_dict['womens volleyball'] = ['http://www.goduke.com/SportSelect.dbml?SPID=1844&SPSID=22705&DB_OEM_ID=4200']
sports_dict['wrestling'] = ['http://www.goduke.com/SportSelect.dbml?SPID=1834&SPSID=22470&DB_OEM_ID=4200']

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
