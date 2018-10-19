# NCAA rosters scraping functions
from urllib.request import urlopen
from urllib.request import FancyURLopener
from bs4 import BeautifulSoup
import pandas as pd
import requests
import re

class MyOpener(FancyURLopener):
    version = 'Mozilla/5.0 (Windows; U; Windows NT 5.1; it; rv:1.8.1.11)'
myopener = MyOpener()

def select_cols(table, colnames):
    # BeautifulSoup table, list of strings --> list of lists
    # for given table and list of column names,
    # returns first column that matches (non-case sensitive)
    # each column name for each column name
    # returns list of rows (list)
    header = table.find_all('tr')[0]
    rows = table.find_all('tr')[1:]
    header = header.find_all('th')
    header_items = []
    for item in header:
        x = item.get_text().strip()
        header_items.append(x)

    indexes_ordered = []
    for colname in colnames:
        col_matches = []
        for item in header_items:
            pattern = r'(.*)' + colname + r'(.*)'
            x = re.match(pattern, item, flags = re.I) != None
            col_matches.append(x)

        try:
            col_index = col_matches.index(True)
            indexes_ordered.append(col_index)
        except ValueError:
            indexes_ordered.append(None)

    print(indexes_ordered)
    cols_text = []
    for j in indexes_ordered:
        if j is not None:
            cols_text.append(header_items[j])
        else:
            cols_text.append('N/A')
    print(cols_text)
    roster = []
    for row in rows:
        row = row.find_all('td')
        row_items = []
        for item in row:
            x = item.get_text().strip()
            row_items.append(x)
        result = []
        for index in indexes_ordered:
            if index is not None:
                try:
                    result.append(row_items[index])
                except IndexError:
                    print("Index Error - trying previous column")
                    result.append(row_items[index - 1])
            else:
                result.append("N/A")

        result += cols_text
        roster.append(result)

    return roster


def get_table(url, tableid):
    # for when rosters are stored in table objects
    # url (str), tableid (str) --> BeautifulSoup table
    html = myopener.open(url)
    soup = BeautifulSoup(html, 'lxml')
    table = soup.find(id = tableid)
    return table


def get_list(url, classname, numlists=1):
    # for when rosters are stored in unordered list objects
    # url (str), list class (str) --> BeautifulSoup list

    html = myopener.open(url)
    soup = BeautifulSoup(html, 'lxml')

    if numlists == 1:
        mylist = soup.find('ul', class_ = classname)
    elif numlists > 1:
        slice = numlists - 1
        mylist = soup.find_all('ul', class_ = classname)
        print(len(mylist))
        mylist = mylist[slice]
    else:
        mylist = []

    return mylist


def get_roster(sport_id, url_template, sporturl, objectid_dict,
               object_type = 'table',
               subitem = 'tr',
               offset = 0):
    # uses either get_table() or get_list(), then collects rosters
    url = url_template.format(sporturl = sporturl)

    if (object_type == 'table'):
        tableid = objectid_dict[sport_id]
        table = get_table(url, tableid)
    elif (object_type == 'list'):
        classid = objectid_dict[sport_id]
        table = get_list(url, classid)

    if (offset > 0):
        roster = table.find_all(subitem)[offset:]
    else:
        roster = table.find_all(subitem)

    return roster


def get_grid(url, divid):
    html = myopener.open(url)
    soup = BeautifulSoup(html, 'lxml')
    grid = soup.find('div', id = divid)
    return grid


def make_player_df(name, hometown, sport_id, school):
    player_df = pd.DataFrame(index=[0])
    player_df['name'] = name
    player_df['hometown'] = hometown
    player_df['sport'] = sport_id
    player_df['school'] = school
    return player_df


def gather_rosters_ul(sports_dict, url_template):
    # takes dictionary with sport name keys and url/table info and url template
    # --> DataFrame with roster for each sport by finding name, then
    # finding hometown from finding first ul item with comma, then
    # taking the next ul item as guess for high school/previous school

    roster_list = []
    classname = 'sidearm-roster-players'

    for (sport_id, sport_info) in sports_dict.items():
        sporturl = sport_info[0]
        ulnum = sport_info[1]
        print(sport_id)
        url = url_template.format(sporturl = sporturl)
        table = get_list(url, classname, numlists=ulnum)
        players = table.find_all('li')
        for player in players:
            name = player.find('div',
                class_ = 'sidearm-roster-player-name').find('a').getText().strip()
            hometown_list = player.find('div',
                class_ = 'sidearm-roster-player-class-hometown').find_all('span')

            try:
                hometown = 'N/A'
                for (j, item) in enumerate(hometown_list):
                    x = item.getText().strip()
                    if ',' in x:
                        hometown = x
                        try:
                            high_school = hometown_list[j+1].getText().strip()
                        except IndexError:
                            high_school = 'N/A'
                        break
                    else:
                        continue
            except IndexError:
                hometown = 'N/A'
                high_school = 'N/A'
            else:
                if hometown == 'N/A':
                    high_school = 'N/A'

            player_row = [name, hometown, high_school, sport_id]
            roster_list.append(player_row)

    colnames = ['name', 'hometown', 'high school?', 'sport']
    full_df = pd.DataFrame(roster_list, columns = colnames)
    return full_df


def gather_rosters_grid(sports_dict):
    # takes a dictionary with sport name key and url
    # --> DataFrame with roster for each sport
    full_df = pd.DataFrame()
    def_gender = 'N/A'
    for (sport_id, sporturl) in sports_dict.items():
        cur_gender = def_gender
        url = sporturl[0]
        grid = get_grid(url, 'roster-grid-layout')
        players = grid.find_all('div')
        roster = []
        print(sport_id)
        for player in players:
            try:
                x = player.get_text().strip()
                if x == 'Men':
                    cur_gender = 'Men'
                elif x == 'Women':
                    cur_gender = 'Women'
                else:
                    pass
                gender = cur_gender
            except:
                try:
                    gender = cur_gender
                except:
                    gender = def_gender
            lev1 = player.find_all('div')
            for div in lev1:
                try:
                    name = div.find('div', class_ = 'player-name').find('a').get_text().strip()
                    lev2 = div.find('div', class_ = 'info')
                    town_school = lev2.find('div', class_ = 'hometown')
                    town_school = town_school.find('span', class_ = 'data').get_text().strip()

                    hs_start = town_school.rfind('(') + 1
                    hs_end   = town_school.rfind(')')
                    ht_end   = town_school.find('(')

                    if ht_end > 0:
                        hometown = town_school[:ht_end].strip()
                    if (hs_start > 0) & (hs_end > 0):
                        high_school = town_school[hs_start:hs_end].strip()

                    row = [name, hometown, high_school, gender]
                    roster.append(row)
                except AttributeError:
                    continue

        colnames = ['name', 'hometown', 'high_school', 'gender']
        x = pd.DataFrame(roster, columns = colnames)
        x['sport'] = sport_id
        full_df = full_df.append(x)
        print('done' + '\n')

    return full_df


def gather_rosters_table(sports_dict, find_cols, url_template):
    # takes a dictionary with sport name keys and url/table info,
    # list of column names to find, and url template
    # --> DataFrame with roster for each sport based on columns given
    cols_text = []
    for c in find_cols:
         cols_text.append(c + " text")
    colnames = find_cols + cols_text

    full_df = pd.DataFrame()

    for (sport_id, sport_info) in sports_dict.items():
        sporturl = sport_info[0]
        table_id = sport_info[1]
        url = url_template.format(sporturl=sporturl)

        table = get_table(url, table_id)
        print(sport_id + '\n')
        roster = select_cols(table, find_cols)

        x = pd.DataFrame(roster, columns = colnames)
        x['sport'] = sport_id
        full_df = full_df.append(x)

    return full_df
