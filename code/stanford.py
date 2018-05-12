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


##### stanford #################
full_df = pd.DataFrame()
school = 'stanford'
url_template = 'http://gostanford.com/roster.aspx?path={sporturl}'
classname = 'sidearm-roster-players'

sports_dict = lookups.get_sports_dict()
# sport_id: [sporturl, sport_table]
sports_dict['baseball'] = ['bsb']
sports_dict['mens basketball'] = ['mbball']
sports_dict['womens basketball'] = ['wbball']
sports_dict['football'] = ['football']
sports_dict['mens soccer'] = ['msoc']
sports_dict['womens soccer'] = ['wsoc']
sports_dict['mens golf'] = ['mgolf']
sports_dict['womens golf'] = ['wgolf']
sports_dict['mens swimming'] = ['mswim']
sports_dict['womens swimming'] = ['wswim']
sports_dict['mens tennis'] = ['mten']
sports_dict['womens tennis'] = ['wten']
sports_dict['mens track'] = ['track']
sports_dict['womens track'] = ['track']
sports_dict['mens volleyball'] = ['mvball']
sports_dict['womens volleyball'] = ['wvball']
sports_dict['mens cross country'] = ['xc']
sports_dict['womens cross country'] = ['xc']
sports_dict['mens rowing'] = ['mrow']
sports_dict['womens rowing'] = ['wrow']
sports_dict['wrestling'] = ['wrestling']
sports_dict['softball'] = ['softball']
sports_dict['mens fencing'] = ['fenc']
sports_dict['womens fencing'] = ['fenc']
sports_dict['mens gymnastics'] = ['mgym']
sports_dict['womens gymnastics'] = ['wgym']
sports_dict['mens sailing'] = ['sail']
sports_dict['womens sailing'] = ['sail']
sports_dict['mens water polo'] = ['mwpolo']
sports_dict['womens water polo'] = ['wwpolo']
sports_dict['womens beach volleyball'] = ['bvball']
sports_dict['womens field hockey'] = ['fhockey']
sports_dict['womens lacrosse'] = ['wlax']
sports_dict['womens rowing light'] = ['row_lt']
sports_dict['womens squash'] = ['wsquash']
sports_dict['womens synchro swimming'] = ['syncswim']

# remove empty sports
for (key, value) in sports_dict.copy().items():
	if value == []:
		del sports_dict[key]

# change list number if not first ul of given classname on page
for (key, value) in sports_dict.items():
	if key in ['womens cross country', 'womens fencing', 'womens sailing',
			   'womens track']:
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
    for player in players:
        name = player.find('div',
            class_ = 'sidearm-roster-player-name').find('a').getText().strip()
        hometown_list = player.find('div',
            class_ = 'sidearm-roster-player-class-hometown').find_all('span')

        try:
            hometown = 'N/A'
            for item in hometown_list:
                x = item.getText().strip()
                if ',' in x:
                    hometown = x
                else:
                    continue
        except IndexError:
            hometown = 'N/A'

        player_df = proj.make_player_df(name, hometown, sport_id, school)
        full_df = full_df.append(player_df, ignore_index=True)

csvname = school + '_rosters.csv'
full_df.to_csv(os.path.join(outdir, csvname))