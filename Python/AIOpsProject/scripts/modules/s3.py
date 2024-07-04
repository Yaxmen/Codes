import boto3
import os

CLOUDFORMATION_BUCKET = "tf-dev1-aiops"

s3 = boto3.resource("s3")

excludes = (".git", ".pyc")

def upload_files(prefix):

    for root, dirs, files in os.walk("."):
        for file in files:
            path = os.path.join(root, file)[2:]
            if all(exclude not in path for exclude in excludes):
                print(f"{prefix}/{path}")
                upload_file = s3.meta.client.upload_file(
                    path, CLOUDFORMATION_BUCKET, f"{prefix}/{path}"
                )

    return True
