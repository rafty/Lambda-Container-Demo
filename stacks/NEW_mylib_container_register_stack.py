import os
from constructs import Construct
import aws_cdk as cdk
from aws_cdk import Duration
from aws_cdk import Stack
from aws_cdk import aws_lambda
from aws_cdk import aws_ecr
from aws_cdk import aws_ecr_assets
# import cdk_ecr_deployment



class RegisterLibToEcrStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # DockerImageAssetを使用してDockerfile-libからECRにイメージを登録
        mylib_image = aws_ecr_assets.DockerImageAsset(self, "MyLibContainerDockerImageToTempRepository",
            directory=os.path.join(os.path.dirname(__file__), "../NEW_REGISTER_FUNCTION_MYLIB_CONTAINER/function"),
            file="Dockerfile.mylib"  # Dockerfileの名前を指定。デフォルトは 'Dockerfile'
        )
