variable "aws_region" {
  description = "The AWS region to create resources in."
  default     = "us-east-1"
}

variable "bucket_name" {
  description = "The name of the S3 bucket to create."
  default     = "my-saas-app-bucket"
}
