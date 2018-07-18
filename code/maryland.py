from urllib.request import urlopen
from urllib.request import FancyURLopener
from bs4 import BeautifulSoup
import pandas as pd
import os
import _proj_functions as proj
import _lookups as lookups
import re

outdir = '../output'

##### maryland ###########################
school = 'maryland'
url_template = 'https://umterps.com/roster.aspx?path={sporturl}'

sports_dict = lookups.get_sports_dict()
sports_dict['baseball'] = ['baseball']
sports_dict['mens basketball'] = ['mbball']
sports_dict['football'] = ['football']
sports_dict['mens golf'] = ['mgolf']
sports_dict['mens lacrosse'] = ['mlax']
sports_dict['mens soccer'] = ['msoc']
sports_dict['mens track'] = ['track']
sports_dict['wrestling'] = ['wrestling']
sports_dict['womens basketball'] = ['wbball']
sports_dict['womens cross country'] = ['wcross']
sports_dict['womens field hockey'] = ['fhockey']
sports_dict['womens golf'] = ['wgolf']
sports_dict['womens gymnastics'] = ['gym']
sports_dict['womens lacrosse'] = ['wlax']
sports_dict['womens soccer'] = ['wsoc']
sports_dict['softball'] = ['softball']
sports_dict['womens tennis'] = ['wten']
sports_dict['womens track'] = ['track']
sports_dict['womens volleyball'] = ['vb']

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

# loop through sports collecting rosters
rosters = proj.gather_rosters_ul(sports_dict, url_template)
rosters['college'] = school
csvname = school + '_rosters.csv'
rosters.to_csv(os.path.join(outdir, csvname))
