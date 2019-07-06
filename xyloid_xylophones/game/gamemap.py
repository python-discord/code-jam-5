import pyglet


class Map:
    '''
    Deserialize and draw simplistic map files

    Map files are written in a simple binary format. Each byte
    (valid values from 1 to 255) is a single sprite, drawn from left to right
    on the screen. A byte with a value of zero drops the sprites to the next
    row on the screen, which is done by decreasing the y coordinate by the
    height of the sprites, in this case 64.
    '''

    def __init__(self, filename, associations={}, player_location=(0,0)):
        '''
        Basic init, parse the map file
        '''

        self.filename = filename
        self.associations = associations
        self.player_x, self.player_y = player_location
        self.map = Map._parse(self.associations, self.filename)

    @staticmethod
    def _parse(associations, filename):
        '''
        Deserialize the map file
        '''

        retval = [[]]
        i = 0
        with open(filename, 'rb') as f:
            key = f.read(1)
            while key != b'':
                ikey = int.from_bytes(key, 'big')
                if ikey > 0:
                    retval[i].append(ikey)
                else:
                    i += 1
                    retval.append([])
                key = f.read(1)
        return retval

    def draw(self):
        sprites = []
        batch = pyglet.graphics.Batch()  # Everything gets batched
        x_coord = self.player_x - 5
        y_coord = self.player_y - 4
        for i in range(10): # y coord
            if y_coord < 0:
                y_coord += 1
                continue
            for j in range(10): # x coord
                if x_coord < 0:
                    x_coord += 1
                    continue
                x, y = j * 64, (i + 1) * 64
                try:
                    t = pyglet.sprite.Sprite(
                            self.associations[self.map[y_coord][x_coord]],
                            x,
                            640 - y,
                            batch=batch)
                    t.scale = 2
                    sprites.append(t)
                except IndexError:
                    pass
                x_coord += 1
            x_coord = self.player_x - 5
            y_coord += 1
        batch.draw()
