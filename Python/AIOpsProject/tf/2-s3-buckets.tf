locals {
    bucket_tags = {
        Name        = "tf-dev1-aiops"
        Environment = "dev"
        Terraform   = "yes"
      }
  }


resource "aws_s3_bucket" "tf-dev1-aiops" {
  bucket = "tf-dev1-aiops"
  tags   = local.bucket_tags
}
