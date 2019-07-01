import json
import time

import pygame
import src.blocks as blocks
import src.graphics as graphics


def test_file():
    try:
        blocks_file = open("data/blocks.json")
    except FileNotFoundError:
        print("Couldn't find blocks file")
        return False
    try:
        blocks_list = json.load(blocks_file)
    except json.JSONDecodeError:
        print("Couldn't decode blocks file")
        return False

    return_value = True
    for num, block in enumerate(blocks_list):
        try:
            if not type(block["name"]) is str:
                print("block number " + str(num) + "'s name was not a string")
                return_value = False
            elif len(block["name"]) > 25:
                print("block number " + str(num) + "'s name was longer than 25 characters")
                return_value = False
        except KeyError:
            print("block number: " + str(num) + " did not have a name")
            return_value = False

        try:
            if not type(block["impact"]) is int:
                print("block number " + str(num) + "'s impact was not an integer")
                return_value = False
            elif -100 > block["impact"] > 100:
                print("block number " + str(num) + "'s impact was an invalid value")
                return_value = False
        except KeyError:
            print("block number: " + str(num) + " did not have a impact value")
            return_value = False

        try:
            if not type(block["virulence"]) is int:
                print("block number " + str(num) + "'s virulence was not an integer")
                return_value = False
            elif -100 > block["virulence"] > 100:
                print("block number " + str(num) + "'s virulence was an invalid value")
                return_value = False
        except KeyError:
            print("block number: " + str(num) + " did not have a virulence value")
            return_value = False

        try:
            if not type(block["detectability"]) is int:
                print("block number " + str(num) + "'s detectability was not an integer")
                return_value = False
            elif -100 > block["detectability"] > 100:
                print("block number " + str(num) + "'s detectability was an invalid value")
                return_value = False
        except KeyError:
            print("block number: " + str(num) + " did not have a detectability value")
            return_value = False

        try:
            if not type(block["cost"]) is int:
                print("block number " + str(num) + "'s cost was not an integer")
                return_value = False
            elif block["cost"] < 0:
                print("block number " + str(num) + "'s cost was an invalid value")
                return_value = False
        except KeyError:
            print("block number: " + str(num) + " did not have a cost value")
            return_value = False

        try:
            if not type(block["default"]) is int:
                print("block number " + str(num) + "'s default was not an integer")
                return_value = False
            elif block["default"] < 0:
                print("block number " + str(num) + "'s default was an invalid value")
                return_value = False
        except KeyError:
            print("block number: " + str(num) + " did not have a default value")
            return_value = False

        try:
            if not type(block["graphic"]) is str:
                print("block number: " + str(num) + "'s graphic path was not an string")
                return_value = False
            else:
                try:
                    open(block["graphic"], "r").close()
                except FileNotFoundError:
                    print("block number " + str(num) + "'s graphic path appears to be invalid")
                    print("above error's attempted path: " + str(block["graphic"]))
                    return_value = False
        except KeyError:
            print("block number: " + str(num) + " did not have a graphic value")
            return_value = False

    return return_value


def test_cards(wait):
    renderer = graphics.Graphics()

    block_list = blocks.get_blocks(renderer)

    display = pygame.display.set_mode((1500, 120))
    for block in block_list:
        block.graphic.update((7500, 600))
        display.blit(block.graphic.card, (0, 0))
        pygame.display.flip()
        time.sleep(wait)
