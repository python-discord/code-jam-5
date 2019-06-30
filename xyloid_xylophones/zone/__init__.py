from pyqtree import Index
from config import *

item_intangible = 0  # basic tile
item_creature = 1    # creature object (not used)
item_player = 2      # the player (not used will be managed in game loop)
item_container = 3   # interactive item

item = {
    'type': item_intangible,
    'name': 'steve',
    'sound': 0,
    'sprite': 0,
    'collision': False,
    'contains': None
    'location': (0, 0, 0, 0)
}

zone_map = []

for i in zone_names:
    zone_map[i] = Index(bbox=(0, 0, 512, 512))

# TODO: populate zone after we figure out zone size / scaling / bounds

'''
# Usage: example moving right-down
x = 0
y = 0
move_left = 0
move_right = 1
move_up = 0
move_down = 1
for i in zone_map[zone_name.index('desolate wasteland')].intersect(x-move_left,y-move_up,x+move_right,y+move_down):
    if i['collision'] is not True:
        can_move = True

Usage: example render
view_distance = 100
for i in zone_map[zone_name.index('desolate wasteland')].intersect(
        x-view_distance,
        y-view_distance,
        x+view_distance,
        y+view_distance):
    draw(i['sprite'],i['location'][0],i['location'][1],i['location'][2],i['location'][3])
'''
