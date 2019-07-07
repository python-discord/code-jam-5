"""Module to deal with logic functions not specific to any one other module"""
import pygame
import numpy as np


def in_pixels(normalized_position):
    """Given a normalized position, return the pixel coords.
    'normalized' describes coordinates between 0 and 1; their position
     relative to display size.
    """
    if any(not 0 <= pos <= 1 for pos in normalized_position):
        raise ValueError("Normalized position must be a value between 0 and 1")
    window_size = pygame.display.get_surface().get_size()
    return np.multiply(normalized_position, window_size)


def in_norm(absolute_position):
    """Given a position in pixels, return the normalized coords.
    'normalized' describes coordinates between 0 and 1; their position
     relative to display size.
    """
    window_size = pygame.display.get_surface().get_size()
    return np.divide(absolute_position, window_size)
