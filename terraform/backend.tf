terraform {
  backend "s3" {
    bucket         = "gokul-eks-tfstate"
    key            = "eks-ops-platform/terraform.tfstate"
    region         = "ap-south-1"
    dynamodb_table = "terraform-lock"
    encrypt        = true
  }
}