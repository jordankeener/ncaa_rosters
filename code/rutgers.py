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

##### rutgers #################
full_df = pd.DataFrame()
school = "rutgers"
url_template = 'http://scarletknights.com/roster.aspx?path={sporturl}'
classname = 'sidearm-roster-players'

sports_dict = lookups.get_sports_dict()
# sport_id: [sporturl, sport_table]
sports_dict['baseball'] = ['baseball']
sports_dict['mens basketball'] = ['mbball']
sports_dict['womens basketball'] = ['wbball']
sports_dict['football'] = ['football']
sports_dict['mens cross country'] = ['mcross']
sports_dict['womens cross country'] = ['wcross']
sports_dict['mens soccer'] = ['msoc']
sports_dict['womens soccer'] = ['wsoc']
sports_dict['mens golf'] = ['mgolf']
sports_dict['womens golf'] = ['wgolf']
sports_dict['womens swimming'] = ['wswim']
sports_dict['womens tennis'] = ['wten']
sports_dict['mens track'] = ['mtrack']
sports_dict['womens track'] = ['wtrack']
sports_dict['wrestling'] = ['wrestling']
sports_dict['womens field hockey'] = ['fhockey']
sports_dict['womens rowing'] = ['wrow']
sports_dict['softball'] = ['softball']
sports_dict['womens volleyball'] = ['wvball']
sports_dict['mens lacrosse'] = ['mlax']
sports_dict['womens lacrosse'] = ['wlax']
sports_dict['womens gymnastics'] = ['wgym']

# remove empty sports
for (key, value) in sports_dict.copy().items():
	if value == []:
		del sports_dict[key]

for (sport_id, sport_info) in sports_dict.items():
    sporturl = sport_info[0]
    print(sport_id)
    url = url_template.format(sporturl = sporturl)
    table = proj.get_list(url, classname)
    players = table.find_all('li')

    if sport_id in ['womens basketball', 'mens soccer']:
        spannum = 0
    else:
        spannum = 1
    for player in players:
        name = player.find('div',
            class_ = 'sidearm-roster-player-name').find('a').getText().strip()
        hometown = player.find('div',
            class_ = 'sidearm-roster-player-class-hometown').find_all('span')[spannum].getText().strip()

        player_df = pd.DataFrame(index=[0])
        player_df['name'] = name
        player_df['hometown'] = hometown
        player_df['sport'] = sport_id
        player_df['school'] = school
        full_df = full_df.append(player_df, ignore_index=True)

csvname = school + '_rosters.csv'
full_df.to_csv(os.path.join(outdir, csvname))
