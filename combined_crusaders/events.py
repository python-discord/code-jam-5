import time


def detect_event_update(func):
    def inner(self, *args, **kwargs):
        new_message = func(self, *args, **kwargs)
        if new_message == self.previous_message:
            new_message = None
        if new_message is not None:
                self.previous_message = new_message
                self.previous_message_time = time.time()
        return new_message
    return inner


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
    "crank_fast_4": "Stop, m'boy! You'll kill us all at these speeds!"
    }


class Events:
    def __init__(self, master):
        self.master = master
        current_time = time.time()
        self.start_time = current_time
        self.previous_message_time = current_time
        self.previous_message = None
        self.event_list = []
        # TODO there's probably a more optimal data structure for this

    def send(self, event: str):
        self.event_list.append((event, time.time()))

    @detect_event_update
    def get_current_message(self,
                            max_history_length=100):
        """Returns what the current message should be.
        Return None if the message should not change."""
        current_time = time.time()
        full_history = [event for event, event_time in self.event_list]
        short_history = [event for event, event_time
                         in self.event_list[:-max_history_length:-1]
                         if current_time - event_time < 10]
        supershort_history = [event for event, event_time
                              in self.event_list[:-max_history_length:-1]
                              if current_time - event_time < 1]
        if not short_history:
            if full_history:
                return msgs["went_away"]
            elif current_time - self.start_time < 5:
                return None
            else:
                return msgs["no_history"]
        if self.previous_message = msgs["went_away"]:
            return msgs["welcome_back"]
        if self.master.speed_sprite.value > 1000:
            return msgs["crank_fast_1"]
        if self.master.speed_sprite.value > 5000:
            return msgs["crank_fast_2"]
        if self.master.speed_sprite.value > 10000:
            return msgs["crank_fast_3"]
        if self.master.speed_sprite.value > 50000:
            return msgs["crank_fast_4"]
        if "crank" in short_history and self.master.energy_per_second > 100:
            return msgs["unnecessary_crank"]
        if len(set(short_history)) == 1:
            if short_history[0] == "crank":
                return msgs["only_crank"]
            return msgs["one_thing"]
