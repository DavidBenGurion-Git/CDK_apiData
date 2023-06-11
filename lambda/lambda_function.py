import requests
import json
import boto3
import os


def handler(event, context):
    # Get the S3 bucket name from the environment variable
    bucket_name = os.environ['BUCKET_NAME']

    # Get the API endpoint from the environment variable
    api_endpoint = os.environ['API_ENDPOINT']

    # Make a request to the API endpoint
    response = requests.get(api_endpoint)

    # Check if the request was successful
    if response.status_code == 200:
        data = response.json()

        # Convert the data to JSON string
        json_data = json.dumps(data)

        # Generate a unique key for the S3 object
        s3_key = 'weather_data.json'

        # Upload the data to the S3 bucket
        s3 = boto3.resource('s3')
        s3.Object(bucket_name, s3_key).put(Body=json_data)

        return {
            'statusCode': 200,
            'body': 'Data stored in S3 bucket'
        }
    else:
        return {
            'statusCode': response.status_code,
            'body': 'Failed to fetch data from API'
        }