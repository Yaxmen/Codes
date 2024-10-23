# resource "aws_iam_role" "aiops_emr_service_role" {
#   name = "emr_service_role"

#   assume_role_policy = <<EOF
# {
#   "Version": "2008-10-17",
#   "Statement": [
#     {
#       "Effect": "Allow",
#       "Principal": {
#         "Service": "elasticmapreduce.amazonaws.com"
#       },
#       "Action": "sts:AssumeRole"
#     }
#   ]
# }
# EOF

#   managed_policy_arns = ["arn:aws:iam::aws:policy/service-role/AmazonElasticMapReduceRole"]
# }


# # Define the EC2 instance profile
# resource "aws_iam_role" "aiops_emr_ec2_instance_role" {
#   name = "emr_ec2_instance_role"

#   assume_role_policy = <<EOF
# {
#   "Version": "2008-10-17",
#   "Statement": [
#     {
#       "Effect": "Allow",
#       "Principal": {
#         "Service": "ec2.amazonaws.com"
#       },
#       "Action": "sts:AssumeRole"
#     }
#   ]
# }
# EOF
# }


# resource "aws_iam_role_policy_attachment" "emr_ec2_instance_role_policy_attachment" {
#   role       = aws_iam_role.aiops_emr_ec2_instance_role.name
#   policy_arn = "arn:aws:iam::aws:policy/AmazonElasticMapReduceFullAccess"
# }

# resource "aws_iam_instance_profile" "emr_instance_profile" {
#   name = "emr_instance_profile"
#   role = aws_iam_role.aiops_emr_ec2_instance_role.name
# }



# resource "aws_emr_cluster" "example_cluster" {
#   name           = "Example Cluster"
#   release_label  = "emr-6.5.0"
#   applications   = ["Spark", "Hadoop"]
#   service_role   = aws_iam_role.aiops_emr_service_role.arn

#   ec2_attributes {
#     instance_profile = aws_iam_instance_profile.emr_instance_profile.arn
#   }

#   master_instance_group {
#     instance_type = "m5.xlarge"
#   }

#   core_instance_group {
#     instance_type  = "m5.xlarge"
#     instance_count = 1
#   }
# }