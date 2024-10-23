from modules import validate_stacks, upload_files

import os
import json
import boto3
import argparse

script_path = os.path.dirname(os.path.realpath(__file__))
os.chdir(script_path + "/../")

CLOUDFORMATION_BUCKET = "tf-dev1-aiops"

cloudformation = boto3.client("cloudformation")


def prepare_build(env, operation):
    print("Starting prepare to build stack\n\n")
    if operation == "update":
        build_stack = cloudformation.update_stack
    elif operation == "create":
        build_stack = cloudformation.create_stack
    else:
        return False
    
    print("Starting validate stacks \n")
    response = validate_stacks()
    if response is None:
        print("Failed validating stacks")
        print("Build canceled")
        return False
    
    ## Folder where stack files will be uploaded
    prefix = f"{env}/infra"

    print("Starting to upload stack files\n")
    response = upload_files(prefix)
    if response is None:
        print("Failed uploading files in S3")
        print("Build canceled")
        return False

    print("Starting stack update\n")
    ##with open(f"env-{env}.json", "r") as file:
     ##   envs = json.load(file)

    response = build_stack(
        StackName=f"{env}-aiops-infra",
        TemplateURL=f"https://s3.amazonaws.com/{CLOUDFORMATION_BUCKET}/{prefix}/main.yml",  ##################
        ## Parameters=envs,
        Capabilities=[
            "CAPABILITY_NAMED_IAM",
        ],
    )

    print(f"Started build http://console.aws.amazon.com/cloudformation/home?region=us-east-1#/stacks/stackinfo?filteringStatus=active&filteringText=&viewNested=false&hideStacks=false&stackId={response.get('StackId')}")
    return True


if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument("-e", "--env", help="Select env")
    parser.add_argument("-o", "--operation", help="Select create/update")
    parser.add_argument("-c", "--confirm", help="Input Yes if you really want to build prd")

    args = parser.parse_args()

    env = args.env
    if env is None or env not in ["dev", "prd"]:
        exit()

    confirm = args.confirm
    if env == "prd" and confirm != "Yes":
        print("Confirm build in PRD")
        exit()

    operation = args.operation
    if operation is None or operation not in ["update", "create"]:
        exit()

    res = prepare_build(env, operation)
    exit(res)
