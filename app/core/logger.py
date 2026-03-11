import json
from datetime import datetime
from app.config import IS_PRODUCTION


class StructuredLogger:

    def info(self, data):
        # In production, suppress INFO logs
        if IS_PRODUCTION:
            return

        log_entry = {
            "level": "INFO",
            "timestamp": datetime.utcnow().isoformat(),
            **data
        }
        print(json.dumps(log_entry))

    def error(self, message):
        log_entry = {
            "level": "ERROR",
            "timestamp": datetime.utcnow().isoformat(),
            "message": message
        }
        print(json.dumps(log_entry))


logger = StructuredLogger()