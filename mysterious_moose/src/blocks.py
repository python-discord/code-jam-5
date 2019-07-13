import json

import pygame


class Block:
    def __init__(self, name, impact, virulence, detectability, image, cost, renderer):
        self.name = name
        self.impact = impact
        self.virulence = virulence
        self.detectability = detectability
        self.cost = cost

        self.graphic = BlockGraphic(name, image, renderer)

    def __mul__(self, other):
        if type(other) is int:
            output = []
            for x in range(other):
                output.append(self)
            return output
        else:
            return NotImplemented


class BlockGraphic:
    def __init__(self, name, image, renderer):
        self.name = name
        self.image = image
        self.renderer = renderer

        self.card = pygame.Surface((500, 120))

        self.resolution = pygame.display.Info()
        self.resolution = (self.resolution.current_w, self.resolution.current_h)
        self.update(self.resolution)

    def update(self, resolution):
        """ updates graphical elements when resolution or virus stats change """
        self.resolution = resolution
        colours = {
            "outline": (200, 200, 200),
            "internal": (75, 75, 75),
            "text": (255, 255, 255)
        }
        self.card = pygame.Surface((1500, 120))
        self.card.fill(colours["outline"])

        image_bg = pygame.Rect(10, 10, 100, 100)
        image = pygame.transform.scale(self.image, (100, 100))

        text_bg = pygame.Rect(120, 10, 1370, 100)
        text = self.renderer.fonts["main"].render(self.name, colours["text"], size=100)[0]
        text_rect = text.get_rect(x=130, centery=60)

        pygame.draw.rect(self.card, colours["internal"], image_bg)
        pygame.draw.rect(self.card, colours["internal"], text_bg)

        self.card.blit(image, (10, 10))
        self.card.blit(text, text_rect)

        self.card = pygame.transform.scale(self.card, (resolution[0]//5, int(resolution[0]*0.016)))


def get_blocks(renderer):
    """ reads data/blocks.json and creates relevant Block objects """
    blocks_file = open("src/data/blocks.json")
    blocks_list = json.load(blocks_file)
    market_blocks = []
    player_blocks = []

    for block in blocks_list:
        graphic = pygame.image.load(open(block["graphic"]))
        block_obj = Block(
            block["name"],
            block["impact"],
            block["virulence"],
            block["detectability"],
            graphic,
            block["cost"],
            renderer
        )
        market_blocks.append(block_obj)

        player_blocks += block_obj*block["default"]

    return market_blocks, player_blocks

