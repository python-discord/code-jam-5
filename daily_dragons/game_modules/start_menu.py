import pyglet
import glooey
from pathlib import Path


left = 'form_left.png'
right = 'form_right.png'
center = 'form_center.png'
class NamePrompt(glooey.Label):
    custom_text = "What is your name?"
    custom_alignment = 'center'


class NameForm(glooey.Form):
    custom_alignment = 'top'

    class Label(glooey.EditableLabel):
        custom_font_name = 'Times New Roman'
        custom_font_size = 10
        custom_color = '#ff00ff'
        custom_alignment = 'top left'
        custom_horz_padding = 5
        custom_top_padding = 5
        custom_width_hint = 200

    class Base(glooey.Background):
        custom_center = pyglet.resource.texture(center)
        custom_left = pyglet.resource.texture(left)
        custom_right = pyglet.resource.texture(right)

