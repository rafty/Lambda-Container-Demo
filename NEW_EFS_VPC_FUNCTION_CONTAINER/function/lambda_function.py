import os
import json
from pathlib import Path
import boto3

print('Loading function')


s3_client = boto3.client('s3')
bucket_name = 'demo-lambda-test-bucket-2024'
s3_object_name = 'sample.jsonl'


def get_efs_file_path(file_name):
    #------ 注意 -------------------------
    # Cloud9からEFSにアクセスするには、Cloud9にEFSをマウントしなければなりませんが、
    # Cloud9にdymmy_efsディレクトリを作成すればデバッグは可能になります。
    if 'AWS_LAMBDA_FUNCTION_NAME' in os.environ:
        print('on Lambda!!!')
        efs_file_path = f'/mnt/efs/{file_name}'
    else:
        print('on Local')
        current_script_path = Path(__file__).resolve()
        deploy_lambda_path = current_script_path.parents[2]
        efs_file_path = deploy_lambda_path / 'dummy_efs' / 'test-1.json'
    return efs_file_path


def lambda_handler(event, context):
    print('called lambda_handler!!')
    print(f'event: {json.dumps(event, indent=2)}')
    json_data = json.dumps(event)
    
    efs_file_path = get_efs_file_path(s3_object_name)

    # S3からオブジェクトを取得し、そのコンテンツをストリーミングする
    response = s3_client.get_object(Bucket=bucket_name, Key=s3_object_name)
    streaming_body = response['Body']
    # EFSにストリーミングで書き込み
    with open(efs_file_path, 'wb') as f:
        while True:
            # S3オブジェクトから10バイトずつ読み込む
            chunk = streaming_body.read(10)  # 適切なサイズにすること 例：1024など
            if not chunk:
                break
            f.write(chunk)
    
    print('Successfully processed the S3 object and written to EFS.')


    return {
        'statusCode': 200,
        'body': 'Successfully processed the S3 object and written to EFS.'
    }


# ------------- for local debug --------------------------
if __name__ == '__main__':
    
    event = {}
    context = {}
    
    response = lambda_handler(event, context)
    
    print(f'response: {response}')
    