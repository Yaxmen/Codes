resource "aws_security_group" "aiops_sg_sage_maker" {
  name        = "aiops_sg_sage_maker"
  description = "Security Group to SageMaker"
  vpc_id      = "vpc-e6cfb69c"


	# HTTPS access to postgre 2
	ingress {
		description = "Allow all inbound for SageMaker"
		from_port   = 0
		to_port     = 0
		protocol    = "-1"
		cidr_blocks = ["0.0.0.0/0"]
	}


	# Internet access to anywhere
	egress {
		from_port   = 0
		to_port     = 0
		protocol    = "-1"
		cidr_blocks = ["0.0.0.0/0"]
  }

  tags = {
    Name = "aiops_project"
  }
}



resource "aws_security_group" "aiops_sg_emr" {
  name        = "aiops_sg_emr"
  description = "Allow inbound traffic"
  vpc_id      = "vpc-e6cfb69c"

  ingress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["172.31.0.0/16"]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  lifecycle {
    ignore_changes = [
      ingress,
      egress,
    ]
  }

  tags = {
    Name = "aiops_project"
  }
}
