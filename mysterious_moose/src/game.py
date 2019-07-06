import logging

# import pygame
# import src.blocks as blocks
# import src.virus as viruses
# import src.world as world

from mysterious_moose.src.turn_simulation import simulate_turn
from mysterious_moose.src.virus import Virus
from mysterious_moose.src.world import World, INDUSTRIES

log = logging.getLogger("main.game")
log.setLevel(logging.INFO)
log.info("game logger initialised")
#
#
# class Game:
#     def __init__(self, graphics):
#         self.graphics = graphics
#         self.market_blocks, self.player_blocks = blocks.get_blocks(graphics)
#         self.world = world.World()
#         self.view = 0  # current graphical view
#         self.selected = -1  # currently selected virus
#         self.viruses = []
#         self.to_render = []
#
#         # list of graphical elements
#         self.elements = {}
#
#         # whether the mouse is pressed
#         self.pressed = False
#
#         # get resolution
#         display_info = pygame.display.Info()
#         # initialise scalable elements
#         self.resolution = (display_info.current_w, display_info.current_h)
#         self.resolution_change(self.resolution)
#
#         # amount of scroll on the main view
#         self.main_view_scroll = 0
#
#     def update(self, events):
#         """ called each loop to update the game """
#         # logic
#
#         # graphics & mouse interactions
#         # resets things to be rendered
#         self.to_render = []
#
#         # gets mouse position
#         mouse_pos = pygame.mouse.get_pos()
#         mouse_pos = pygame.Rect(mouse_pos[0], mouse_pos[1], 1, 1)
#         mouse_state = pygame.mouse.get_pressed()
#
#         # background
#         self.to_render.append([{"type": "bg", "colour": (0, 0, 0)}])
#
#         if self.view == 0:
#             # main view
#
#             # static objects
#             self.to_render.append([
#                 {
#                     "type": "surface",
#                     "surface": self.elements["mv.tray"],
#                     "dest": self.elements["mv.tray.loc"]
#                 }
#             ])
#
#             up_arrow = self.elements["mv.up"]
#             down_arrow = self.elements["mv.down"]
#             wm_button = self.elements["mv.wm"]
#
#             num_of_viruses = len(self.viruses)
#             total_card_height = (num_of_viruses + 1)*self.elements["mv.card.dy"]
#             virus_buttons = []
#
#             for num, virus in enumerate(self.viruses):
#                 self.to_render.append([{
#                         "type": "surface",
#                         "surface": virus.graphic.card,
#                         "dest": (
#                             self.elements["mv.card.x"],
#                             self.elements["mv.card.dy"]*num + self.main_view_scroll
#                         )
#                     }])
#                 virus_buttons.append(
#                     virus.graphic.card.get_rect(
#                         x=self.elements["mv.card.x"],
#                         y=self.elements["mv.card.dy"]*num + self.main_view_scroll
#                     )
#                 )
#
#             self.to_render.append([{
#                     "type": "surface",
#                     "surface": self.elements["mv.card.new"],
#                     "dest": (
#                         self.elements["mv.card.x"],
#                         self.elements["mv.card.dy"] * num_of_viruses + self.main_view_scroll
#                     )
#                 }])
#             virus_buttons.append(
#                 self.elements["mv.card.new"].get_rect(
#                     x=self.elements["mv.card.x"],
#                     y=self.elements["mv.card.dy"] * num_of_viruses + self.main_view_scroll
#                 )
#             )
#
#             buttons = [
#                 self.elements["mv.buttons.up"],
#                 self.elements["mv.buttons.down"],
#                 self.elements["mv.buttons.wm"]
#             ]
#
#             mouse_collision = mouse_pos.collidelist(buttons + virus_buttons)
#             if mouse_collision > -1:
#
#                 if mouse_state[0] == 1:
#                     self.pressed = True
#                     if mouse_collision == 0:
#                         up_arrow = self.elements["mv.up.pressed"]
#                     elif mouse_collision == 1:
#                         down_arrow = self.elements["mv.down.pressed"]
#                     elif mouse_collision == 2:
#                         wm_button = self.elements["mv.wm.pressed"]
#
#                 elif mouse_state[0] == 0 and self.pressed is True:
#                     self.pressed = False
#                     if mouse_collision == 0:
#                         self.main_view_scroll -= self.elements["mv.card.dy"]
#                         if self.main_view_scroll < self.resolution[1] - total_card_height:
#                             self.main_view_scroll = self.resolution[1] - total_card_height
#                     elif mouse_collision == 1:
#                         self.main_view_scroll += self.elements["mv.card.dy"]
#                         if self.main_view_scroll > 0:
#                             self.main_view_scroll = 0
#                     elif mouse_collision == 2:
#                         self.view = 1
#                     elif mouse_collision > len(buttons) - 1:
#                         virus_collision = mouse_collision - len(buttons)
#                         self.selected = virus_collision
#                         if virus_collision == len(virus_buttons) - 1:
#                             log.info("Creating new virus")
#                             self.viruses.append(viruses.Virus(self.graphics))
#                             self.view = 4
#                         else:
#                             if self.viruses[self.selected].released is True:
#                                 log.info("Transitioning to virus info view: " + str(self.selected))
#                                 self.view = 3
#                             else:
#                                 log.info(
#                                     "Transitioning to virus creation view: " + str(self.selected))
#                                 self.view = 4
#
#                 else:
#                     if mouse_collision == 0:
#                         up_arrow = self.elements["mv.up.hover"]
#                     elif mouse_collision == 1:
#                         down_arrow = self.elements["mv.down.hover"]
#                     elif mouse_collision == 2:
#                         wm_button = self.elements["mv.wm.hover"]
#
#             else:
#                 self.pressed = False
#
#             self.to_render.append([
#                 {
#                     "type": "surface",
#                     "surface": up_arrow,
#                     "dest": self.elements["mv.up.loc"]
#                 }, {
#                     "type": "surface",
#                     "surface": down_arrow,
#                     "dest": self.elements["mv.down.loc"]
#                 }, {
#                     "type": "surface",
#                     "surface": wm_button,
#                     "dest": self.elements["mv.wm.loc"]
#                 }
#
#             ])
#
#         elif self.view == 1:
#             # world map
#             buttons = (
#                 self.elements["wm.buttons.mv"],
#             )
#
#             mv_button = self.elements["wm.mv"]
#
#             mouse_collision = mouse_pos.collidelist(buttons)
#
#             if mouse_collision > -1:
#
#                 if mouse_state[0] == 1:
#                     self.pressed = True
#                     if mouse_collision == 0:
#                         mv_button = self.elements["wm.mv.pressed"]
#
#                 elif mouse_state[0] == 0 and self.pressed is True:
#                     self.pressed = False
#                     if mouse_collision == 0:
#                         self.view = 0
#
#                 else:
#                     if mouse_collision == 0:
#                         mv_button = self.elements["wm.mv.hover"]
#
#             else:
#                 self.pressed = False
#
#             self.to_render.append([
#                 {
#                     "type": "surface",
#                     "surface": mv_button,
#                     "dest": self.elements["wm.mv.loc"]
#                 }
#             ])
#
#         elif self.view == 2:
#             # market
#             pass
#         elif self.view == 3:
#             # virus info
#             buttons = (
#                 self.elements["v.buttons.mv"],
#             )
#
#             mv_button = self.elements["v.mv"]
#
#             mouse_collision = mouse_pos.collidelist(buttons)
#
#             if mouse_collision > -1:
#
#                 if mouse_state[0] == 1:
#                     self.pressed = True
#                     if mouse_collision == 0:
#                         mv_button = self.elements["v.mv.pressed"]
#
#                 elif mouse_state[0] == 0 and self.pressed is True:
#                     self.pressed = False
#                     if mouse_collision == 0:
#                         self.view = 0
#
#                 else:
#                     if mouse_collision == 0:
#                         mv_button = self.elements["v.mv.hover"]
#
#             else:
#                 self.pressed = False
#
#             self.to_render.append([
#                 {
#                     "type": "surface",
#                     "surface": mv_button,
#                     "dest": self.elements["wm.v.loc"]
#                 }
#             ])
#         elif self.view == 4:
#             # virus creation
#
#             # player blocks
#
#             num_of_blocks = len(self.player_blocks)
#             total_card_height = (num_of_blocks + 1) * self.elements["vc.block.dy"]
#             pb_buttons = []
#
#             for num, player_block in enumerate(self.player_blocks):
#                 self.to_render.append([
#                     {
#                         "type": "surface",
#                         "surface": player_block.graphic.card,
#                         "dest": (
#                             self.elements["vc.player_block.x"],
#                             self.elements["vc.block.y"] + num * self.elements["vc.block.dy"])
#                     }
#                 ])
#                 pb_buttons.append(
#                     player_block.graphic.card.get_rect(
#                         x=self.elements["vc.player_block.x"],
#                         y=self.elements["vc.block.y"] + num * self.elements["vc.block.dy"]
#                     )
#                 )
#
#             # virus blocks
#
#             num_of_blocks = len(self.viruses[self.selected].blocks)
#             total_card_height = (num_of_blocks + 1) * self.elements["vc.block.dy"]
#             vb_buttons = []
#
#             for num, virus_block in enumerate(self.viruses[self.selected].blocks):
#                 self.to_render.append([
#                     {
#                         "type": "surface",
#                         "surface": virus_block.graphic.card,
#                         "dest": (
#                             self.elements["vc.virus_block.x"],
#                             self.elements["vc.block.y"] + num * self.elements["vc.block.dy"])
#                     }
#                 ])
#                 vb_buttons.append(
#                     virus_block.graphic.card.get_rect(
#                         x=self.elements["vc.virus_block.x"],
#                         y=self.elements["vc.block.y"] + num * self.elements["vc.block.dy"]
#                     )
#                 )
#
#             buttons = [
#                 self.elements["v.buttons.mv"],
#             ]
#
#             mv_button = self.elements["v.mv"]
#
#             mouse_collision = mouse_pos.collidelist(buttons + pb_buttons + vb_buttons)
#
#             if mouse_collision > -1:
#
#                 if mouse_state[0] == 1:
#                     self.pressed = True
#                     if mouse_collision == 0:
#                         mv_button = self.elements["v.mv.pressed"]
#
#                 elif mouse_state[0] == 0 and self.pressed is True:
#                     self.pressed = False
#                     if mouse_collision == 0:
#                         self.view = 0
#                         self.viruses[self.selected].update_stats()
#
#                     elif mouse_collision > len(buttons + pb_buttons) - 1:
#                         block_collision = mouse_collision - len(buttons + pb_buttons)
#                         self.player_blocks.append(
#                             self.viruses[self.selected].blocks.pop(block_collision)
#                         )
#                     elif mouse_collision > len(buttons) - 1:
#                         block_collision = mouse_collision - len(buttons)
#                         self.viruses[self.selected].blocks.append(
#                             self.player_blocks.pop(block_collision)
#                         )
#
#                 else:
#                     if mouse_collision == 0:
#                         mv_button = self.elements["v.mv.hover"]
#
#             else:
#                 self.pressed = False
#
#             self.to_render.append([
#                 {
#                     "type": "surface",
#                     "surface": mv_button,
#                     "dest": self.elements["v.mv.loc"]
#                 }, {
#                     "type": "surface",
#                     "surface": self.elements["vc.infobar"],
#                     "dest": self.elements["vc.infobar.loc"]
#                 }
#             ])
#         else:
#             log.error("view was set to an invalid value resetting")
#             self.view = 0
#
#         self.graphics.update(self.to_render)
#
#     def resolution_change(self, resolution):
#         """ updates graphical game elements for a new resolution """
#         """
#         abbreviation used in `elements`:
#         mv: main view
#         wm: world map
#         mp: market
#         vi: virus info
#         vc: virus creation
#         v: virus info/creation
#         """
#         # colours
#         colours = {
#             "button": (150, 150, 150),
#             "button_hover": (125, 125, 125),
#             "button_pressed": (100, 100, 100),
#             "tray": (50, 50, 50),
#             "scroll": (75, 75, 75),
#
#             "outline": (200, 200, 200),
#             "internal": (75, 75, 75),
#             "text": (255, 255, 255)
#         }
#
#         self.resolution = resolution
#
#         # viruses
#         for virus in self.viruses:
#             virus.graphic.update(resolution)
#
#         for block in self.market_blocks:
#             block.graphic.update(resolution)
#
#         # main view
#
#         # button to world map
#         # button width
#         button_width = (resolution[0]//15)
#         button = pygame.Surface((button_width, resolution[1]))
#         button.fill(colours["button"])
#
#         button_icon = self.graphics.images["world icon"]
#         button_icon = pygame.transform.scale(button_icon, (button_width, button_width))
#
#         # find button centre
#         button_centre = button_icon.get_rect(center=(button.get_width()//2, button.get_height()//2))
#
#         button.blit(button_icon, button_centre)
#         self.elements["mv.wm"] = button.copy()
#
#         button.fill(colours["button_hover"])
#         button.blit(button_icon, button_centre)
#         self.elements["mv.wm.hover"] = button.copy()
#
#         button.fill(colours["button_pressed"])
#         button.blit(button_icon, button_centre)
#         self.elements["mv.wm.pressed"] = button
#
#         self.elements["mv.wm.loc"] = (0, 0)
#         self.elements["mv.buttons.wm"] = button.get_rect()
#
#         # virus tray
#         virus_tray_width = resolution[0]//5
#         virus_scroll_width = resolution[0]//40
#
#         tray = pygame.Surface((virus_scroll_width + virus_tray_width, resolution[1]))
#
#         scroll_bar = pygame.Rect(0, 0, virus_scroll_width, resolution[1])
#         virus_select = pygame.Rect(virus_scroll_width, 0, virus_tray_width, resolution[1])
#
#         pygame.draw.rect(tray, colours["scroll"], scroll_bar)
#         pygame.draw.rect(tray, colours["tray"], virus_select)
#
#         self.elements["mv.tray"] = tray
#         self.elements["mv.tray.loc"] = (resolution[0] - virus_tray_width - virus_scroll_width, 0)
#
#         # up scroll arrow
#         top_scroll_arrow = pygame.Surface((virus_scroll_width, virus_scroll_width))
#
#         top_scroll_arrow.fill(colours["button"])
#         self.elements["mv.up"] = top_scroll_arrow.copy()
#         top_scroll_arrow.fill(colours["button_hover"])
#         self.elements["mv.up.hover"] = top_scroll_arrow.copy()
#         top_scroll_arrow.fill(colours["button_pressed"])
#         self.elements["mv.up.pressed"] = top_scroll_arrow
#         self.elements["mv.up.loc"] = (
#             resolution[0] - virus_tray_width - virus_scroll_width,
#             0
#         )
#         self.elements["mv.buttons.up"] = pygame.Rect(
#             self.elements["mv.up.loc"],
#             (virus_scroll_width, virus_scroll_width)
#         )
#
#         # down scroll arrow
#         bottom_scroll_arrow = pygame.Surface((virus_scroll_width, virus_scroll_width))
#
#         bottom_scroll_arrow.fill(colours["button"])
#         self.elements["mv.down"] = bottom_scroll_arrow.copy()
#         bottom_scroll_arrow.fill(colours["button_hover"])
#         self.elements["mv.down.hover"] = bottom_scroll_arrow.copy()
#         bottom_scroll_arrow.fill(colours["button_pressed"])
#         self.elements["mv.down.pressed"] = bottom_scroll_arrow
#         self.elements["mv.down.loc"] = (
#             resolution[0] - virus_tray_width - virus_scroll_width,
#             resolution[1] - virus_scroll_width
#         )
#         self.elements["mv.buttons.down"] = pygame.Rect(
#             self.elements["mv.down.loc"],
#             (virus_scroll_width, virus_scroll_width)
#         )
#
#         # create new virus card
#
#         self.elements["mv.card.new"] = pygame.Surface((900, 300))
#         self.elements["mv.card.new"].fill(colours["outline"])
#         internal_bg = pygame.Rect(25, 25, 850, 250)
#
#         name_text = self.graphics.fonts["main"].render("Create new virus", colours["text"], size=60)
#
#         pygame.draw.rect(self.elements["mv.card.new"], colours["internal"], internal_bg)
#
#         self.elements["mv.card.new"].blit(name_text[0], (40, 40))
#
#         self.elements["mv.card.new"] = pygame.transform.scale(
#             self.elements["mv.card.new"],
#             (resolution[0] // 5, resolution[0] // 15)
#         )
#
#         self.elements["mv.card.x"] = resolution[0] - virus_tray_width
#         self.elements["mv.card.dy"] = int(self.elements["mv.card.new"].get_height()*1.1)
#
#         # world view
#
#         # button to main view
#         # button width
#         button_width = (resolution[0] // 15)
#         button = pygame.Surface((button_width, resolution[1]))
#         button.fill(colours["button"])
#
#         button_icon = self.graphics.images["right arrow"]
#         button_icon = pygame.transform.scale(button_icon, (button_width, button_width))
#
#         # find button centre
#         button_centre = button_icon.get_rect(
#             center=(button.get_width() // 2, button.get_height() // 2))
#
#         button.blit(button_icon, button_centre)
#         self.elements["wm.mv"] = button.copy()
#
#         button.fill(colours["button_hover"])
#         button.blit(button_icon, button_centre)
#         self.elements["wm.mv.hover"] = button.copy()
#
#         button.fill(colours["button_pressed"])
#         button.blit(button_icon, button_centre)
#         self.elements["wm.mv.pressed"] = button
#
#         self.elements["wm.mv.loc"] = (resolution[0] - button_width, 0)
#         self.elements["wm.buttons.mv"] = pygame.Rect(
#             self.elements["wm.mv.loc"],
#             (button_width, resolution[1])
#         )
#
#         # virus info/creation
#
#         # button to main view
#         # button width
#         button_width = (resolution[0] // 15)
#         button = pygame.Surface((button_width, resolution[1]))
#         button.fill(colours["button"])
#
#         button_icon = self.graphics.images["left arrow"]
#         button_icon = pygame.transform.scale(button_icon, (button_width, button_width))
#
#         # find button centre
#         button_centre = button_icon.get_rect(
#             center=(button.get_width() // 2, button.get_height() // 2))
#
#         button.blit(button_icon, button_centre)
#         self.elements["v.mv"] = button.copy()
#
#         button.fill(colours["button_hover"])
#         button.blit(button_icon, button_centre)
#         self.elements["v.mv.hover"] = button.copy()
#
#         button.fill(colours["button_pressed"])
#         button.blit(button_icon, button_centre)
#         self.elements["v.mv.pressed"] = button
#
#         self.elements["v.mv.loc"] = (0, 0)
#         self.elements["v.buttons.mv"] = pygame.Rect(
#             self.elements["v.mv.loc"],
#             (button_width, resolution[1])
#         )
#
#         # virus creation
#         sidebar_x = self.elements["v.buttons.mv"][2]
#
#         self.elements["vc.player_block.x"] = (resolution[0] - sidebar_x)//5 + sidebar_x
#         self.elements["vc.virus_block.x"] = (resolution[0] - sidebar_x)//5*3 + sidebar_x
#         self.elements["vc.block.dy"] = int(resolution[0]*0.016)
#         self.elements["vc.block.y"] = self.elements["vc.block.dy"] * 2
#
#         self.elements["vc.infobar"] = pygame.Surface(
#             (resolution[0] - sidebar_x, int(resolution[1]*0.1))
#         )
#         self.elements["vc.infobar"].fill(colours["outline"])
#         self.elements["vc.infobar.loc"] = (sidebar_x, int(resolution[1]*0.9))
#
#
#         release_text = self.graphics.fonts["main"].render("Release!")
#
#         self.elements["vc.release"] = pygame.Surface((resolution[0]//20, resolution[1]//20))


def main():
    earth = World()
    simulate_turn(
        earth,
        Virus(
            10, 50, 70,
            industry=INDUSTRIES.index('Chemical Manufacturing'),
            start_region=earth.regions['West Europe'])
    )


if __name__ == '__main__':
    main()
