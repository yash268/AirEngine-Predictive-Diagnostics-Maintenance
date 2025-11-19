import joblib, os, json
MODEL_PATH = "/opt/ml/model/rul_model.pkl"

if os.path.exists(MODEL_PATH):
    model = joblib.load(MODEL_PATH)
else:
    model = None

def predict(features_dict):
    # features_dict: keys are feature names in sorted order
    keys = sorted(features_dict.keys())
    X = [features_dict[k] for k in keys]
    return float(model.predict([X])[0])

# Example Lambda-style handler (for local testing)
def handler(event, context):
    body = event.get('body') or event
    if isinstance(body, str):
        body = json.loads(body)
    pred = predict(body)
    return {'statusCode':200, 'body': json.dumps({'predicted_rul': pred})}
