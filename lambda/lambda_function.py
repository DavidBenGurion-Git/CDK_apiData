import requests
import json
import boto3
import os
from datetime import datetime

def handler(event, context):
    bucket_name = os.environ['BUCKET_NAME']

    api_endpoint_1 = os.environ['API_ENDPOINT_1']
    api_endpoint_2 = os.environ['API_ENDPOINT_2']
    api_endpoint_3 = os.environ['API_ENDPOINT_3']
    api_endpoint_4 = os.environ['API_ENDPOINT_4']
    api_endpoint_5 = os.environ['API_ENDPOINT_5']
    api_endpoint_6 = os.environ['API_ENDPOINT_6']

    current_timestamp = int(datetime.now().timestamp())

    api_endpoint_1 = api_endpoint_1.replace('end=dynamic', f'end={current_timestamp}')
    api_endpoint_2 = api_endpoint_2.replace('end=dynamic', f'end={current_timestamp}')
    api_endpoint_3 = api_endpoint_3.replace('end=dynamic', f'end={current_timestamp}')
    api_endpoint_4 = api_endpoint_4.replace('end=dynamic', f'end={current_timestamp}')
    api_endpoint_5 = api_endpoint_5.replace('end=dynamic', f'end={current_timestamp}')
    api_endpoint_6 = api_endpoint_6.replace('end=dynamic', f'end={current_timestamp}')

    response_1 = requests.get(api_endpoint_1)
    response_2 = requests.get(api_endpoint_2)
    response_3 = requests.get(api_endpoint_3)
    response_4 = requests.get(api_endpoint_4)
    response_5 = requests.get(api_endpoint_5)
    response_6 = requests.get(api_endpoint_6)

    if (response_1.status_code == 200 and response_2.status_code == 200 and
        response_3.status_code == 200 and response_4.status_code == 200 and
        response_5.status_code == 200 and response_6.status_code == 200):
        data_1 = response_1.json()
        data_2 = response_2.json()
        data_3 = response_3.json()
        data_4 = response_4.json()
        data_5 = response_5.json()
        data_6 = response_6.json()

        for item in data_1["list"]:
            item["location"] = "London"

        for item in data_2["list"]:
            item["location"] = "Paris"

        for item in data_3["list"]:
            item["location"] = "Brussels"

        for item in data_4["list"]:
            item["location"] = "Madrid"

        for item in data_5["list"]:
            item["location"] = "Budapest"

        for item in data_6["list"]:
            item["location"] = "Oslo"

        merged_data = {
            'coord': data_1['coord'],
            'list': data_1['list'] + data_2['list'] + data_3['list'] + data_4['list'] + data_5['list'] + data_6['list']
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
    else:
        return {
            'statusCode': 500,
            'body': 'Failed to fetch data from API'
        }