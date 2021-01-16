terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 3.0"
    }
  }
}

# Configure the AWS Provider
provider "aws" {
  region = "us-east-1"
  shared_credentials_file = "secrets""
  access_key = "my-access-key"
  secret_key = "my-secret-key"
}

#Ubuntu 20.04 AMI = ami-0885b1f6bd170450c

resource "aws_instance" "ELK" {
  ami           = "ami-0885b1f6bd170450c"
  instance_type = "t2.micro"
  volume_size = "30"
}
