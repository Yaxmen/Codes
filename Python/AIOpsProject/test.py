import boto3

s3_client = boto3.client('s3')

# Upload the file to S3
s3_client.upload_file('hello.txt', 'tf-dev1-aiops', 'hello-remote.txt')

# Download the file from S3
s3_client.download_file('tf-dev1-aiops', 'hello-remote.txt', 'hello2.txt')
print(open('hello2.txt').read())

