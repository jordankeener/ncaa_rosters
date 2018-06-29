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

##### maryland ###########################
school = 'maryland'

sports_dict = lookups.get_sports_dict()
sports_dict['baseball'] = ['http://www.umterps.com/SportSelect.dbml?DB_OEM_ID=29700&SPID=120725&SPSID=716378&DB_OEM_ID=29700']
sports_dict['mens basketball'] = ['http://www.umterps.com/SportSelect.dbml?DB_OEM_ID=29700&SPID=120728&SPSID=716396&KEY=&Q_SEASON=2017']
sports_dict['football'] = ['http://www.umterps.com/SportSelect.dbml?DB_OEM_ID=29700&SPID=120713&SPSID=716328&DB_OEM_ID=29700']
sports_dict['mens golf'] = ['http://www.umterps.com/SportSelect.dbml?DB_OEM_ID=29700&SPID=120720&SPSID=716361&DB_OEM_ID=29700']
sports_dict['mens lacrosse'] = ['http://www.umterps.com/SportSelect.dbml?DB_OEM_ID=29700&SPID=120711&SPSID=716314&DB_OEM_ID=29700']
sports_dict['mens soccer'] = ['http://www.umterps.com/SportSelect.dbml?DB_OEM_ID=29700&SPID=120714&SPSID=716339&DB_OEM_ID=29700']
sports_dict['mixed track'] = ['http://www.umterps.com/SportSelect.dbml?DB_OEM_ID=29700&SPID=120718&SPSID=751912&DB_OEM_ID=29700']
sports_dict['wrestling'] = ['http://www.umterps.com/SportSelect.dbml?DB_OEM_ID=29700&SPID=120708&SPSID=752115&DB_OEM_ID=29700']
sports_dict['womens basketball'] = ['http://www.umterps.com/SportSelect.dbml?DB_OEM_ID=29700&SPID=120729&SPSID=716398&DB_OEM_ID=29700']
sports_dict['womens cross country'] = ['http://www.umterps.com/SportSelect.dbml?DB_OEM_ID=29700&SPID=120712&SPSID=716324&DB_OEM_ID=29700']
sports_dict['womens field hockey'] = ['http://www.umterps.com/SportSelect.dbml?DB_OEM_ID=29700&SPID=120737&SPSID=751910&DB_OEM_ID=29700']
sports_dict['womens golf'] = ['http://www.umterps.com/SportSelect.dbml?DB_OEM_ID=29700&SPID=120710&SPSID=752111&DB_OEM_ID=29700']
sports_dict['womens gymnastics'] = ['http://www.umterps.com/SportSelect.dbml?DB_OEM_ID=29700&SPID=120716&SPSID=716351&DB_OEM_ID=29700']
sports_dict['womens lacrosse'] = ['http://www.umterps.com/SportSelect.dbml?DB_OEM_ID=29700&SPID=120734&SPSID=752015&DB_OEM_ID=29700']
sports_dict['womens soccer'] = ['http://www.umterps.com/SportSelect.dbml?DB_OEM_ID=29700&SPID=120735&SPSID=752112&DB_OEM_ID=29700']
sports_dict['softball'] = ['http://www.umterps.com/SportSelect.dbml?DB_OEM_ID=29700&SPID=120719&SPSID=716356&DB_OEM_ID=29700']
sports_dict['womens tennis'] = ['http://www.umterps.com/SportSelect.dbml?DB_OEM_ID=29700&SPID=120722&SPSID=752018&DB_OEM_ID=29700']
sports_dict['womens volleyball'] = ['http://www.umterps.com/SportSelect.dbml?DB_OEM_ID=29700&SPID=120724&SPSID=752012&DB_OEM_ID=29700']

# remove empty sports
for (key, value) in sports_dict.copy().items():
	if value == []:
		del sports_dict[key]

# loop through sports collecting rosters
rosters = proj.gather_rosters_grid(sports_dict)
rosters['college'] = school
csvname = school + '_rosters.csv'
rosters.to_csv(os.path.join(outdir, csvname))
