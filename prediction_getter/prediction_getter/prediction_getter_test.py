import json
import uuid
from unittest import TestCase
from unittest.mock import patch

prediction_id = str(uuid.UUID(int=0))
the_wire_uuid = uuid.uuid4()
the_sopranos_uuid = uuid.uuid4()
show_ids = [str(the_wire_uuid), str(the_sopranos_uuid)]

from prediction_getter.prediction_getter import lambda_handler


class PredictionGetterTest(TestCase):
    def setUp(self):
        self.mock_get_shows_patch = patch(
            "prediction_getter.prediction_getter.get_shows"
        )
        self.mock_get_prediction_patch = patch(
            "prediction_getter.prediction_getter.get_prediction"
        )
        self.mock_logger_patch = patch(
            "prediction_getter.prediction_getter.logging.getLogger"
        )

        self.mock_get_shows = self.mock_get_shows_patch.start()
        self.mock_get_prediction = self.mock_get_prediction_patch.start()
        self.mock_logger = self.mock_logger_patch.start()

        self.addCleanup(self.mock_get_shows.stop)
        self.addCleanup(self.mock_get_prediction_patch.stop)
        self.addCleanup(self.mock_logger_patch.stop)

    def test_it_requires_a_prediction_id(self):
        event = {"queryStringParameters": {}}
        context = {}

        result = lambda_handler(event, context)

        self.assertEqual(result["statusCode"], 400)

    def test_it_returns_not_found_when_no_prediction_found(self):
        self.mock_get_prediction.return_value = None
        event = {"queryStringParameters": {"prediction_id": prediction_id}}
        context = {}

        result = lambda_handler(event, context)

        self.assertEqual(result["statusCode"], 404)

    def test_it_retrieves_shows_for_prediction(self):
        shows = [
            {
                "id": "id",
                "title": "title",
                "normalized_title": "normalized_title",
                "logo_url": "logo_url",
                "description": "description",
                "air_date": "air_date",
                "rating": "rating",
            }
        ]
        self.mock_get_prediction.return_value = {
            "Prediction": json.dumps([str(the_wire_uuid), str(the_sopranos_uuid)])
        }

        self.mock_get_shows.return_value = shows
        event = {"queryStringParameters": {"prediction_id": prediction_id}}
        context = {}

        result = lambda_handler(event, context)

        self.assertEqual(result["statusCode"], 200)
        self.assertEqual(json.loads(result["body"])["shows"], shows)
