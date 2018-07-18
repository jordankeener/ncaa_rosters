
# list of sports
# note that "mixed" often means mens and womens teams can't be separated easily
# on the roster page, so they are grouped together here and gender
# is determined later on (in the grid scrape function)
def get_sports_list():
    x = ['mens basketball',
         'womens basketball',
         'baseball',
         'football',
         'mens soccer',
         'womens soccer',
         'mens cross country',
         'womens cross country',
         'mens golf',
         'womens golf',
         'mens swimming',
         'womens swimming',
         'mens tennis',
         'womens tennis',
         'mens track',
         'womens track',
         'wrestling',
         'womens field hockey',
         'womens rowing',
         'softball',
         'womens volleyball',
         'mens water polo'
         'womens water polo',
         'mens fencing',
         'womens fencing',
         'mens gymnastics',
         'womens gymnastics',
         'mens hockey',
         'womens hockey',
         'mens lacrosse',
         'womens lacrosse',
         'mens pistol',
         'womens pistol',
         'mixed rifle',
         'mens volleyball',
         'womens synchro swimming',
         'mens rowing',
         'womens rowing light',
         'mixed track',
         'mixed cross country',
         'womens beach volleyball',
         'womens bowling',
         'womens rifle',
         'mixed fencing',
         'mixed swimming',
         'mens sailing',
         'womens sailing',
         'mens skiing',
         'womens skiing',
         'mens squash',
         'womens squash',
         'womens equestrian',
         'womens acrobatics',
         'womens triathlon',
         'mens rugby']
    return x

# converting list of sports to dict 
def get_sports_dict():
    # . --> dictionary with sport keys and empty list values
    sports_list = get_sports_list()
    x = dict.fromkeys(sports_list, list())
    return x
