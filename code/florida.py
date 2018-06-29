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
school = 'florida'
url_template = 'http://floridagators.com/roster.aspx?path={sporturl}'

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

# change list number if not first ul of given classname on page
for (key, value) in sports_dict.items():
	if key in []:
		value.append(2)
	else:
		value.append(1)

# loop through sports collecting rosters
rosters = proj.gather_rosters_ul(sports_dict, url_template)
rosters['college'] = school
csvname = school + '_rosters.csv'
rosters.to_csv(os.path.join(outdir, csvname))
