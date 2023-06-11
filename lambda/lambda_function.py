import requests
import json
import boto3
import os


def handler(event, context):
    bucket_name = os.environ['BUCKET_NAME']

    api_endpoint = os.environ['API_ENDPOINT']

    response = requests.get(api_endpoint)

    if response.status_code == 200:
        data = response.json()

        json_data = json.dumps(data)

        s3_key = 'weather_data.json'

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