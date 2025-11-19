provider "aws" { region = var.region }

module "data_bucket" {
  source = "../../modules/s3-bucket"
  bucket_name = var.bucket_name
  tags = var.tags
}

module "kinesis_stream" {
  source = "../../modules/kinesis-stream"
  name = var.kinesis_stream_name
  shard_count = var.kinesis_shards
  tags = var.tags
}

module "firehose" {
  source = "../../modules/kinesis-firehose"
  name = var.firehose_name
  s3_bucket_arn = module.data_bucket.bucket_arn
  tags = var.tags
}

output "s3_bucket_name" { value = module.data_bucket.bucket_name }
output "kinesis_stream_name" { value = module.kinesis_stream.name }
output "firehose_name" { value = module.firehose.name }
