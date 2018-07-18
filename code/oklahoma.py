from urllib.request import urlopen
from urllib.request import FancyURLopener
from bs4 import BeautifulSoup
import pandas as pd
import os
import _proj_functions as proj
import _lookups as lookups
import re

outdir = '../output'

##### oklahoma ###########################
school = 'oklahoma'

sports_dict = lookups.get_sports_dict()
# {'sport_id' : ['full sport url']}
sports_dict['baseball'] = ['http://www.soonersports.com/SportSelect.dbml?DB_OEM_ID=31000&SPID=127257&SPSID=750376&DB_OEM_ID=31000']
sports_dict['mens basketball'] = ['http://www.soonersports.com/SportSelect.dbml?DB_OEM_ID=31000&SPID=127260&SPSID=750394&DB_OEM_ID=31000']
sports_dict['mixed cross country'] = ['http://www.soonersports.com/SportSelect.dbml?DB_OEM_ID=31000&SPID=127258&SPSID=750386&DB_OEM_ID=31000']
sports_dict['football'] = ['http://www.soonersports.com/SportSelect.dbml?DB_OEM_ID=31000&SPID=127245&SPSID=750326']
sports_dict['mens golf'] = ['http://www.soonersports.com/SportSelect.dbml?DB_OEM_ID=31000&SPID=127252&SPSID=750359&DB_OEM_ID=31000']
sports_dict['mens gymnastics'] = ['http://www.soonersports.com/SportSelect.dbml?DB_OEM_ID=31000&SPID=127248&SPSID=750349&DB_OEM_ID=31000']
sports_dict['mens tennis'] = ['http://www.soonersports.com/SportSelect.dbml?DB_OEM_ID=31000&SPID=127253&SPSID=750366&DB_OEM_ID=31000']
sports_dict['mixed track'] = ['http://www.soonersports.com/SportSelect.dbml?DB_OEM_ID=31000&SPID=127250&SPSID=779713&DB_OEM_ID=31000']
sports_dict['wrestling'] = ['http://www.soonersports.com/SportSelect.dbml?DB_OEM_ID=31000&SPID=127240&SPSID=780015&DB_OEM_ID=31000']
sports_dict['womens basketball'] = ['http://www.soonersports.com/SportSelect.dbml?DB_OEM_ID=31000&SPID=127261&SPSID=750396&DB_OEM_ID=31000']
sports_dict['womens golf'] = ['http://www.soonersports.com/SportSelect.dbml?DB_OEM_ID=31000&SPID=127242&SPSID=779918&DB_OEM_ID=31000']
sports_dict['womens gymnastics'] = ['http://www.soonersports.com/SportSelect.dbml?DB_OEM_ID=31000&SPID=127243&SPSID=750312&DB_OEM_ID=31000']
sports_dict['womens rowing'] = ['http://www.soonersports.com/SportSelect.dbml?DB_OEM_ID=31000&SPID=127244&SPSID=750322&DB_OEM_ID=31000']
sports_dict['womens soccer'] = ['http://www.soonersports.com/SportSelect.dbml?DB_OEM_ID=31000&SPID=127246&SPSID=750337&DB_OEM_ID=31000']
sports_dict['softball'] = ['http://www.soonersports.com/SportSelect.dbml?DB_OEM_ID=31000&SPID=127251&SPSID=779811&DB_OEM_ID=31000']
sports_dict['womens tennis'] = ['http://www.soonersports.com/SportSelect.dbml?DB_OEM_ID=31000&SPID=127254&SPSID=780010&DB_OEM_ID=31000']
sports_dict['womens volleyball'] = ['http://www.soonersports.com/SportSelect.dbml?DB_OEM_ID=31000&SPID=127256&SPSID=779912&DB_OEM_ID=31000']

# remove empty sports
for (key, value) in sports_dict.copy().items():
	if value == []:
		del sports_dict[key]

# loop through sports collecting rosters
rosters = proj.gather_rosters_grid(sports_dict)
rosters['college'] = school
csvname = school + '_rosters.csv'
rosters.to_csv(os.path.join(outdir, csvname))
