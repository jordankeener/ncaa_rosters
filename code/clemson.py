from urllib.request import urlopen
from urllib.request import FancyURLopener
from bs4 import BeautifulSoup
import pandas as pd
import os
import _proj_functions as proj
import _lookups as lookups
import re

outdir = '../output'

## Softball roster unavailable on 7/17/18
## Track and CC men's and women's rosters are mixed together; ignoring

##### clemson ###########################
school = 'clemson'
url_template = 'http://clemsontigers.com/sports/{sporturl}/roster/'
tableid_template = 'person__list'

sports_dict = lookups.get_sports_dict()
# {'sport_id' : ['full sport url']}
sports_dict['baseball'] = ['baseball']
sports_dict['mens basketball'] = ['mens-basketball']
# sports_dict['mixed cross country'] = []
sports_dict['football'] = ['football']
sports_dict['mens golf'] = ['mens-golf']
sports_dict['mens soccer'] = ['mens-soccer']
sports_dict['mens tennis'] = ['mens-tennis']
# sports_dict['mixed track'] = []
sports_dict['womens basketball'] = ['w-basketball']
sports_dict['womens golf'] = ['womens-golf']
sports_dict['womens rowing'] = ['rowing']
sports_dict['womens soccer'] = ['womens-soccer']
sports_dict['womens tennis'] = ['womens-tennis']
sports_dict['womens volleyball'] = ['volleyball']
# sports_dict['softball'] = ['softball']

# remove empty sports
for (key, value) in sports_dict.copy().items():
	if value == []:
		del sports_dict[key]

# change table names where necessary
for (key, value) in sports_dict.items():
	if key in []:
		value.append(tableid_template + "_M")
	elif key in []:
		value.append(tableid_template + "_F")
	else:
		value.append(tableid_template)

# loop through sports collecting rosters
find_cols = ['name', 'hometown', 'high school', 'school']
rosters = proj.gather_rosters_table(sports_dict, find_cols, url_template)
rosters['college'] = school
csvname = school + '_rosters.csv'
rosters.to_csv(os.path.join(outdir, csvname))
