import json
import uuid
from unittest import TestCase
from unittest.mock import patch
from prediction_worker.app import lambda_handler

prediction_id = str(uuid.UUID(int=0))
the_wire_uuid = uuid.uuid4()
the_sopranos_uuid = uuid.uuid4()
show_ids = [str(the_wire_uuid), str(the_sopranos_uuid)]


class PredictionWorkerTest(TestCase):
    def setUp(self):
        self.mock_write_is_liked = patch("app.write_is_liked").start()
        self.mock_get_prediction = patch("app.get_prediction").start()
        self.mock_save_prediction = patch("app.save_prediction").start()

        self.mock_logger = patch("app.logging.getLogger").start()

    def tearDown(self):
        self.mock_write_is_liked.stop()
        self.mock_get_prediction.stop()
        self.mock_save_prediction.stop()
        self.mock_logger.stop()

    def test_it_retrives_and_saves_prediction(self):
        prediction_uuid = uuid.uuid4()
        self.mock_get_prediction.return_value = [prediction_uuid]

        event = {
            "Records": [
                {
                    "body": json.dumps(
                        {"prediction_id": prediction_id, "show_ids": show_ids}
                    )
                }
            ]
        }
        context = {}
        result = lambda_handler(event, context)

        self.mock_write_is_liked.assert_called_with(show_ids)
        self.mock_get_prediction.assert_called_with(show_ids)
        self.mock_save_prediction.assert_called_with(prediction_id, [prediction_uuid])
        self.assertEqual(result["statusCode"], 200)
