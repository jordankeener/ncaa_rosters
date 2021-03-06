from urllib.request import urlopen
from urllib.request import FancyURLopener
from bs4 import BeautifulSoup
import pandas as pd
import os
import _proj_functions as proj
import _lookups as lookups
import re

outdir = '../output'

##### ohio state #################
school = "ohio_state"
url_template = 'http://ohiostatebuckeyes.com/sports/{sporturl}/roster/'
tableid_template = 'roster_sort'

# bring in sports dictionary (sports: empty list)
sports_dict = lookups.get_sports_dict()
# sport_id: [sporturl, sport_table]
sports_dict['mens basketball'] = ['m-baskbl']
sports_dict['womens basketball'] = ['w-baskbl']
sports_dict['football'] = ['m-footbl']
sports_dict['mens cross country'] = ['m-xc']
sports_dict['womens cross country'] = ['w-xc']
sports_dict['baseball'] = ['m-basebl']
sports_dict['mens soccer'] = ['m-soccer']
sports_dict['womens soccer'] = ['w-soccer']
sports_dict['mens golf'] = ['m-golf']
sports_dict['womens golf'] = ['w-golf']
sports_dict['mens swimming'] = ['m-swim']
sports_dict['womens swimming'] = ['w-swim']
sports_dict['mens tennis'] = ['m-tennis']
sports_dict['womens tennis'] = ['w-tennis']
sports_dict['mens track'] = ['m-track']
sports_dict['womens track'] = ['w-track']
sports_dict['wrestling'] = ['m-wrestl']
sports_dict['womens field hockey'] = ['w-fieldh']
sports_dict['womens rowing'] = ['w-rowing']
sports_dict['softball'] = ['w-softbl']
sports_dict['womens volleyball'] = ['w-volley']
# sports_dict['mens fencing'] = ['c-fenc']
# sports_dict['womens fencing'] = ['c-fenc']
sports_dict['mens gymnastics'] = ['m-gym']
sports_dict['womens gymnastics'] = ['w-gym']
sports_dict['mens hockey'] = ['m-hockey']
sports_dict['womens hockey'] = ['w-hockey']
sports_dict['mens lacrosse'] = ['m-lacros']
sports_dict['womens lacrosse'] = ['w-lacros']
# sports_dict['mens pistol'] = ['c-pistol']
# sports_dict['womens pistol'] = ['c-pistol']
# sports_dict['mixed rifle'] = ['c-rifle']
sports_dict['mens volleyball'] = ['m-volley']
sports_dict['womens synchro swimming'] = ['w-syncs']

# remove empty sports
for (key, value) in sports_dict.copy().items():
	if value == []:
		del sports_dict[key]

# change table names where necessary
for (key, value) in sports_dict.items():
	if key in ['mens fencing', 'mens pistol']:
		value.append(tableid_template + "_M")
	elif key in ['womens fencing', 'womens pistol']:
		value.append(tableid_template + "_F")
	else:
		value.append(tableid_template)

# collect roster for each sport
find_cols = ['name', 'hometown', 'high school', 'school']
rosters = proj.gather_rosters_table(sports_dict, find_cols, url_template)
rosters['college'] = school
csvname = school + '_rosters.csv'
rosters.to_csv(os.path.join(outdir, csvname))
