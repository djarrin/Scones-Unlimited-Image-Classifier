# serializeImageData Function

import json
import boto3
import base64

s3 = boto3.client('s3')

def lambda_handler(event, context):
    """A function to serialize target data from S3"""

    key = event['s3_key']  
    bucket = event['s3_bucket']  

    s3.download_file(bucket, key, '/tmp/image.png')

    with open("/tmp/image.png", "rb") as f:
        image_data = base64.b64encode(f.read()).decode('utf-8')

    print("Event:", event.keys())
    return {
        'statusCode': 200,
        'body': {
            "image_data": image_data,
            "s3_bucket": bucket,
            "s3_key": key,
            "inferences": []
        }
    }

# dataClassifier function

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



# outlierFilter function
import json

THRESHOLD = 0.93  # Adjust this threshold as needed (between 1.00 and 0.000)

def lambda_handler(event, context):
    try:
        inferences = json.loads(event["inferences"])

        meets_threshold = any(value >= THRESHOLD for value in inferences)

        if meets_threshold:
            return {
                'statusCode': 200,
                'body': json.dumps(event)
            }
        else:
            raise Exception("THRESHOLD_CONFIDENCE_NOT_MET")
    except Exception as e:
        return {
            'statusCode': 500,  
            'body': str(e)  
        }

