import math
import random
from PIL import Image, ImageDraw
from characters import Characters as char
from collections import deque


class GameBoard:
    def __init__(self, members, size=300):
        self.operators = len(members)
        self.size = size
        self.apices = self.board_coords()
        self.inner = self.board_coords(size*.1)
        self.seats = self._seats()
        self.players = deque(self._players(members))
        self.eliminated = []
        self.board = self._board()
        self.turn_mark = self._turn_mark

    def _players(self, members):
        num = len(members)
        acts = num//2+1
        random.shuffle(members)
        players = []
        for faction, player, position in zip(
            [char.Zilla] + [char.polluter]*(num-acts-1) + [char.green_activist]*acts,
            members, self.seats
        ):
            players.append(faction(player, position))
        random.shuffle(players)
        return players

    def board_coords(self, border=20):
        sides = self.operators
        center = [self.size/2] * 2
        segment = math.pi * 2 / sides
        radius = self.size / 2 - border
        rotation = segment - math.pi
        if sides % 2 == 0:
            rotation /= 2
        points = [(math.sin(segment * side + rotation) * radius,
                   math.cos(segment * side + rotation) * radius) for side in range(sides)]
        if center:
            points = [tuple(sum(pair) for pair in zip(point, center)) for point in points]
        return points

    def _seats(self):
        pos = self.apices + [self.apices[0]]
        return [tuple(map(lambda x: sum(x)/2, zip(*pos[index:index+2])))
                for index in range(len(self.apices))]

    def _board(self):
        board = Image.new('RGBA', (self.size, self.size), (50, 50, 50, 0))
        draw = ImageDraw.ImageDraw(board, 'RGBA')
        draw.polygon(self.apices, fill=(200, 200, 200))
        draw.polygon(self.inner, fill=(78, 46, 40))
        for player in self.players:
            draw.text(player.position, player.name, fill=(125, 125, 25))
        return board

    def _turn_mark(self):
        running_bd = self.board.copy()
        draw = ImageDraw.ImageDraw(running_bd, 'RGBA')
        active = self.players[0]
        active.active = True
        x, y = active.position
        r = self.size*.1
        draw.ellipse((x-r, y-r, x+r, y+r), outline=(255, 223, 0, 0))
        self.players.rotate(1)
        return running_bd
