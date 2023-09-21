import json
import sagemaker
import base64
from sagemaker.serializers import IdentitySerializer

ENDPOINT = "image-classification-2023-09-21-11-50-22-931"  

def lambda_handler(event, context):

    print("Received Event:", json.dumps(event))

    image = base64.b64decode(event["image_data"]) 

    predictor = sagemaker.predictor.Predictor(
        endpoint_name=ENDPOINT,
        serializer=IdentitySerializer("image/png")  
    )

    inferences = predictor.predict(image)  

    event["inferences"] = inferences.decode('utf-8')
    return {
        'statusCode': 200,
        'body': json.dumps(event)
    }

