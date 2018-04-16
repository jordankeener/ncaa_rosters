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

## womens soccer, womens rowing, and track have hometown under another level
## just leaving as missing for now
##### syracuse #################
full_df = pd.DataFrame()
school = 'syracuse'
url_template = 'https://cuse.com/roster.aspx?path={sporturl}'
classname = 'sidearm-roster-players'

sports_dict = lookups.get_sports_dict()
# sport_id: [sporturl, sport_table]
sports_dict['mens basketball'] = ['mbasket']
sports_dict['womens basketball'] = ['wbasket']
sports_dict['football'] = ['football']
sports_dict['mens soccer'] = ['msoccer']
sports_dict['womens soccer'] = ['wsoccer']
sports_dict['softball'] = ['softball']
sports_dict['womens tennis'] = ['tennis']
sports_dict['mixed track'] = ['trun']
sports_dict['womens volleyball'] = ['vball']
sports_dict['mixed cross country'] = ['ccountry']
sports_dict['mens rowing'] = ['crew']
sports_dict['womens rowing'] = ['rowing']
sports_dict['mens lacrosse'] = ['mlacrosse']
sports_dict['womens lacrosse'] = ['wlacrosse']
sports_dict['womens field hockey'] = ['fhockey']
sports_dict['womens hockey'] = ['wice']

# remove empty sports
for (key, value) in sports_dict.copy().items():
	if value == []:
		del sports_dict[key]

# change list number if not first ul of given classname on page
for (key, value) in sports_dict.items():
	if key in []:
		value.append(2)
	else:
		value.append(1)

for (sport_id, sport_info) in sports_dict.items():
    sporturl = sport_info[0]
    ulnum = sport_info[1]
    print(sport_id)
    url = url_template.format(sporturl = sporturl)
    table = proj.get_list(url, classname, numlists=ulnum)
    players = table.find_all('li')

    if sport_id in []:
        spannum = 0
    else:
        spannum = 1

    print(spannum)

    for player in players:
        name = player.find('div',
            class_ = 'sidearm-roster-player-name').find('a').getText().strip()
        hometown = player.find('div',
            class_ = 'sidearm-roster-player-class-hometown').find_all('span')

        try:
            hometown = hometown[spannum].getText().strip()
        except IndexError:
            hometown = 'N/A'

        player_df = proj.make_player_df(name, hometown, sport_id, school)
        full_df = full_df.append(player_df, ignore_index=True)

csvname = school + '_rosters.csv'
full_df.to_csv(os.path.join(outdir, csvname))
