import os
from constructs import Construct
import aws_cdk as cdk
from aws_cdk import Duration
from aws_cdk import Stack
from aws_cdk import aws_lambda
from aws_cdk import aws_s3
from aws_cdk import aws_efs
from aws_cdk import aws_ec2
from aws_cdk import aws_iam


class CreateFunctionEfsS3ContainerImageStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # 既存のVPCを取得
        vpc = aws_ec2.Vpc.from_lookup(self, "ExistingVPC",
                                      vpc_name='Cloud9')


        # EFSファイルシステムの作成
        file_system = aws_efs.FileSystem(self, "Cloud9VpcfsFileSystem",
                                         vpc=vpc,
                                         removal_policy=cdk.RemovalPolicy.DESTROY)
        # EFSアクセスポイントの作成
        access_point = file_system.add_access_point("AccessPoint",
                                                    path="/lambda_tmp",
                                                    create_acl=aws_efs.Acl(owner_uid="1001", owner_gid="1001", permissions="750"),
                                                    posix_user=aws_efs.PosixUser(uid="1001", gid="1001"))


        # container imageを作成する
        lambda_container = aws_lambda.DockerImageCode.from_image_asset(
            directory=os.path.join(os.path.dirname(__file__), "../NEW_EFS_VPC_FUNCTION_CONTAINER"),
            file='Dockerfile.function')

        # DockerイメージからLambda関数を作成
        lambda_function = aws_lambda.DockerImageFunction(self, "AwsLambdaEfsVpcContainerImageFunction",
                                                         vpc=vpc,  #  VPC Lambdaにする。
                                                         function_name='demo_efs_streaming_container_lambda',
                                                         code=lambda_container,
                                                         filesystem=aws_lambda.FileSystem.from_efs_access_point(access_point, '/mnt/efs'))

        # AmazonS3FullAccessマネージドポリシーをLambda関数のロールにアタッチ
        lambda_function.role.add_managed_policy(
            aws_iam.ManagedPolicy.from_aws_managed_policy_name("AmazonS3FullAccess")
        )

        # # S3への読み書きアクセスを許可するポリシーステートメントの作成
        # policy_statement = aws_iam.PolicyStatement(
        #     actions=[
        #         "s3:GetObject",     # オブジェクトの読み取り
        #         "s3:PutObject",     # オブジェクトの書き込み
        #         "s3:DeleteObject",  # オブジェクトの削除
        #         "s3:ListBucket"     # バケット内のオブジェクトリスト取得
        #     ],
        #     # resources=["arn:aws:s3:::*/*"],  # すべてのS3バケットとオブジェクトに対する権限
        #     resources=[
        #         "arn:aws:s3:::demo-lambda-test-bucket-2024",       # 指定されたバケットに対する権限
        #         "arn:aws:s3:::demo-lambda-test-bucket-2024/*"      # 指定されたバケット内のすべてのオブジェクトに対する権限
        #     ],  # すべてのS3バケットとオブジェクトに対する権限
        # )
        # # ポリシーステートメントをLambda関数のロールにアタッチ
        # lambda_function.add_to_role_policy(policy_statement)
