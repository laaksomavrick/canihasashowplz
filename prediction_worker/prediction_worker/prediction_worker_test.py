import json
import uuid
from unittest import TestCase
from unittest.mock import patch

prediction_id = str(uuid.UUID(int=0))
the_wire_uuid = uuid.uuid4()
the_sopranos_uuid = uuid.uuid4()
show_ids = [str(the_wire_uuid), str(the_sopranos_uuid)]

from prediction_worker.prediction_worker import lambda_handler


class PredictionWorkerTest(TestCase):
    def setUp(self):
        self.mock_write_is_liked_patch = patch(
            "prediction_worker.prediction_worker.write_is_liked"
        )
        self.mock_get_prediction_patch = patch(
            "prediction_worker.prediction_worker.get_prediction"
        )
        self.mock_save_prediction_patch = patch(
            "prediction_worker.prediction_worker.save_prediction"
        )
        self.mock_logger_patch = patch(
            "prediction_worker.prediction_worker.logging.getLogger"
        )

        self.mock_write_is_liked = self.mock_write_is_liked_patch.start()
        self.mock_get_prediction = self.mock_get_prediction_patch.start()
        self.mock_save_prediction = self.mock_save_prediction_patch.start()
        self.mock_logger = self.mock_logger_patch.start()

        self.addCleanup(self.mock_write_is_liked_patch.stop)
        self.addCleanup(self.mock_get_prediction_patch.stop)
        self.addCleanup(self.mock_save_prediction_patch.stop)
        self.addCleanup(self.mock_logger_patch.stop)

    def test_it_retrieves_and_saves_prediction(self):
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
