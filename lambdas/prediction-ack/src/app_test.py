import json
import uuid
from unittest import TestCase
from unittest.mock import patch, MagicMock
from src.app import lambda_handler

empty_uuid = uuid.UUID(int=0)
shows = ["The Wire", "The Sopranos"]


class PredictionAckTest(TestCase):
    def setUp(self):
        self.mock_push_to_queue = patch("src.app.push_to_queue").start()
        self.mock_logger = patch("src.app.logging.getLogger").start()

        self.mock_uuid = patch("src.app.uuid4").start()
        self.mock_uuid.return_value = empty_uuid

    def tearDown(self):
        self.mock_push_to_queue.stop()
        self.mock_uuid.stop()
        self.mock_logger.stop()

    def test_it_pushes_prediction_request_to_queue(self):
        event = {"body": json.dumps({"shows": shows})}
        context = {}
        result = lambda_handler(event, context)

        first_call_args, _ = self.mock_push_to_queue.call_args_list[0]
        first_push_to_queue_arg = first_call_args[0]

        self.mock_push_to_queue.assert_called()
        self.assertEqual(
            first_push_to_queue_arg,
            {"prediction_id": str(empty_uuid), "show_titles": shows},
        )
        self.assertEqual(result["statusCode"], 200)

    def test_it_bad_requests_when_no_shows(self):
        event = {"body": json.dumps({})}
        context = {}
        result = lambda_handler(event, context)

        self.mock_push_to_queue.assert_not_called()
        self.assertEqual(result["statusCode"], 400)

    def test_it_fails_when_queue_push_error_occurs(self):
        event = {"body": json.dumps({"shows": shows})}
        context = {}

        self.mock_push_to_queue.return_value = None

        result = lambda_handler(event, context)

        self.mock_push_to_queue.assert_called()
        self.assertEqual(result["statusCode"], 500)
