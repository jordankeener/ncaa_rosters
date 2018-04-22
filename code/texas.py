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

# womens track not working 4/22/2018

##### texas #################
full_df = pd.DataFrame()
school = 'texas'
url_template = 'http://texassports.com/roster.aspx?path=football'
classname = 'sidearm-roster-players'

sports_dict = lookups.get_sports_dict()
# sport_id: [sporturl, sport_table]
sports_dict['baseball'] = ['baseball']
sports_dict['mens basketball'] = ['mbball']
sports_dict['womens basketball'] = ['wbball']
sports_dict['football'] = ['football']
sports_dict['womens soccer'] = ['wsoc']
sports_dict['mens golf'] = ['mgolf']
sports_dict['womens golf'] = ['wgolf']
sports_dict['mens swimming'] = ['mswim']
sports_dict['womens swimming'] = ['wswim']
sports_dict['mens tennis'] = ['mten']
sports_dict['womens tennis'] = ['wten']
sports_dict['mens track'] = ['xc_tf']
# sports_dict['womens track'] = ['xc_tf']
sports_dict['womens volleyball'] = ['wvball']
sports_dict['womens rowing'] = ['wrow']
sports_dict['softball'] = ['softball']


# remove empty sports
for (key, value) in sports_dict.copy().items():
	if value == []:
		del sports_dict[key]

# change list number if not first ul of given classname on page
for (key, value) in sports_dict.items():
	if key in ['womens track']:
		value.append(2)
	else:
		value.append(1)

for (sport_id, sport_info) in sports_dict.items():
    sporturl = sport_info[0]
    ulnum = sport_info[1]
    print(sport_id)
    print(ulnum)
    url = url_template.format(sporturl = sporturl)
    table = proj.get_list(url, classname, numlists=ulnum)
    players = table.find_all('li')

    if sport_id in []:
        spannum = 1
    else:
        spannum = 2

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
