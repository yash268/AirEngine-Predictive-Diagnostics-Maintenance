variable "name" { type = string }
variable "shard_count" { type = number }
variable "retention_hours" { type = number default = 24 }
variable "tags" { type = map(string) default = {} }
