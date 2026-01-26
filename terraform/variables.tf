variable "aws_region" {
  description = "AWS region for the platform."
  type        = string
  default     = "us-east-1"
}

variable "project_name" {
  description = "Name used to label AWS resources."
  type        = string
  default     = "ai-native-microservice"
}

variable "cluster_node_count" {
  description = "Desired EKS managed node count."
  type        = number
  default     = 2
}
