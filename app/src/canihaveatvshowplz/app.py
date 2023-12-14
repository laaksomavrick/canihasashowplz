import joblib
import json

model_file = "/opt/ml/model"
model = joblib.load(model_file)


def lambda_handler(event, context):
    body = event["body"]
    print(body)

    # The Wire, DS9, The Sopranos
    prediction = model.predict(["365563,9c7a19bc-6f54-4d21-b6b6-0606e29fbba3", "447316,8c0ebcc3-fbf7-4a67-8c3e-85f13de11f8e"])

    return {
        "statusCode": 200,
        "body": json.dumps(
            {
                "prediction": prediction,
            }
        ),
    }
