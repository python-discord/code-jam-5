import math
import random
from PIL import Image,ImageDraw
from characters import *

class game_board:
    def __init__(self, members, size=200):
        self.players = self._players(members)
        self.size = size
        self.board_coords()
        self.seats = self._seats()
        self.board = self._board
        self.seated_players = dict(zip(self.seats, self.players)) 
    def _players(self, members):
        num = len(members)
        acts = num//2+1
        random.shuffle(members)
        players = []
        for i,j in zip(members, [Zilla] + [polluter]*(num-acts-1) + [green_activist]*acts):
            players.append(j(i))
        random.shuffle(players)
        return players
    def board_coords(self):
        sides = len(self.players)
        center = [self.size/2] * 2
        segment = math.pi * 2 / sides
        radius = self.size / 2 - 20
        rotation = segment - math.pi
        if sides % 2 == 0:
            rotation /= 2
        points = [(math.sin(segment * side + rotation) * radius,
                   math.cos(segment * side + rotation) * radius) for side in range(sides)]
        if center:
            points = [tuple(sum(pair) for pair in zip(point, center)) for point in points]
        self.apices = points
    def _seats(self):
        pos = self.apices + [self.apices[0]]
        return [tuple(map(lambda x: sum(x)/2, zip(*pos[index:index+2]))) for index in range(len(self.apices))]
    def _board(self):
        x = Image.new('RGBA', (self.size, self.size), (50,50,50,0))
        draw = ImageDraw.ImageDraw(x)
        draw.polygon(self.apices, fill=(200,200,200))
        for i,j in self.seated_players.items():
            #draw.text(tuple(map(lambda x:x-10, i)), j.name, fill=(125,25,125,200))
            draw.text(i, j.name, fill=(125,125,25))
        x.show()
    def turn_marker(self):
        pass
