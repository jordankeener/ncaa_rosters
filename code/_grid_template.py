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


##### school ###########################
full_df = pd.DataFrame()
school = ''
def_gender = 'N/A'

sports_dict = lookups.get_sports_dict()
# {'sport_id' : ['full sport url']}
# sports_dict['baseball'] = ['http://www.huskers.com/SportSelect.dbml?DB_OEM_ID=100&SPID=33&SPSID=104&DB_OEM_ID=100']
sports_dict[''] = ['']


# remove empty sports
for (key, value) in sports_dict.copy().items():
	if value == []:
		del sports_dict[key]

# loop through sports collecting rosters
rosters = proj.gather_rosters_grid(sports_dict)
rosters['college'] = school
csvname = school + '_rosters.csv'
rosters.to_csv(os.path.join(outdir, csvname))
