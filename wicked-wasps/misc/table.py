import math
from PIL import Image, ImageDraw
from collections import deque


class GameBoard:
    def __init__(self, members, size=300, terminal=True):
        self.operators = len(members)
        self.size = size
        self.apices = self.board_coords()
        self.inner = self.board_coords(size*.1)
        self.seats = self._seats()
        self.players = deque(self._players(members))
        self.eliminated = []
        self.turn_count = 1
        self.board = self._board()
        self.initial_setup()
        self.next_turn = self._turn_mark

    def board_coords(self, border=20):
        sides = self.operators
        center = self.size/2
        segment = math.pi * 2 / sides
        radius = self.size / 2 - border
        rotation = segment - math.pi
        if sides % 2 == 0:
            rotation /= 2
        points = [(math.sin(segment * side + rotation) * radius + center,
                   math.cos(segment * side + rotation) * radius + center) for side in range(sides)]
        # points = [tuple(sum(pair) for pair in zip(point, center)) for point in points]
        return points

    def _seats(self):
        pos = self.apices + [self.apices[0]]
        return [tuple(map(lambda x: sum(x)/2, zip(*pos[index:index+2])))
                for index in range(len(self.apices))]

    def _board(self):
        board = Image.new('RGBA', (self.size, self.size), (50, 50, 50, 0))
        draw = ImageDraw.ImageDraw(board, 'RGBA')
        draw.polygon(self.apices, fill=(200, 200, 200, 0))
        draw.polygon(self.inner, fill=(78, 46, 40, 0))
        for player in self.players:
            draw.text(player.position, player.name, fill=(125, 125, 25, 0))
        return board

    def _turn_mark(self):
        running_bd = self.board.copy()
        draw = ImageDraw.ImageDraw(running_bd, 'RGBA')
        self.active = self.players[0]
        self.active.is_active = True
        x, y = self.active.position
        r = self.size*.1
        draw.ellipse((x-r, y-r, x+r, y+r), outline=(255, 223, 0, 0))
        for eliminated in self.eliminated:
            x, y = eliminated.position
            r = self.size*.05
            draw.ellipse((x-r, y-r, x+r, y+r), outline=(255, 0, 0, 0))
        self.players.rotate(-1)
        return running_bd

    def run(self):
        self._start_phase()
        self._mid_phase()
        self._end_phase()
        # self._turn_mark()

    def to_a4(self):
        pass
