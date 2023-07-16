from aws_cdk import (
    aws_lambda as _lambda,
    aws_s3 as s3,
    aws_s3_notifications as s3_notifications,
    aws_secretsmanager as secretsmanager,
    aws_events as events,
    aws_events_targets as targets,
)
import aws_cdk as cdk

class APIdataStack(cdk.Stack):
    def __init__(self, scope: cdk.App, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        secret_name = "internship/apikey"
        secret_key = "appid"
        secret_value = secretsmanager.Secret.from_secret_name_v2(
            self, 'SecretValue', secret_name
        ).secret_value_from_json(secret_key).to_string()

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
                'API_ENDPOINT': f'http://api.openweathermap.org/data/2.5/air_pollution/history?lat={{lat}}&lon={{lon}}&start'
                                f'=1672531200&end=dynamic&appid={secret_value}'
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

        schedule_expression = 'cron(0 0 * * ? *)'

        rule = events.Rule(
            self,
            'WeatherDataPullSchedule',
            schedule=events.Schedule.expression(schedule_expression)
        )

        rule.add_target(
            targets.LambdaFunction(weather_data_pull)
        )

        apidata_bucket.grant_read_write(convert_weather_json_to_csv)

        notification = s3_notifications.LambdaDestination(convert_weather_json_to_csv)
        apidata_bucket.add_event_notification(s3.EventType.OBJECT_CREATED, notification)

app = cdk.App()
APIdataStack(app, 'APIdataStack')
app.synth()
