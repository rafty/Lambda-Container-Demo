import io
import os
import sys
from pathlib import Path
import json
import boto3
# ---------------------------------------------
# for open_smart install
# !! need to pip install in current directory
# pip install smart_open --target=./libs
# ---------------------------------------------
current_dir = os.path.dirname(os.path.abspath(__file__))
libs_dir = os.path.join(current_dir, 'libs')
sys.path.append(libs_dir)
from libs.smart_open import open as smart_open


print('Loading function')

s3_client = boto3.client('s3')
bucket_name = 'demo-lambda-test-bucket-2024'
jsonl_file_name = 'sample.jsonl'
jsonl_memory_file_name = 'sample-memory.jsonl'


def get_tmp_file_path(file_name: str) -> Path:
    """
    実行環境に応じて適切な一時ファイルパスを返します。
    """
    if 'AWS_LAMBDA_FUNCTION_NAME' in os.environ:
        print('on Lambda!!!')
        return Path('/tmp') / file_name
    else:
        print('on Local')
        return Path(__file__).resolve().parents[2] / 'dummy_tmp' / file_name


def create_jsonl_file(filename: Path, data, num_lines=100, in_memory=False):
    """
    一時ストレージまたはメモリ内にJSONLファイルを作成します。
    """
    if in_memory:
        with io.StringIO() as f:
            for _ in range(num_lines):
                f.write(json.dumps(data) + '\n')
            return f.getvalue()
    else:
        with open(filename, 'w', encoding='utf-8') as f:
            for _ in range(num_lines):
                f.write(json.dumps(data) + '\n')
        return str(filename)


def upload_to_s3(content, bucket_name, object_name, is_file=True):
    """
    S3にコンテンツをアップロードします。コンテンツはファイルまたはメモリ文字列からのものです。
    """
    if is_file:
        s3_client.upload_file(content, bucket_name, object_name)
    else:
        s3_client.put_object(Bucket=bucket_name, Key=object_name, Body=content)


def lambda_handler(event, context):
    print('called lambda_handler!!', json.dumps(event, indent=2))

    # ----------------------------------------------------------
    # JSONLファイルを作成してアップロード
    # ----------------------------------------------------------
    tmp_file_path = create_jsonl_file(get_tmp_file_path(jsonl_file_name), event)
    upload_to_s3(tmp_file_path, bucket_name, jsonl_file_name)

    # ----------------------------------------------------------
    # メモリ内のJSONLコンテンツを作成してアップロード
    # ----------------------------------------------------------
    memory_file_content = create_jsonl_file(None, event, in_memory=True)
    upload_to_s3(memory_file_content, bucket_name, jsonl_memory_file_name, is_file=False)

    # ----------------------------------------------------------------------
    # S3からストリーミング読み込み、処理、S3にsmart_openを使用して書き戻す
    # ----------------------------------------------------------------------
    from_s3_file_streaming_read = 'sample.jsonl'
    to_s3_file_streaming_write = f's3://{bucket_name}/sample_streaming_write.jsonl'
    

    # S3から指定されたオブジェクトを取得し、そのコンテンツをストリーミングする
    response = s3_client.get_object(Bucket=bucket_name, Key=from_s3_file_streaming_read)
    streaming_body = response['Body']
    # ストリーミングボディをテキストとして扱うためにTextIOWrapperを使用
    with io.TextIOWrapper(streaming_body, encoding='utf-8') as text_wrapper:
        # smart_openを使用して指定されたS3オブジェクトに対して書き込みモードでオープン
        with smart_open(to_s3_file_streaming_write, 'w', encoding='utf-8') as target_file:
            
            # テキストラッパーを介してストリーミングボディ
            # から1行ずつ読み取り、JSONの各行を処理する
            for line in text_wrapper:
              
                print(f'processing json line: {line}')  # ここで１行のJSONの何かしらの処理を行う
                
                target_file.write(line)  # 処理中のJSONLの1行を新しいS3オブジェクトに書き込む

    
    
    return {'statusCode': 200, 'body': {}}


if __name__ == '__main__':
    event = {"key1": 1, "key2": 2, "key3": 3}
    context = {}
    response = lambda_handler(event, context)
    print(f'response: {response}')
