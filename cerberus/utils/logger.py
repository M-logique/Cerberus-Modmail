import logging as _logging
from colorlog import ColoredFormatter as _ColoredFormatter

class DiscordLogger(_logging.Logger):
    def __init__(self, name):
        super().__init__(name)
        self.setLevel(_logging.INFO)

        formatter = _ColoredFormatter(
            '%(asctime)s | %(log_color)s%(levelname)s%(reset)s | %(message)s',
            datefmt='%H:%M:%S',
            log_colors={
                'DEBUG':    'cyan',
                'INFO':     'green',
                'WARNING':  'yellow',
                'ERROR':    'red',
                'CRITICAL': 'red',
            }
        )

        handler = _logging.StreamHandler()
        handler.setFormatter(formatter)
        self.addHandler(handler)

        self.info(f'{self.name} logger initialized.')

logger = DiscordLogger('Cerberus-ModMail')