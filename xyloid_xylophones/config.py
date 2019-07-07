# Dimensions of game Window
game_width = 640
game_height = 640

# Locations
location_sound = 'assets/sounds/'
location_music = 'assets/music/'
location_scene = 'assets/scenes/'

# quest texts
quest_text_start = "zone_desolate wasteland_I'm not happy in this waist land! " \
                   "I should find the rock of transportation and try to fix things!"
quest_text_end = "zone_lush forest_I found a plant I will dedicate my life " \
                 "to nurture it and reverse climate change! yay!"

# zone names
zone_names = ['desolate wasteland', 'northern tundra', 'lush forest']

# assuming all our sprites will be uniform (player == tile == object(item))
sprite_width = 64
sprite_height = 64

# Sprite Options
# Dimensions of the spritesheet
char_sheet_rows = 32
char_sheet_cols = 27
# Position of the desired sprite
sprite_row = 31
sprite_down_col = 1
sprite_up_col = 7
sprite_right_col = 3

# number of squares to find around us (screen_size / sprite_width / 2 )
view_distance = 6

# number of tiles width and height tiles start at -1024,-1024
zone_width = 32
zone_height = 32

# cut scene timeout (0 = wait for action=keypress|mouseClick)
cut_scene = True
cut_scene_timeout = 9
cut_scene_name = 'default_cut_scene'

__all__ = [
    'zone_names',
    'current_zone',
    'player_name',
    'sprite_width',
    'sprite_height',
    'view_distance',
    'zone_width',
    'zone_height',
    'cut_scene',
    'cut_scene_timeout',
    'cut_scene_name',
    'location_sound',
    'location_music',
    'location_scene',
    'game_width',
    'game_height'
]
