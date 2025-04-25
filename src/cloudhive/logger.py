class Logger:
    name: str = __file__
    LOG_LEVELS = {
        "debug": 10,
        "info": 20,
        "warning": 30,
        "error": 40,
        "fatal": 50,
    }

    def __init__(self):
        self.current_level = None
        self.set_level("warning")

    @classmethod
    def get_logger(cls, name=None):
        cls.name = name
        return cls()


    def set_level(self, level: str):
        """Set the log level."""
        level = level.lower()
        if level not in self.LOG_LEVELS:
            raise ValueError(f"Invalid log level: {level}. Choose from {list(self.LOG_LEVELS.keys())}")
        self.current_level = self.LOG_LEVELS[level]

    def log(self, level: str, message: str):
        """Log a message only if the level is >= current log level."""
        level = level.lower()
        if self.LOG_LEVELS[level] >= self.current_level:
            print(f"[{level.upper()}] {message}")

    def debug(self, message: str):
        self.log("debug", message)

    def info(self, message: str):
        self.log("info", message)

    def warning(self, message: str):
        self.log("warning", message)

    def error(self, message: str):
        self.log("error", message)

    def fatal(self, message: str):
        self.log("fatal", message)

"""
>>> logger = Logger.get_logger(name="base")
>>> logger.set_level("debug")
>>> logger.debug("This is the debug line")
"""
