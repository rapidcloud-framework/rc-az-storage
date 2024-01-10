variable "profile" {}
variable "env" {}
variable "workload" {}
variable "cmd_id" {}

variable "name" {
  type    = string
  description = "The name of the storage container "
}

variable "storage_account_name" {
  type        = string
  description = "the unique name describes which storage account to bind with"
}

variable "container_access_type" {
  type        = string
  description = "the unique access type of storage it is"
}