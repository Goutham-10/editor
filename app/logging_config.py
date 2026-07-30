import logging
import sys

from app.config import get_settings

_CONFIGURED = False


def configure_logging() -> None:
    global _CONFIGURED
    if _CONFIGURED:
        return

    settings = get_settings()
    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(
        logging.Formatter("%(asctime)s %(levelname)-8s %(name)s: %(message)s")
    )

    root = logging.getLogger()
    root.setLevel(settings.log_level)
    root.addHandler(handler)

    # Noisy third-party loggers stay at WARNING unless explicitly raised.
    logging.getLogger("httpx").setLevel(logging.WARNING)
    logging.getLogger("uvicorn.access").setLevel(logging.WARNING)

    _CONFIGURED = True
