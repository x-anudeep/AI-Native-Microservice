# Terraform

This directory provisions the AWS shape for the platform:

- VPC, subnets, internet gateway, routes, and security group.
- EKS control plane and managed node group sized for 2 to 6 nodes.
- IAM roles and managed policy attachments for cluster and worker nodes.

```bash
terraform init
terraform plan
terraform apply
```

The files are intentionally provider-native so the resource graph is easy to inspect in interviews and code reviews.
