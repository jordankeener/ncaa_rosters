from urllib.request import urlopen
from urllib.request import FancyURLopener
from bs4 import BeautifulSoup
import pandas as pd
import os
import _proj_functions as proj
import _lookups as lookups
import re

outdir = '../output'

##### lsu ###########################
school = 'lsu'

sports_dict = lookups.get_sports_dict()
# {'sport_id' : ['full sport url']}
sports_dict['football'] = ['http://www.lsusports.net/SportSelect.dbml?DB_OEM_ID=5200&SPID=2164&SPSID=27812&KEY=&Q_SEASON=2018']
sports_dict['mixed cross country'] = ['http://www.lsusports.net/SportSelect.dbml?SPID=2516&SPSID=54178&DB_OEM_ID=5200']
sports_dict['baseball'] = ['http://www.lsusports.net/SportSelect.dbml?SPID=2173&SPSID=27867&DB_OEM_ID=5200']
sports_dict['mens basketball'] = ['http://www.lsusports.net/SportSelect.dbml?SPID=2166&SPSID=27829&DB_OEM_ID=5200']
sports_dict['womens basketball'] = ['http://www.lsusports.net/SportSelect.dbml?SPID=2167&SPSID=27833&DB_OEM_ID=5200']
sports_dict['womens beach volleyball'] = ['http://www.lsusports.net/SportSelect.dbml?SPID=2169&SPSID=774011&DB_OEM_ID=5200']
sports_dict['mens golf'] = ['http://www.lsusports.net/SportSelect.dbml?SPID=2175&SPSID=27877&DB_OEM_ID=5200']
sports_dict['womens golf'] = ['http://www.lsusports.net/SportSelect.dbml?SPID=2176&SPSID=27885&DB_OEM_ID=5200']
sports_dict['womens gymnastics'] = ['http://www.lsusports.net/SportSelect.dbml?SPID=2171&SPSID=27857&DB_OEM_ID=5200']
sports_dict['womens soccer'] = ['http://www.lsusports.net/SportSelect.dbml?DB_OEM_ID=5200&SPID=2168&SPSID=27839&KEY=&Q_SEASON=2017']
sports_dict['softball'] = ['http://www.lsusports.net/SportSelect.dbml?SPID=2174&SPSID=27872&DB_OEM_ID=5200']
sports_dict['mixed swimming'] = ['http://www.lsusports.net/SportSelect.dbml?SPID=2177&SPSID=27890&DB_OEM_ID=5200']
sports_dict['mens tennis'] = ['http://www.lsusports.net/SportSelect.dbml?SPID=2162&SPSID=27806&DB_OEM_ID=5200']
sports_dict['womens tennis'] = ['http://www.lsusports.net/SportSelect.dbml?SPID=2229&SPSID=28698&DB_OEM_ID=5200']
sports_dict['mixed track'] = ['http://www.lsusports.net/SportSelect.dbml?SPID=2172&SPSID=27861&DB_OEM_ID=5200']
sports_dict['womens volleyball'] = ['http://www.lsusports.net/SportSelect.dbml?DB_OEM_ID=5200&SPID=2165&SPSID=27819&KEY=&Q_SEASON=2017']

# remove empty sports
for (key, value) in sports_dict.copy().items():
	if value == []:
		del sports_dict[key]

# loop through sports collecting rosters
rosters = proj.gather_rosters_grid(sports_dict)
rosters['college'] = school
csvname = school + '_rosters.csv'
rosters.to_csv(os.path.join(outdir, csvname))
