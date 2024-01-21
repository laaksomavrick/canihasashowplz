import json
import uuid
from unittest import TestCase
from unittest.mock import patch
from prediction_getter.app import lambda_handler

prediction_id = str(uuid.UUID(int=0))


the_wire_uuid = uuid.uuid4()
the_sopranos_uuid = uuid.uuid4()
show_ids = [str(the_wire_uuid), str(the_sopranos_uuid)]


class PredictionWorkerTest(TestCase):
    def setUp(self):
        self.mock_get_show_titles = patch("app.get_show_titles").start()
        self.mock_get_prediction = patch("app.get_prediction").start()

        self.mock_logger = patch("app.logging.getLogger").start()

    def tearDown(self):
        self.mock_get_show_titles.stop()
        self.mock_get_prediction.stop()
        self.mock_logger.stop()

    # it 400 if no prediction id
    # it 404 if prediction not found
    # it 200

    def it_requires_a_prediction_id(self):
        event = {"queryStringParameters": {}}
        context = {}

        result = lambda_handler(event, context)

        self.assertEqual(result["statusCode"], 400)

    def it_returns_not_found_when_no_prediction_found(self):
        self.mock_get_prediction.return_value = None
        event = {"queryStringParameters": {"prediction_id": prediction_id}}
        context = {}

        result = lambda_handler(event, context)

        self.assertEqual(result["statusCode"], 404)

    def it_retrieves_shows_for_prediction(self):
        self.mock_get_prediction.return_value = json.dumps(
            [the_wire_uuid, the_sopranos_uuid]
        )
        self.mock_get_show_titles.return_value = ["The Wire", "The Sopranos"]
        event = {"queryStringParameters": {"prediction_id": prediction_id}}
        context = {}

        result = lambda_handler(event, context)

        self.assertEqual(result["statusCode"], 200)
        self.assertEqual(
            json.loads(result["body"])["show_titles"], ["The Wire", "The Sopranos"]
        )
