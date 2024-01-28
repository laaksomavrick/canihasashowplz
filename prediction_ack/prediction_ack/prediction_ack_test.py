import json
import uuid
from unittest import TestCase
from unittest.mock import patch

empty_uuid = uuid.UUID(int=0)
the_wire_uuid = uuid.uuid4()
the_sopranos_uuid = uuid.uuid4()
shows = ["The Wire", "The Sopranos"]
show_ids = [the_wire_uuid, the_sopranos_uuid]

from prediction_ack.prediction_ack import lambda_handler


class PredictionAckTest(TestCase):
    def setUp(self):
        self.mock_push_to_queue_patch = patch(
            "prediction_ack.prediction_ack.push_to_queue"
        )
        self.mock_get_show_ids_for_titles_patch = patch(
            "prediction_ack.prediction_ack.get_show_ids_for_titles"
        )
        self.mock_logger_patch = patch(
            "prediction_ack.prediction_ack.logging.getLogger"
        )
        self.mock_uuid_patch = patch("prediction_ack.prediction_ack.uuid4")

        self.mock_push_to_queue = self.mock_push_to_queue_patch.start()
        self.mock_get_show_ids_for_titles = (
            self.mock_get_show_ids_for_titles_patch.start()
        )
        self.mock_logger = self.mock_logger_patch.start()
        self.mock_uuid = self.mock_uuid_patch.start()

        self.mock_get_show_ids_for_titles.return_value = show_ids
        self.mock_uuid.return_value = empty_uuid

        self.addCleanup(self.mock_push_to_queue_patch.stop)
        self.addCleanup(self.mock_get_show_ids_for_titles_patch.stop)
        self.addCleanup(self.mock_logger_patch.stop)
        self.addCleanup(self.mock_uuid_patch.stop)

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
        self.mock_push_to_queue.return_value = None

        event = {"body": json.dumps({"shows": shows})}
        context = {}

        result = lambda_handler(event, context)

        self.mock_push_to_queue.assert_called()
        self.assertEqual(result["statusCode"], 500)
