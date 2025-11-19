resource "aws_s3_bucket" "this" {
  bucket = var.bucket_name
  acl    = "private"
  versioning { enabled = true }
  server_side_encryption_configuration {
    rule {
      apply_server_side_encryption_by_default { sse_algorithm = "aws:kms" }
    }
  }
  lifecycle_rule {
    id      = "transition"
    enabled = true
    transition {
      days = 30
      storage_class = "STANDARD_IA"
    }
  }
  tags = var.tags
}
