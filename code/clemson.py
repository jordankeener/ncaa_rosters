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

## Softball roster unavailable on 4/14/2018

##### clemson ###########################
school = 'clemson'

sports_dict = lookups.get_sports_dict()
# {'sport_id' : ['full sport url']}
# sports_dict['baseball'] = ['http://www.huskers.com/SportSelect.dbml?DB_OEM_ID=100&SPID=33&SPSID=104&DB_OEM_ID=100']
sports_dict['baseball'] = ['http://www.clemsontigers.com/SportSelect.dbml?DB_OEM_ID=28500&SPID=103712&SPSID=657822&DB_OEM_ID=28500']
sports_dict['mens basketball'] = ['http://www.clemsontigers.com/SportSelect.dbml?DB_OEM_ID=28500&SPID=103715&SPSID=657840&DB_OEM_ID=28500']
sports_dict['mixed cross country'] = ['http://www.clemsontigers.com/SportSelect.dbml?DB_OEM_ID=28500&SPID=103700&SPSID=657768&DB_OEM_ID=28500']
sports_dict['football'] = ['http://www.clemsontigers.com/SportSelect.dbml?DB_OEM_ID=28500&SPID=103701&SPSID=657772&DB_OEM_ID=28500']
sports_dict['mens golf'] = ['http://www.clemsontigers.com/SportSelect.dbml?DB_OEM_ID=28500&SPID=103708&SPSID=657805&DB_OEM_ID=28500']
sports_dict['mens soccer'] = ['http://www.clemsontigers.com/SportSelect.dbml?DB_OEM_ID=28500&SPID=103704&SPSID=657795&DB_OEM_ID=28500']
sports_dict['mens tennis'] = ['http://www.clemsontigers.com/SportSelect.dbml?DB_OEM_ID=28500&SPID=103709&SPSID=657812&DB_OEM_ID=28500']
sports_dict['mixed track'] = ['http://www.clemsontigers.com/SportSelect.dbml?DB_OEM_ID=28500&SPID=103706&SPSID=667679&DB_OEM_ID=28500']
sports_dict['womens basketball'] = ['http://www.clemsontigers.com/SportSelect.dbml?DB_OEM_ID=28500&SPID=103716&SPSID=657842&DB_OEM_ID=28500']
sports_dict['womens golf'] = ['http://www.clemsontigers.com/SportSelect.dbml?DB_OEM_ID=28500&SPID=103698&SPSID=667668&DB_OEM_ID=28500']
sports_dict['womens rowing'] = ['http://www.clemsontigers.com/SportSelect.dbml?DB_OEM_ID=28500&SPID=103699&SPSID=657758&DB_OEM_ID=28500']
sports_dict['womens soccer'] = ['http://www.clemsontigers.com/SportSelect.dbml?DB_OEM_ID=28500&SPID=103702&SPSID=657783&DB_OEM_ID=28500']
sports_dict['womens tennis'] = ['http://www.clemsontigers.com/SportSelect.dbml?DB_OEM_ID=28500&SPID=103710&SPSID=667671&DB_OEM_ID=28500']
sports_dict['womens volleyball'] = ['http://www.clemsontigers.com/SportSelect.dbml?DB_OEM_ID=28500&SPID=103711&SPSID=667674&DB_OEM_ID=28500']
# sports_dict['softball'] = ['http://www.clemsontigers.com/SportSelect.dbml?DB_OEM_ID=28500&SPID=188508&SPSID=1168112&DB_OEM_ID=28500']

# remove empty sports
for (key, value) in sports_dict.copy().items():
	if value == []:
		del sports_dict[key]

# loop through sports collecting rosters
rosters = proj.gather_rosters_grid(sports_dict)
rosters['college'] = school
csvname = school + '_rosters.csv'
rosters.to_csv(os.path.join(outdir, csvname))
