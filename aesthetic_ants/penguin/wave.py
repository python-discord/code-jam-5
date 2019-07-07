import argparse
import inspect
import shlex

from . import enemy


def enemy_class(type):
    # Warning: here be dragons

    try:
        member = getattr(enemy, type)
    except AttributeError:
        raise ValueError(f'{type} is not a valid enemy type')

    # Subclass of Enemy
    if inspect.isclass(member) and issubclass(member, enemy.Enemy):
        return member

    raise ValueError(f'{type} is not a valid enemy type')


def _create_parser():
    def command_rush(args):
        for i in range(args.count):
            yield args.type
            yield args.delay

    def command_sleep(args):
        yield args.delay

    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(help='wave commands')

    sleep_parser = subparsers.add_parser('sleep', help='pauses spawn for some time')
    sleep_parser.set_defaults(func=command_sleep)
    sleep_parser.add_argument('delay', type=float)

    rush_parser = subparsers.add_parser('rush', help='summons an enemy rush')
    rush_parser.set_defaults(func=command_rush)
    rush_parser.add_argument('-t', '--type', type=enemy_class, nargs='?', default=enemy.Enemy)
    rush_parser.add_argument('-c', '--count', type=int)
    rush_parser.add_argument('-d', '--delay', type=float)

    return parser


_PARSER = _create_parser()


class Wave:
    def __init__(self, instructions):
        self.instructions = iter(instructions.splitlines())
        self.current = self._next_instruction()

    def __iter__(self):
        return self

    def __next__(self):
        while True:
            try:
                return next(self.current)
            except StopIteration:
                pass

            self.current = self._next_instruction()

    @classmethod
    def load(cls, filename):
        with open(filename) as f:
            return cls(f.read())

    def _next_instruction(self):
        instruction = next(self.instructions)
        args = _PARSER.parse_args(shlex.split(instruction))
        return args.func(args)
