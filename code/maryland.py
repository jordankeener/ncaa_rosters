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

##### maryland ###########################
full_df = pd.DataFrame()
school = 'maryland'
def_gender = 'N/A'

sports_dict = lookups.get_sports_dict()
sports_dict['baseball'] = ['http://www.umterps.com/SportSelect.dbml?DB_OEM_ID=29700&SPID=120725&SPSID=716378&DB_OEM_ID=29700']
sports_dict['mens basketball'] = ['http://www.umterps.com/SportSelect.dbml?DB_OEM_ID=29700&SPID=120728&SPSID=716396&KEY=&Q_SEASON=2017']
sports_dict['football'] = ['http://www.umterps.com/SportSelect.dbml?DB_OEM_ID=29700&SPID=120713&SPSID=716328&DB_OEM_ID=29700']
sports_dict['mens golf'] = ['http://www.umterps.com/SportSelect.dbml?DB_OEM_ID=29700&SPID=120720&SPSID=716361&DB_OEM_ID=29700']
sports_dict['mens lacrosse'] = ['http://www.umterps.com/SportSelect.dbml?DB_OEM_ID=29700&SPID=120711&SPSID=716314&DB_OEM_ID=29700']
sports_dict['mens soccer'] = ['http://www.umterps.com/SportSelect.dbml?DB_OEM_ID=29700&SPID=120714&SPSID=716339&DB_OEM_ID=29700']
sports_dict['mixed track'] = ['http://www.umterps.com/SportSelect.dbml?DB_OEM_ID=29700&SPID=120718&SPSID=751912&DB_OEM_ID=29700']
sports_dict['wrestling'] = ['http://www.umterps.com/SportSelect.dbml?DB_OEM_ID=29700&SPID=120708&SPSID=752115&DB_OEM_ID=29700']
sports_dict['womens basketball'] = ['http://www.umterps.com/SportSelect.dbml?DB_OEM_ID=29700&SPID=120729&SPSID=716398&DB_OEM_ID=29700']
sports_dict['womens cross country'] = ['http://www.umterps.com/SportSelect.dbml?DB_OEM_ID=29700&SPID=120712&SPSID=716324&DB_OEM_ID=29700']
sports_dict['womens field hockey'] = ['http://www.umterps.com/SportSelect.dbml?DB_OEM_ID=29700&SPID=120737&SPSID=751910&DB_OEM_ID=29700']
sports_dict['womens golf'] = ['http://www.umterps.com/SportSelect.dbml?DB_OEM_ID=29700&SPID=120710&SPSID=752111&DB_OEM_ID=29700']
sports_dict['womens gymnastics'] = ['http://www.umterps.com/SportSelect.dbml?DB_OEM_ID=29700&SPID=120716&SPSID=716351&DB_OEM_ID=29700']
sports_dict['womens lacrosse'] = ['http://www.umterps.com/SportSelect.dbml?DB_OEM_ID=29700&SPID=120734&SPSID=752015&DB_OEM_ID=29700']
sports_dict['womens soccer'] = ['http://www.umterps.com/SportSelect.dbml?DB_OEM_ID=29700&SPID=120735&SPSID=752112&DB_OEM_ID=29700']
sports_dict['softball'] = ['http://www.umterps.com/SportSelect.dbml?DB_OEM_ID=29700&SPID=120719&SPSID=716356&DB_OEM_ID=29700']
sports_dict['womens tennis'] = ['http://www.umterps.com/SportSelect.dbml?DB_OEM_ID=29700&SPID=120722&SPSID=752018&DB_OEM_ID=29700']
sports_dict['womens volleyball'] = ['http://www.umterps.com/SportSelect.dbml?DB_OEM_ID=29700&SPID=120724&SPSID=752012&DB_OEM_ID=29700']

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
