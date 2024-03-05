import os
from constructs import Construct
import aws_cdk as cdk
from aws_cdk import Duration
from aws_cdk import Stack
from aws_cdk import aws_lambda
from aws_cdk import aws_ecr
from aws_cdk import aws_ecr_assets
from aws_cdk import aws_s3
# from aws_cdk import aws_s3_deployment


# import cdk_ecr_deployment



class CreateFunctionContainerImageStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)


        # S3 Bucketの作成
        s3_bucket = aws_s3.Bucket(self, 'DebugLambdaBucket',
            bucket_name='demo-lambda-test-bucket-2024',
            versioned=True,
            removal_policy=cdk.RemovalPolicy.DESTROY,
            auto_delete_objects=True,
        )


        # container imageを作成する
        lambda_container = aws_lambda.DockerImageCode.from_image_asset(
            directory=os.path.join(os.path.dirname(__file__), "../NEW_REGISTER_FUNCTION_MYLIB_CONTAINER"),
            file='Dockerfile.function')

        # Container Image Lambdaの作成
        lambda_function = aws_lambda.DockerImageFunction(self, "S3StreamingLambdaContainerImageDeploy",
                                                         function_name='demo_s3_streaming_container_lambda',
                                                         code=lambda_container)
        s3_bucket.grant_read_write(lambda_function)
