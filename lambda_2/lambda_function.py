import json
import boto3
import os
import pandas as pd
import awswrangler as wr
import urllib
from datetime import datetime

def handler(event, context):
    source_bucket_name = os.environ['BUCKET_NAME']
    file_key = urllib.parse.unquote_plus(event['Records'][0]['s3']['object']['key'],encoding="utf-8")

    output_file_name = 'processed-csv-file'

    s3 = boto3.resource('s3')
    source_bucket = s3.Bucket(source_bucket_name)

    json_file = source_bucket.Object(file_key).get()['Body'].read().decode('utf-8')
    data = json.loads(json_file)

    flattened_data = process_json(data)

    csvdf = pd.DataFrame(flattened_data)

    csv_file_path = f's3://{source_bucket_name}/processed-csv-file.csv'
    wr.s3.to_csv(df=csvdf, path=csv_file_path, index=False)

    return {
        'statusCode': 200,
        'body': f'CSV file {output_file_name} saved in S3 bucket'
    }

def process_json(json_content):
    flattened_records = []

    for item in json_content['list']:
        location = item['location']
        latitude = None
        longitude = None

        if location == 'London':
            latitude = 51.5098
            longitude = -0.1180
        elif location == 'Paris':
            latitude = 48.8588897
            longitude = 2.3200410217200766
        elif location == 'Brussels':
            latitude = 50.8465573
            longitude = 4.351697
        elif location == 'Madrid':
            latitude = 40.4167047
            longitude = -3.7035825
        elif location == 'Budapest':
            latitude = 47.48138955
            longitude = 19.14609412691246
        elif location == 'Oslo':
            latitude = 59.97239745
            longitude = 10.775729194051895
        else:
            latitude = 0.0
            longitude = 0.0

        timestamp = datetime.fromtimestamp(item['dt']).strftime('%d/%m/%Y %H:%M:%S')
        record = {
            "Location": location,
            "Latitude": latitude,
            "Longitude": longitude,
            "Date": timestamp,
            "aqi": item['main']['aqi'],
            "co": item['components']['co'],
            "no": item['components']['no'],
            "no2": item['components']['no2'],
            "o3": item['components']['o3'],
            "so2": item['components']['so2'],
            "pm2_5": item['components']['pm2_5'],
            "pm10": item['components']['pm10'],
            "nh3": item['components']['nh3']
        }
        flattened_records.append(record)

    return flattened_records

