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

        lambda_layer = _lambda.LayerVersion(
            self,
            "RequestsLambdaLayer",
            compatible_runtimes=[_lambda.Runtime.PYTHON_3_7],
            code=_lambda.Code.from_asset("requests"),
        )

        lambda_function = _lambda.Function(
            self,
            'APIDataLambda',
            runtime=_lambda.Runtime.PYTHON_3_7,
            handler='lambda_function.handler',
            code=_lambda.Code.from_asset('lambda'),
            environment={
                'BUCKET_NAME': apidata_bucket.bucket_name,
                'API_ENDPOINT': 'http://api.openweathermap.org/data/2.5/air_pollution/history?lat=51.5098&lon=-0.1180&start'
                                '=1606266000&end=dynamic&appid=57e5f883d398a3a11dd65e86c5909df4'
            },
            layers=[lambda_layer],
            timeout=cdk.Duration.minutes(5)
        )

        apidata_bucket.grant_write(lambda_function)

        second_lambda_function = _lambda.Function(
            self,
            'FlattenJsontoCSV',
            runtime=_lambda.Runtime.PYTHON_3_7,
            handler='lambda_function.handler',
            code=_lambda.Code.from_asset('lambda_2'),
            environment={
                'BUCKET_NAME': apidata_bucket.bucket_name
            },
            timeout=cdk.Duration.minutes(5)
        )

        apidata_bucket.grant_read_write(second_lambda_function)

        s3_notifications.LambdaDestination(second_lambda_function).bind(apidata_bucket).bucket.add_event_notification(
            s3.EventType.OBJECT_CREATED,
            s3_notifications.S3EventLambdaDestination(second_lambda_function)
        )

app = cdk.App()
APIdataStack(app, 'APIdataStack')
app.synth()
