import requests
import json
import boto3
import os
from datetime import datetime

def handler(event, context):
    bucket_name = os.environ['BUCKET_NAME']
    api_endpoint = os.environ['API_ENDPOINT']

    latitudes = [51.5098, 48.8588897, 50.8465573, 40.4167047, 47.48138955, 59.97239745]
    longitudes = [-0.1180, 2.3200410217200766, 4.351697, -3.7035825, 19.14609412691246, 10.775729194051895]

    current_timestamp = int(datetime.now().timestamp())

    response_data = []

    for i in range(len(latitudes)):
        lat = latitudes[i]
        lon = longitudes[i]
        endpoint = api_endpoint.format(lat=lat, lon=lon).replace('end=dynamic', f'end={current_timestamp}')

        response = requests.get(endpoint)
        if response.status_code == 200:
            response_data.append(response.json())
        else:
            return {
                'statusCode': 500,
                'body': 'Failed to fetch data from API'
            }

    locations = ["London", "Paris", "Brussels", "Madrid", "Budapest", "Oslo"]

    for i in range(len(response_data)):
        data = response_data[i]
        for item in data["list"]:
            item["location"] = locations[i]

    merged_data = {
        'coord': response_data[0]['coord'],
        'list': [item for data in response_data for item in data['list']]
    }

    json_data = json.dumps(merged_data)

    current_datetime = datetime.now().strftime("%Y-%m-%d-%H:%M:%S")
    s3_key = f'weather_data_{current_datetime}.json'

    s3 = boto3.resource('s3')
    s3.Object(bucket_name, s3_key).put(Body=json_data)

    return {
        'statusCode': 200,
        'body': 'Data stored in S3 bucket'
    }
