import json
import csv
import boto3
import os
from datetime import datetime

def handler(event, context):
    source_bucket_name = os.environ['BUCKET_NAME']
    file_key = event['Records'][0]['s3']['object']['key']

    output_file_name = 'flattened_records.csv'

    s3 = boto3.resource('s3')
    source_bucket = s3.Bucket(source_bucket_name)

    json_file = source_bucket.Object(file_key).get()['Body'].read().decode('utf-8')
    data = json.loads(json_file)

    flattened_data = process_json(data)

    with open('/tmp/flattened_records.csv', 'w', newline='') as outfile:
        writer = csv.writer(outfile)
        writer.writerow(["Date", "aqi", "co", "no", "no2", "o3", "so2", "pm2_5", "pm10", "nh3"])
        for record in flattened_data:
            date = datetime.fromtimestamp(record['dt']).strftime('%d/%m/%Y %H:%M:%S')
            writer.writerow(
                [date, record['aqi'], record['co'], record['no'], record['no2'], record['o3'], record['so2'],
                 record['pm2_5'], record['pm10'], record['nh3']])

    csv_data = '/tmp/flattened_records.csv'

    s3.upload_file(csv_data, source_bucket, output_file_name)

    return {
        'statusCode': 200,
        'body': f'CSV file {output_file_name} saved in S3 bucket'
    }

def process_json(json_content):
    flattened_records = []

    for item in json_content['list']:
        record = {
            "dt": item['dt'],
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

