
# dictionary from our sport names to default URL
# def get_sports_url_dict():
#     sports_url_dict = {'mens basketball':'mbball',
#                   'womens basketball': 'wbball',
#                   'baseball': 'baseball',
#                   'football': 'football',
#                   'mens soccer': 'msoc',
#                   'womens soccer': 'wsoc',
#                   'mens cross country': 'xc',
#                   'womens cross country': 'xc',
#                   'mens golf': 'mgolf',
#                   'womens golf': 'wgolf',
#                   'mens swimming': 'mswim',
#                   'womens swimming':'wswim',
#                   'mens tennis': 'mten',
#                   'womens tennis': 'wten',
#                   'mens track': 'track',
#                   'womens track': 'track',
#                   'wrestling': 'wrestling',
#                   'womens field hockey': 'fhockey',
#                   'womens rowing': 'wrow',
#                   'softball': 'softball',
#                   'womens volleyball': 'wvball',
#                   'womens water polo': 'wwpolo'}
#
#     return sports_url_dict

# x = get_sports_url_dict()
# sports_list = x.keys()
#
# # dictionary for default table/class ID
# def make_sport_objectid_dict(def_object_name = None):
#     sports_objectid_dict = dict.fromkeys(sports_list, def_object_name)
#     return sports_objectid_dict

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
         'womens squash']
    return x

def get_sports_dict():
    # . --> dictionary with sport keys and empty list values
    sports_list = get_sports_list()
    x = dict.fromkeys(sports_list, list())
    return x
