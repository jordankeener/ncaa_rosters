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

##### nebraska ###########################
school = 'nebraska'

sports_dict = lookups.get_sports_dict()
sports_dict['baseball'] = ['http://www.huskers.com/SportSelect.dbml?DB_OEM_ID=100&SPID=33&SPSID=104&DB_OEM_ID=100']
sports_dict['mens basketball'] = ['http://www.huskers.com/SportSelect.dbml?DB_OEM_ID=100&SPID=24&SPSID=23&DB_OEM_ID=100']
sports_dict['mixed cross country'] = ['http://www.huskers.com/SportSelect.dbml?DB_OEM_ID=100&SPID=27&SPSID=50&DB_OEM_ID=100']
sports_dict['football'] = ['http://www.huskers.com/SportSelect.dbml?DB_OEM_ID=100&SPID=22&SPSID=4&DB_OEM_ID=100']
sports_dict['mens golf'] = ['http://www.huskers.com/SportSelect.dbml?DB_OEM_ID=100&SPID=35&SPSID=122&DB_OEM_ID=100']
sports_dict['mens gymnastics'] = ['http://www.huskers.com/SportSelect.dbml?DB_OEM_ID=100&SPID=29&SPSID=68&DB_OEM_ID=100']
sports_dict['mens tennis'] = ['http://www.huskers.com/SportSelect.dbml?DB_OEM_ID=100&SPID=37&SPSID=140&DB_OEM_ID=100']
sports_dict['mixed track'] = ['http://www.huskers.com/SportSelect.dbml?DB_OEM_ID=100&SPID=32&SPSID=95&DB_OEM_ID=100']
sports_dict['wrestling'] = ['http://www.huskers.com/SportSelect.dbml?DB_OEM_ID=100&SPID=28&SPSID=61&DB_OEM_ID=100']
sports_dict['womens basketball'] = ['http://www.huskers.com/SportSelect.dbml?DB_OEM_ID=100&SPID=25&SPSID=32&DB_OEM_ID=100']
sports_dict['womens beach volleyball'] = ['http://www.huskers.com/SportSelect.dbml?DB_OEM_ID=100&SPID=123508&SPSID=732210&DB_OEM_ID=100']
sports_dict['womens bowling'] = ['http://www.huskers.com/SportSelect.dbml?DB_OEM_ID=100&SPID=39&SPSID=158&DB_OEM_ID=100']
sports_dict['womens golf'] = ['http://www.huskers.com/SportSelect.dbml?DB_OEM_ID=100&SPID=36&SPSID=131&DB_OEM_ID=100']
sports_dict['womens gymnastics'] = ['http://www.huskers.com/SportSelect.dbml?DB_OEM_ID=100&SPID=30&SPSID=77&DB_OEM_ID=100']
sports_dict['womens rifle'] = ['http://www.huskers.com/SportSelect.dbml?DB_OEM_ID=100&SPID=40&SPSID=167&DB_OEM_ID=100']
sports_dict['womens soccer'] = ['http://www.huskers.com/SportSelect.dbml?DB_OEM_ID=100&SPID=26&SPSID=41&DB_OEM_ID=100']
sports_dict['softball'] = ['http://www.huskers.com/SportSelect.dbml?DB_OEM_ID=100&SPID=34&SPSID=113&DB_OEM_ID=100']
sports_dict['womens swimming'] = ['http://www.huskers.com/SportSelect.dbml?DB_OEM_ID=100&SPID=31&SPSID=86&DB_OEM_ID=100']
sports_dict['womens tennis'] = ['http://www.huskers.com/SportSelect.dbml?DB_OEM_ID=100&SPID=38&SPSID=149&DB_OEM_ID=100']
sports_dict['womens volleyball'] = ['http://www.huskers.com/SportSelect.dbml?DB_OEM_ID=100&SPID=23&SPSID=14&DB_OEM_ID=100']

# remove empty sports
for (key, value) in sports_dict.copy().items():
    if value == []:
        del sports_dict[key]

# loop through sports collecting rosters
rosters = proj.gather_rosters_grid(sports_dict)
rosters['college'] = school
csvname = school + '_rosters.csv'
rosters.to_csv(os.path.join(outdir, csvname))
