import boto3
from pathlib import Path

client = boto3.client("cloudformation")


def validate_stacks():
    stacks = [str(path) for path in Path(".").rglob("*.yml")]

    for path in stacks:
        print("-------->")
        print(f"Validating {path}")
        try:
            with open(path, "r") as f:
                response = client.validate_template(TemplateBody=f.read())
            print(f"Stack ok {path}")
            print("<--------/n")
        except Exception as e:
            print(e)
            print("<--------/n")
            return None
    return True
