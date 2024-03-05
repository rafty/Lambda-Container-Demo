#!/usr/bin/env python3

import os
import aws_cdk as cdk

from stacks.NEW_mylib_container_register_stack import RegisterLibToEcrStack
from stacks.NEW_Func_container_register_stack import CreateFunctionContainerImageStack
from stacks.NEW_EFS_VPC_lambda_container_stack import CreateFunctionEfsS3ContainerImageStack


app = cdk.App()

env = cdk.Environment(
    account=os.environ.get("CDK_DEPLOY_ACCOUNT", os.environ["CDK_DEFAULT_ACCOUNT"]),
    region=os.environ.get("CDK_DEPLOY_REGION", os.environ["CDK_DEFAULT_REGION"]),
)


# Smart_openのコンテナイメージ
# 注意!! このstackはマルチスタックで動作させないこと!! シングルStackに変更して使用してください。
# RegisterLibToEcrStack(app, 'RegisterLibToEcrStack', env=env)

# Smart_openのコンテナイメーをマルチステージで持つLambda Functionの作成
CreateFunctionContainerImageStack(app, 'CreateFunctionContainerImageStack', env=env)


# EFSをマウントするVPC Lambda Function Container Imageの作成
CreateFunctionEfsS3ContainerImageStack(app, 'CreateFunctionEfsS3ContainerImageStack', env=env)


app.synth()
