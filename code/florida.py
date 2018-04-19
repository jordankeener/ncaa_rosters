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


##### florida #################
full_df = pd.DataFrame()
school = 'florida'
url_template = 'http://floridagators.com/roster.aspx?path={sporturl}'
tableid_template = 'ctl00_cplhMainContent_dgrdRoster'

# bring in sports dictionary (sports: empty list)
sports_dict = lookups.get_sports_dict()
# sport_id: [sporturl, sport_table]
sports_dict['baseball'] = ['baseball']
sports_dict['mens basketball'] = ['basketball-men']
sports_dict['womens basketball'] = ['basketball-women']
sports_dict['mens cross country'] = ['crosscountry']
sports_dict['womens cross country'] = ['crosscountry']
sports_dict['football'] = ['football']
sports_dict['mens golf'] = ['golf-men']
sports_dict['womens golf'] = ['golf-women']
sports_dict['mens swimming'] = ['swimmingdiving-men']
sports_dict['womens swimming'] = ['swimmingdiving-women']
sports_dict['mens tennis'] = ['tennis-men']
sports_dict['womens tennis'] = ['tennis-women']
sports_dict['womens gymnastics'] = ['gymnastics']
sports_dict['womens lacrosse'] = ['lacrosse']
sports_dict['womens soccer'] = ['soccer']
sports_dict['softball'] = ['softball']
sports_dict['mens track'] = ['trackfield']
sports_dict['womens track'] = ['trackfield']
sports_dict['womens volleyball'] = ['volleyball']


# remove empty sports
for (key, value) in sports_dict.copy().items():
	if value == []:
		del sports_dict[key]

# change table names where necessary
for (key, value) in sports_dict.items():
	if key in ['mens cross country', 'mens track']:
		value.append(tableid_template + "_M")
	elif key in ['womens cross country', 'womens track']:
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
