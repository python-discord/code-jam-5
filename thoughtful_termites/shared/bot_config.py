import json
import traceback as tb

class Config:
    def __init__(self):
        self.bot_token: str = ''
        self.client_id: str = ''
        self.owner_id: int = 0

    @classmethod
    def load(cls, path):
        result = cls()

        try:
            with open(path) as file:
                data = json.load(file)

                result.bot_token = data['bot_token']
                result.client_id = data['client_id']
                result.owner_id = data['owner_id']

        except FileNotFoundError:
            pass

        except Exception:  # noqa
            tb.print_exc()

        return result

    def save(self, path):
        with open(path, 'w') as file:
            json.dump({
                'bot_token': self.bot_token,
                'client_id': self.client_id,
                'owner_id': self.owner_id,
            }, file)
