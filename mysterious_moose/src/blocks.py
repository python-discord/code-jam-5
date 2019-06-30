import json
import pygame


class BlockGraphic:
    def __init__(self, image):
        self.image = image


class Block:
    def __init__(self, name, impact, virulence, detectability, image, cost):
        self.name = name
        self.impact = impact
        self.virulence = virulence
        self.detectability = detectability
        self.cost = cost

        self.graphic = BlockGraphic(image)


def get_blocks():
    """ reads data/blocks.json and creates relevant Block objects """
    blocks_file = open("data/blocks.json")
    blocks_list = json.load(blocks_file)
    blocks = []

    for block in blocks_list:
        graphic = pygame.image.load(open(block["graphic"]))
        blocks.append(Block(
            block["name"],
            block["impact"],
            block["virulence"],
            block["detectability"],
            graphic,
            block["cost"]
        ))

    return blocks
