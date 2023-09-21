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

