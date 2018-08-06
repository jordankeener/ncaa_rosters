# calls each school's scraping file
# then calls do-file that cleans and combines
import subprocess


## 1. scraping each school
import alabama
import arizona_state
import arizona
import arkansas
import auburn
import baylor
import boston_college
import cal
import clemson
import colorado
import duke
import florida_state
import florida
import georgia_tech
import georgia
import illinois
import indiana
import iowa_state
import iowa
import kansas_state
import kansas
import kentucky
import louisville
import lsu
import maryland
import miami
import michigan_state
import michigan
import minnesota
import miss_state
import missouri
import nc_state
import nebraska
import north_carolina
import northwestern
import notre_dame
import ohio_state
import oklahoma_state
import oklahoma
import ole_miss
import oregon_state
import oregon
import penn_state
import pitt
import purdue
import rutgers
import south_carolina
import stanford
import syracuse
import tcu
import tennessee
import texas_am
import texas_tech
import texas
import ucla
import usc
import utah
import vanderbilt
import virginia_tech
import virginia
import wake_forest
import washington_state
import washington
import west_virginia
import wisconsin

## 2. cleaning rosters and combining to single dataset
rundofile = ['StataMP-64', 'do', 'clean/clean.do']
subprocess.call(rundofile)
