class VirusGraphic:
    """ can create and return key Virus graphics"""
    def __init__(self, name):
        self.name = name

        self.impact, self.virulence, self.detectability = 0, 0, 0

    def update_stats(self, impact, virulence, detectability):
        self.impact = impact
        self.virulence = virulence
        self.detectability = detectability


class Virus:
    """ Main Virus class """
    def __init__(self, name):
        self.blocks = []
        self.impact, self.virulence, self.detectability = 0, 0, 0
        self.graphic = VirusGraphic(name)

    def update_stats(self):
        """ updates a virus's key stats to current block values"""
        # reset values
        self.impact, self.virulence, self.detectability = 0, 0, 0

        # read each block and add respective values
        for block in self.blocks:
            self.impact += block.impact
            self.virulence += block.virulence
            self.detectability += block.detectability

        self.graphic.update_stats(self.impact, self.virulence, self.detectability)

    def valid(self):
        """ checks whether the virus is valid or not """
        if len(self.blocks) > 0:
            return True
        else:
            return False

    def add_block(self, block):
        """ adds a block to the virus"""
        self.blocks.append(block)
        self.update_stats()

    def remove_block(self, block):
        """ removes a block from a virus"""
        self.blocks.remove(block)
        self.update_stats()
