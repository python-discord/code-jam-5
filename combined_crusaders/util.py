import pygame
import numpy as np


def in_pixels(normalized_position):
    if any(not 0 <= pos <= 1 for pos in normalized_position):
        raise ValueError("Normalized position must be a value between 0 and 1")
    return np.multiply(
        normalized_position, pygame.display.get_surface().get_size())
