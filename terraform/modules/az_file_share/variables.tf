variable "profile" {}
variable "env" {}
variable "workload" {}
variable "cmd_id" {}

variable "name" {
  type    = string
  description = "The name of the shared file"
}

variable "quota" {
  type        = string
  description = "The capacity value describes the capacity of file share"
  default = "50"
}


variable "storage_account_name" {
  type        = string
  description = "the unique name describes which family of storage account it belongs to"
}
