# import json
# from datetime import datetime
# from app.config import IS_PRODUCTION


# class StructuredLogger:

#     def info(self, data):
#         # In production, suppress INFO logs
#         if IS_PRODUCTION:
#             return

#         log_entry = {
#             "level": "INFO",
#             "timestamp": datetime.utcnow().isoformat(),
#             **data
#         }
#         print(json.dumps(log_entry))

#     def error(self, message):
#         log_entry = {
#             "level": "ERROR",
#             "timestamp": datetime.utcnow().isoformat(),
#             "message": message
#         }
#         print(json.dumps(log_entry))


# logger = StructuredLogger()



















import json
from datetime import datetime


class Logger:

    def _log(self, level, message):

        # If message is a string, convert to dict
        if isinstance(message, str):
            message = {"message": message}

        log_entry = {
            "level": level,
            "timestamp": datetime.utcnow().isoformat(),
            **message
        }

        print(json.dumps(log_entry))


    def info(self, message):
        self._log("INFO", message)


    def error(self, message):
        self._log("ERROR", message)


    def warning(self, message):
        self._log("WARNING", message)


logger = Logger()