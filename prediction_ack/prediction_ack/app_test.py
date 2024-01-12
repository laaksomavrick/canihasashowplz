import json
import uuid
from unittest import TestCase
from unittest.mock import patch
from prediction_ack.app import lambda_handler

empty_uuid = uuid.UUID(int=0)
the_wire_uuid = uuid.uuid4()
the_sopranos_uuid = uuid.uuid4()
shows = ["The Wire", "The Sopranos"]
show_ids = [the_wire_uuid, the_sopranos_uuid]


class PredictionAckTest(TestCase):
    def setUp(self):
        self.mock_push_to_queue = patch("app.push_to_queue").start()
        self.mock_get_show_ids_for_titles = patch(
            "src.app.get_show_ids_for_titles"
        ).start()
        self.mock_logger = patch("app.logging.getLogger").start()
        self.mock_uuid = patch("app.uuid4").start()

        self.mock_get_show_ids_for_titles.return_value = show_ids
        self.mock_uuid.return_value = empty_uuid

    def tearDown(self):
        self.mock_push_to_queue.stop()
        self.mock_get_show_ids_for_titles.stop()
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
            {"prediction_id": str(empty_uuid), "show_ids": show_ids},
        )
        self.assertEqual(result["statusCode"], 200)

    def test_it_bad_requests_when_no_shows(self):
        event = {"body": json.dumps({})}
        context = {}
        result = lambda_handler(event, context)

        self.mock_push_to_queue.assert_not_called()
        self.assertEqual(result["statusCode"], 400)

    def test_it_not_founds_when_shows_dont_exist(self):
        self.mock_get_show_ids_for_titles.return_value = []
        event = {"body": json.dumps({"shows": shows})}
        context = {}
        result = lambda_handler(event, context)

        self.mock_push_to_queue.assert_not_called()
        self.assertEqual(result["statusCode"], 404)

    def test_it_fails_when_queue_push_error_occurs(self):
        event = {"body": json.dumps({"shows": shows})}
        context = {}

        self.mock_push_to_queue.return_value = None

        result = lambda_handler(event, context)

        self.mock_push_to_queue.assert_called()
        self.assertEqual(result["statusCode"], 500)
