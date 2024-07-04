# # VPC Criation
# resource "aws_vpc" "aiops_vpc" {
#   cidr_block            = "${var.vpc_cidr}"
#   instance_tenancy      = "default"
#   enable_dns_support    = "true"
#   enable_dns_hostnames  = "true"

#   tags = {
#     Name = "aiops_project"
#   }
# }

# # Criação do Internet Gateway
# resource "aws_internet_gateway" "aiops_vpc_igw" {
#   vpc_id = aws_vpc.aiops_vpc.id

#   tags = {
#     Name = "aiops_project"
#   }
# }

# # Criação das subnets Publicas
# resource "aws_subnet" "public_subnet_us_east_1a" {
#   vpc_id                  = aws_vpc.aiops_vpc.id
#   cidr_block              = "${var.subnet1_cidr}"
#   availability_zone       = "us-east-1a"
#   map_public_ip_on_launch = true

#   tags = {
#     Name = "aiops_project"
#   }
# }

# # Criação da Tabela de Roteamento
# resource "aws_route_table" "aiops_vpc_public_table" {
#   vpc_id = "${aws_vpc.aiops_vpc.id}"

#   route {
#     cidr_block = "0.0.0.0/0"
#     gateway_id = "${aws_internet_gateway.aiops_vpc_igw.id}"
#   }

#   tags = {
#     Name = "aiops_project"
#   }
# }


# #Associação da Subnet Pública com a Tabela de Roteamento
# resource "aws_route_table_association" "public_us_eas_1a" {
#   subnet_id      = "${aws_subnet.public_subnet_us_east_1a.id}"
#   route_table_id = "${aws_route_table.aiops_vpc_public_table.id}"
# }