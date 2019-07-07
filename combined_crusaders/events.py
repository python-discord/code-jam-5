"""Module to handle events.
'Events' refers to any notable action that the user has performed.
"""
import time
import random


def detect_event_update(func):
    """Using the result of a message function, update the class properties."""
    def inner(self, *args, **kwargs):
        new_message = func(self, *args, **kwargs)
        if new_message is not None and new_message != self.previous_message:
                self.previous_message = new_message
                self.previous_message_time = time.time()
        return new_message
    return inner


special_messages = [
    "Geese are NEAT",
    "How can mirrors be real if our eyes aren't real",
    "I'm the captain now",
    "Maku is awesome",
    "MissingFragment is awesome",
    "Mahabama is awesome"
    "Maku",
    "Super electromagnetic shrapnel cannon FIRE!",
    "Ideas are bulletproof",
    "What do we say to Death? Not today.",
    "Nao Tomori is best person",
    "Do not use any ligma-identified software in parallel with ClimateClicker",
    "Wear polyester when doing laptop repairs",
    "Don't f*** with my shovel",
    "If I don't come back within five minutes assume I died",
    "You you eat sleep eat sleep whoa why can't I see anything",
    "Expiration dates are just suggestions",
    "Cake am lie",
    "Oh dang is that a gun -Uncle Ben",
    "With great power comes great responsibility -Uncle Ben"
]


msgs = {
    "one_thing": "You uh, sure like doing that, and uh, not anything else",
    "only_crank": "Crank away, m'boy!",
    "went_away": "Hey, you still there? What're you doin",
    "welcome_back": "Welcome back, ya scoundral!",
    "no_history": "Go ahead! Click the crank! Ya silly~",
    "unnecessary_crank": "Keep cranking if ya want, but ya don't need ta",
    "crank_fast_1": "Go, m'boy! Keep cranking!",
    "crank_fast_2": "My god, yer cranking like th' heroes of old!",
    "crank_fast_3": "This... I've never experienced this much POWER before!",
    "crank_fast_4": "Stop, m'boy! You'll kill us all at these speeds!",
    "upgrade_crank_speed": "Nice! Now yer crank'll crank like a dog!",
    "upgrade_crank_points": "Ah, gettin' more bang for yer crank, I see",
    "buy_solar_panel": "Plants survive on solar panels, ye can too!",
    "buy_wind_turbine": "Ah, quite a large crank right there!",
    "upgrade_crank_inertia": "YES! We be discoverin' perpetual motion!",
    "load": "Welcome back! Or maybe not, temporal mechanics confuses me.",
    "save": "Time ain't a toy, boy. You can't save energy by saving a game.",
    "fail_load": "Y'ain't got any save file, boy!"
}


class Events:
    """Class to hold a history of user actions
    parent: Parent object, of class ClimateClicker
    start_time: Unix time at the start of the game
    previous_message_time: Unix time at the last event
    previous_message: Last event message
    event_list: Full history of events
    """
    def __init__(self, parent):
        self.parent = parent
        current_time = time.time()
        self.start_time = current_time
        self.previous_message_time = current_time
        self.previous_message = None
        self.event_list = []
        # TODO there's probably a more optimal data structure for this

    def send(self, event: str):
        """Receive an event code.
        Will be called when the user has performed a notable action.
        """
        self.event_list.append((event, time.time()))

    @detect_event_update
    def get_current_message(self,
                            max_history_length=100):
        """Returns what the current message should be.
        Return None if the message should not change.
        """
        current_time = time.time()
        time_delta = current_time - self.previous_message_time
        full_history = [event for event, event_time in self.event_list]
        short_history = [event for event, event_time
                         in self.event_list[-max_history_length:]
                         if current_time - event_time < 10]
        supershort_history = [event for event, event_time
                              in self.event_list[-max_history_length:]
                              if current_time - event_time < 1]

        if not short_history:
            if full_history:
                return msgs["went_away"]
            elif current_time - self.start_time < 5:
                return None
            else:
                return msgs["no_history"]

        if short_history[-1] == "load":
            return msgs["load"]
        elif short_history[-1] == "save":
            return msgs["save"]
        elif short_history[-1] == "fail_load":
            return msgs["fail_load"]

        if self.previous_message == msgs["went_away"]:
            return msgs["welcome_back"]

        if random.random() < 0.0001:
            return random.choice(special_messages)

        if "buy_upgrade_crank_speed" in supershort_history:
            return msgs["upgrade_crank_speed"]
        if "buy_upgrade_click_value" in supershort_history:
            return msgs["upgrade_crank_points"]
        if "buy_upgrade_crank_inertia" in supershort_history:
            return msgs["upgrade_crank_inertia"]
        if "buy_machine_solar_panel" in supershort_history:
            return msgs["buy_solar_panel"]
        if "buy_machine_wind_turbine" in supershort_history:
            return msgs["buy_wind_turbine"]

        if time_delta < 0.5:
            # Following messages aren't important enough to overwrite that fast
            return None

        if self.parent.speed_sprite.value > 500:
            return msgs["crank_fast_4"]
        if self.parent.speed_sprite.value > 100:
            return msgs["crank_fast_3"]
        if self.parent.speed_sprite.value > 50:
            return msgs["crank_fast_2"]
        if self.parent.speed_sprite.value > 10:
            return msgs["crank_fast_1"]

        if "crank" in short_history and self.parent.energy_per_second > 100:
            return msgs["unnecessary_crank"]
        if len(set(short_history)) == 1:
            if short_history[0] == "crank":
                return msgs["only_crank"]
            return msgs["one_thing"]
