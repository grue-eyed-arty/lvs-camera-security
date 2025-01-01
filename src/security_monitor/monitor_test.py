import unittest
from src.security_monitor import monitor
from datetime import datetime
import json

class MonitorTest(unittest.TestCase):
    #Partially AI generated since this is just a quick verification of the ndjson.
    def test_create_capture_ndjson_line(self):
        timestamp = datetime.now()
        expected = json.dumps({
        "filename": str(timestamp) + ".jpg",
        "timestamp": str(timestamp),
        "type": "test_event"
    })
        result = monitor.create_capture_ndjson_line(timestamp, "test_event")
        self.assertEqual(result, expected)

    #AI generated since this is just a quick verification of the ndjson.
    def test_create_error_ndjson_line(self):
        timestamp = datetime.now()
        expected = json.dumps({
            "timestamp": str(timestamp),
            "error": "test_error",
            "exception_body": "test_exception"
        })
        result = monitor.create_error_ndjson_line(timestamp, "test_error", Exception("test_exception"))
        self.assertEqual(result, expected)

    #AI generated since this is just a quick verification of the ndjson.
    def test_create_activity_ndjson_line(self):
        timestamp = datetime.now()
        expected = json.dumps({
            "timestamp": str(timestamp),
            "activity": "test_activity"
        })
        result = monitor.create_activity_ndjson_line(timestamp, "test_activity")
        self.assertEqual(result, expected)

    #Manually tests happy and null path
    def test_filename_as_jpg(self):
        now = datetime.now()
        name = monitor.filename_as_jpg(now)
        assert(name == str(now) + ".jpg")

        now = None
        name = monitor.filename_as_jpg(now)
        assert(name == str(now) + ".jpg")

