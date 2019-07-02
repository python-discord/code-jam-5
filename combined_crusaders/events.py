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
    "no_history": "Go ahead! Click the crank! Ya silly~"
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
                            max_history_length=100,
                            max_history_seconds=10):
        """Returns what the current message should be.
        Return None if the message should not change."""
        current_time = time.time()
        history = [event for event, event_time
                   in self.event_list[:-max_history_length:-1]
                   if current_time - event_time < max_history_seconds]
        if not history:
            if self.event_list:
                return msgs["went_away"]
            elif current_time - self.start_time < 5:
                return None
            else:
                return msgs["no_history"]
        if len(set(history)) == 1:
            if history[0] == "crank":
                return msgs["only_crank"]
            return msgs["one_thing"]
