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


##### virginia tech #################
full_df = pd.DataFrame()
school = 'virginia_tech'
url_template = 'http://www.hokiesports.com/{sporturl}/players/'
classname = 'table-like'

sports_dict = lookups.get_sports_dict()
# sport_id: [sporturl, sport_table]
sports_dict['baseball'] = ['baseball']
sports_dict['mens basketball'] = ['mbasketball']
sports_dict['womens basketball'] = ['wbasketball']
sports_dict['football'] = ['football']
sports_dict['mens soccer'] = ['msoccer']
sports_dict['womens soccer'] = ['wsoccer']
sports_dict['mens golf'] = ['golf']
sports_dict['womens golf'] = ['wgolf']
sports_dict['womens lacrosse'] = ['lax']
sports_dict['softball'] = ['softball']
sports_dict['mens swimming'] = ['swimming']
sports_dict['womens swimming'] = ['swimming']
sports_dict['mens tennis'] = ['mtennis']
sports_dict['womens tennis'] = ['wtennis']
sports_dict['mens track'] = ['track']
sports_dict['womens track'] = ['track']
sports_dict['womens volleyball'] = ['volleyball']
sports_dict['wrestling'] = ['wrestling']
sports_dict['mens cross country'] = ['cc']
sports_dict['womens cross country'] = ['cc']

# remove empty sports
for (key, value) in sports_dict.copy().items():
	if value == []:
		del sports_dict[key]

# change list number if not first ul of given classname on page
for (key, value) in sports_dict.items():
	if key in ['womens cross country', 'womens swimming', 'womens track']:
		value.append(4)
	else:
		value.append(2)

for (sport_id, sport_info) in sports_dict.items():
    sporturl = sport_info[0]
    ulnum = sport_info[1]
    print(sport_id)
    url = url_template.format(sporturl = sporturl)
    table = proj.get_list(url, classname, numlists=ulnum)
    players = table.find_all('li')

    for player in players:
        name = player.find('div', class_ = 'nameshow').find('a')
        try:
            name = name.get_text().strip()
        except AttributeError:
            name = 'N/A'

        hometown = player.find('div', class_ = 'hometown')
        try:
            hometown = hometown.getText().strip()
        except IndexError:
            hometown = 'N/A'

        player_df = proj.make_player_df(name, hometown, sport_id, school)
        full_df = full_df.append(player_df, ignore_index=True)

csvname = school + '_rosters.csv'
full_df.to_csv(os.path.join(outdir, csvname))
