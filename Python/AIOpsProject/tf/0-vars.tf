

variable "region" {
 description = "AWS region for hosting our your network"
 default = "us-east-1"
}

variable "vpc_cidr" {
  default = "10.0.0.0/16"
}

# Defining CIDR Block for Subnet
variable "subnet1_cidr" {
  default = "10.0.1.0/24"
}