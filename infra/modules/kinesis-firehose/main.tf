resource "aws_iam_role" "firehose_role" {
  name = "${var.name}-firehose-role"
  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{ Action="sts:AssumeRole", Effect="Allow", Principal={ Service="firehose.amazonaws.com" } }]
  })
}

resource "aws_iam_role_policy" "firehose_policy" {
  name = "${var.name}-policy"
  role = aws_iam_role.firehose_role.id
  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      { Action = ["s3:PutObject","s3:PutObjectAcl"], Effect="Allow", Resource = ["${var.s3_bucket_arn}/*"] },
      { Action = ["logs:CreateLogGroup","logs:CreateLogStream","logs:PutLogEvents"], Effect="Allow", Resource = "*" }
    ]
  })
}

resource "aws_kinesis_firehose_delivery_stream" "this" {
  name = var.name
  destination = "s3"
  s3_configuration {
    role_arn = aws_iam_role.firehose_role.arn
    bucket_arn = var.s3_bucket_arn
    prefix = "raw/!{partitionKey}/"
    buffering_size = 5
    buffering_interval = 60
    compression_format = "GZIP"
  }
}
