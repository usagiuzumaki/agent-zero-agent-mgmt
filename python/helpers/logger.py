import json
import logging
import os
import sys
import time
import uuid
from datetime import datetime

class JsonFormatter(logging.Formatter):
    def format(self, record):
        log_record = {
            "timestamp": datetime.fromtimestamp(record.created).isoformat(),
            "level": record.levelname,
            "message": record.getMessage(),
            "module": record.module,
            "funcName": record.funcName,
            "request_id": getattr(record, "request_id", None),
        }
        if record.exc_info:
            log_record["exception"] = self.formatException(record.exc_info)

        # Add extra fields if they exist
        if hasattr(record, "extra_fields"):
            log_record.update(record.extra_fields)

        return json.dumps(log_record)

def setup_logger(name="aria", level=logging.INFO):
    logger = logging.getLogger(name)
    logger.setLevel(level)

    # Check if handler already exists
    if not logger.handlers:
        handler = logging.StreamHandler(sys.stdout)
        handler.setFormatter(JsonFormatter())
        logger.addHandler(handler)

    return logger

# Global logger instance
logger = setup_logger()

def get_logger():
    return logger

class AriaLoggerAdapter(logging.LoggerAdapter):
    def process(self, msg, kwargs):
        extra = self.extra.copy()
        if "extra" in kwargs:
            extra.update(kwargs.pop("extra"))
        kwargs["extra"] = {"extra_fields": extra}
        return msg, kwargs

def get_request_logger(request_id=None):
    if not request_id:
        request_id = str(uuid.uuid4())
    return AriaLoggerAdapter(logger, {"request_id": request_id})
