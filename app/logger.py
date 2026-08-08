import logging

def setup_logging(log_level: str = "INFO") -> None:
    """Set up app-wide logging with safe defaults."""
    resolved_level = getattr(logging, log_level.upper(), logging.INFO)

    logging.basicConfig(
        level=resolved_level,
        format="%(levelname)s: %(message)s",
    )


def get_logger(name: str) -> logging.Logger:
    """Return a logger for a module/file."""
    return logging.getLogger(name)
