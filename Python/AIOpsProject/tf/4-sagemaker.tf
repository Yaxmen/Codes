resource "aws_iam_role" "sagemaker_role" {
    name = "sagemaker_role"

    assume_role_policy = jsonencode({
        Version = "2012-10-17"
        Statement = [{
            Action = [
                "sts:AssumeRole"
            ]
            Effect = "Allow"
            Principal = {
                Service = "sagemaker.amazonaws.com"
            }

        }]
    })
}
resource "aws_iam_policy" "sagemaker_s3_access" {
    name        = "sagemaker_s3_access"
    description = "Permite ao SageMaker acessar buckets S3 específicos"

    policy = jsonencode({
        Version = "2012-10-17"
        Statement = [{
            Action = [
                "s3:GetObject",
                "s3:ListBucket"
            ]
            Effect = "Allow"
            Resource = [
                "arn:aws:s3:::tf-dev1-aiops",
                "arn:aws:s3:::tf-dev1-aiops/",
                "arn:aws:s3:::tf-dev1-aiops/*"
            ]
        }]
    })
}


resource "aws_sagemaker_notebook_instance" "sagemaker_notebook_instance" {
    
    name            = "sagemaker-notebook-instance" 
    role_arn        = aws_iam_role.sagemaker_role.arn
    instance_type   = "ml.t2.medium"
}

resource "aws_iam_policy_attachment" "sagemaker_policy_attachment" {
    name    = "sagemaker-full-access"
    roles   = [
        aws_iam_role.sagemaker_role.name,
        ]
    policy_arn = "arn:aws:iam::aws:policy/AmazonSageMakerFullAccess"
}


resource "aws_iam_role_policy_attachment" "sagemaker_s3_policy_attachment" {
    role       = aws_iam_role.sagemaker_role.name
    policy_arn = aws_iam_policy.sagemaker_s3_access.arn
}

