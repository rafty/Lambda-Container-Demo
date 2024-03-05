# AWS Lambda function container image の デバッグ デモ


# S3 Streaming ReadWrite Lambda Function

`./NEW_REGISTER_FUNCTION_MYLIB_CONTAINER/`
S3 Streaming read writeを実現するコード  

# From S3 to EFS Streaming Lambda Function

`./NEW_EFS_VPC_FUNCTION_CONTAINER/`
S3 Streaming read し EFSへStreaming Writeするコード  

# AWS CDK

`./NEW_REGISTER_FUNCTION_MYLIB_CONTAINER/`
`./NEW_EFS_VPC_FUNCTION_CONTAINER/`

上記以外のコードは、AWS CDK pythonのコードで、以下のリソースを作成するためのものです。

- AWS Lambda function container image
- ECR repository
- EFS
- S3 bucket
- Docker Image

## 注意事項

### 動作保証
- デモのために突貫で作成したため動作保証はいたしかねます。

### Dockerコマンド推奨
AWS Lambda function container imageのためのDocker Imageを作成する際、 AWS CDKによりDocker Imageを作成しています。通常の使い方とは異なりますので、 Dockerコマンドを使用してDocker Imageを作成することを推奨します。