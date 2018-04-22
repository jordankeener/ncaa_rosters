# NCAA rosters scraping functions
from urllib.request import urlopen
from urllib.request import FancyURLopener
from bs4 import BeautifulSoup
import pandas as pd
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
            pattern = r'(.*)'+ colname + r'(.*)'
            x = re.match(pattern, item, flags = re.I) != None
            col_matches.append(x)

        try:
            col_index = col_matches.index(True)
            indexes_ordered.append(col_index)
        except ValueError:
            indexes_ordered.append(None)

    print(indexes_ordered)
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
