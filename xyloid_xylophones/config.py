location_sound = 'assets/sounds/'
location_music = 'assets/music/'
location_scenes = 'assets/scenes/'

# zone names
zone_names = ['desolate wasteland', 'northern tundra', 'lush forest']

# starter zone name
current_zone = 'desolate wasteland'

# default player name
player_name = 'Steve'

# assuming all our sprites will be uniform (player == tile == object(item))
sprite_width = 64
sprite_height = 64

# number of squares to find around us (screen_size / sprite_width / 2 )
view_distance = 6

# number of tiles width and height tiles start at -1024,-1024
zone_width = 32
zone_height = 32

# cut scene timeout (0 = wait for action=keypress|mouseClick)
cut_scene = False
cut_scene_timeout = 100
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
]
