from aws_cdk import (
    aws_lambda as _lambda,
    aws_s3 as s3,
    aws_s3_notifications as s3_notifications,
)
import aws_cdk as cdk

class APIdataStack(cdk.Stack):
    def __init__(self, scope: cdk.App, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        apidata_bucket = s3.Bucket(
            self,
            'APIDataBucket-Internship',
            removal_policy=cdk.RemovalPolicy.DESTROY
        )

        lambda_layer_requests = _lambda.LayerVersion(
            self,
            "RequestsLambdaLayer",
            compatible_runtimes=[_lambda.Runtime.PYTHON_3_7],
            code=_lambda.Code.from_asset("requests"),
        )

        weather_data_pull = _lambda.Function(
            self,
            'weather-data-pull',
            runtime=_lambda.Runtime.PYTHON_3_7,
            handler='lambda_function.handler',
            code=_lambda.Code.from_asset('lambda'),
            environment={
                'BUCKET_NAME': apidata_bucket.bucket_name,
                'API_ENDPOINT_1': 'http://api.openweathermap.org/data/2.5/air_pollution/history?lat=51.5098&lon=-0.1180&start'
                                '=1672531200&end=dynamic&appid=57e5f883d398a3a11dd65e86c5909df4',
                'API_ENDPOINT_2': 'http://api.openweathermap.org/data/2.5/air_pollution/history?lat=48.8588897&lon=2.3200410217200766&start'
                                '=1672531200&end=dynamic&appid=57e5f883d398a3a11dd65e86c5909df4',
                'API_ENDPOINT_3': 'http://api.openweathermap.org/data/2.5/air_pollution/history?lat=50.8465573&lon=4.351697&start'
                                '=1672531200&end=dynamic&appid=57e5f883d398a3a11dd65e86c5909df4',
                'API_ENDPOINT_4': 'http://api.openweathermap.org/data/2.5/air_pollution/history?lat=40.4167047&lon=-3.7035825&start'
                                '=1672531200&end=dynamic&appid=57e5f883d398a3a11dd65e86c5909df4',
                'API_ENDPOINT_5': 'http://api.openweathermap.org/data/2.5/air_pollution/history?lat=47.48138955&lon=19.14609412691246&start'
                                '=1672531200&end=dynamic&appid=57e5f883d398a3a11dd65e86c5909df4',
                'API_ENDPOINT_6': 'http://api.openweathermap.org/data/2.5/air_pollution/history?lat=59.97239745&lon=10.775729194051895&start'
                                '=1672531200&end=dynamic&appid=57e5f883d398a3a11dd65e86c5909df4'
            },
            layers=[lambda_layer_requests],
            timeout=cdk.Duration.minutes(5)
        )

        apidata_bucket.grant_write(weather_data_pull)

        pandas_layer_arn = 'arn:aws:lambda:ap-southeast-2:336392948345:layer:AWSSDKPandas-Python37:5'
        lambda_layer_pandas = _lambda.LayerVersion.from_layer_version_arn(
            self,
            'PandasLayer',
            pandas_layer_arn)

        convert_weather_json_to_csv = _lambda.Function(
            self,
            'convert-weather-json-to-csv',
            runtime=_lambda.Runtime.PYTHON_3_7,
            handler='lambda_function.handler',
            code=_lambda.Code.from_asset('lambda_2'),
            environment={
                'BUCKET_NAME': apidata_bucket.bucket_name
            },
            memory_size=1024,
            layers=[lambda_layer_pandas],
            timeout=cdk.Duration.minutes(5)
        )

        apidata_bucket.grant_read_write(convert_weather_json_to_csv)

        notification = s3_notifications.LambdaDestination(convert_weather_json_to_csv)
        apidata_bucket.add_event_notification(s3.EventType.OBJECT_CREATED, notification)

app = cdk.App()
APIdataStack(app, 'APIdataStack')
app.synth()
