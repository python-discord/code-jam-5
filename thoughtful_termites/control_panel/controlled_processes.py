import multiprocessing as mp
import subprocess as sp
from thoughtful_termites.shared import qt
from typing import Type

from pathlib import Path

bot_script_path = Path(__file__).parents[1] / 'bot' / '__init__.py'


class ControlledProcess(qt.QThread):
    def __init__(self, process_type: Type[mp.Process], *args, **kwargs):
        super().__init__()
        self.process_type = process_type
        self.args = args
        self.kwargs = kwargs
        self.process: mp.Process = None

    def run(self) -> None:
        self.process = self.process_type(*self.args, **self.kwargs)
        self.process.daemon = True
        self.process.start()
        self.process.join()

    def stop(self):
        self.process.terminate()

    def toggle(self):
        if self.process and self.process.is_alive():
            self.stop()
        else:
            self.start()


class GoalsProcess(mp.Process):
    def run(self) -> None:
        super().run()

        import sys
        from thoughtful_termites import app
        sys.exit(app.run())


class BotControlledProcess(ControlledProcess):
    def __init__(self):
        super().__init__(None)
        self.subprocess: sp.Popen = None

    def run(self) -> None:
        self.subprocess = sp.Popen(
            ['pipenv', 'run', 'python', str(bot_script_path)],
            creationflags=sp.CREATE_NEW_CONSOLE,
            cwd=bot_script_path.parent,
        )

        self.subprocess.wait()

    def stop(self):
        if self.subprocess:
            self.subprocess.kill()
