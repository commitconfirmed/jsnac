import sys
import logging

class ColorFormatter:
    COLORS = {
        'DEBUG': '\033[94m',    # Blue
        'INFO': '\033[92m',     # Green
        'WARNING': '\033[93m',  # Yellow
        'ERROR': '\033[91m',    # Red
        'CRITICAL': '\033[95m', # Magenta
        'ENDC': '\033[0m',      # Reset to default color
    }

    @staticmethod
    def format(level, message):
        color = ColorFormatter.COLORS.get(level, ColorFormatter.COLORS['ENDC'])
        return f"{color}{level}: {message}{ColorFormatter.COLORS['ENDC']}"

def log(level, message):
    formatted_message = ColorFormatter.format(level, message)
    logging.basicConfig(level=logging.DEBUG)
    logger = logging.getLogger(__name__)
    logger.log(getattr(logging, level), formatted_message)

if __name__ == "__main__":
    log('DEBUG', 'This is a debug message.')
    log('INFO', 'This is an info message.')
    log('WARNING', 'This is a warning message.')
    log('ERROR', 'This is an error message.')
    log('CRITICAL', 'This is a critical message.')