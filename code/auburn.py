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


##### auburn #################
full_df = pd.DataFrame()
school = 'auburn'
url_template = 'http://www.auburntigers.com/sports/{sporturl}/mtt/aub-{sporturl}-mtt.html'
tableid_template = 'sortable_roster'

# bring in sports dictionary (sports: empty list)
sports_dict = lookups.get_sports_dict()
# sport_id: [sporturl, sport_table]
sports_dict['mens basketball'] = ['m-baskbl']
sports_dict['womens basketball'] = ['w-baskbl']
sports_dict['football'] = ['m-footbl']
sports_dict['baseball'] = ['m-basebl']
sports_dict['womens soccer'] = ['w-soccer']
sports_dict['mens golf'] = ['m-golf']
sports_dict['womens golf'] = ['w-golf']
sports_dict['mens swimming'] = ['c-swim']
sports_dict['womens swimming'] = ['c-swim']
sports_dict['mens tennis'] = ['m-tennis']
sports_dict['womens tennis'] = ['w-tennis']
sports_dict['mens track'] = ['c-xctrack']
sports_dict['womens track'] = ['c-xctrack']
sports_dict['softball'] = ['w-softbl']
sports_dict['womens volleyball'] = ['w-volley']
sports_dict['womens gymnastics'] = ['w-gym']
sports_dict['womens equestrian'] = ['w-equest']

# remove empty sports
for (key, value) in sports_dict.copy().items():
	if value == []:
		del sports_dict[key]

# change table names where necessary
for (key, value) in sports_dict.items():
	if key in ['mens swimming', 'mens track']:
		value.append(tableid_template + "_M")
	elif key in ['womens swimming', 'womens track']:
		value.append(tableid_template + "_F")
	else:
		value.append(tableid_template)

# collect roster for each sport
find_cols = ['name', 'hometown']

for (sport_id, sport_info) in sports_dict.items():
	sporturl = sport_info[0]
	table_id = sport_info[1]
	url = url_template.format(sporturl=sporturl)

	table = proj.get_table(url, table_id)
	print(sport_id + '\n')
	roster = proj.select_cols(table, find_cols)

	x = pd.DataFrame(roster, columns = find_cols)
	x['sport'] = sport_id
	x['school'] = school
	full_df = full_df.append(x)

csvname = school + '_rosters.csv'
full_df.to_csv(os.path.join(outdir, csvname))
