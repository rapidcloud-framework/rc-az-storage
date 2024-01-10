
variable "profile" {}
variable "env" {}
variable "workload" {}
variable "cmd_id" {}

variable "resource_group_name" {
  type = string
  description = "Name of resource group to deploy virtual network in."
}

variable "location" {
  type    = string
  description = "The location where the subnet will be created"
}

variable "name" {
  type    = string
  description = "The name of the storage account"
}

variable "access_tier" {
  type        = string
  description = "The tier of access"
}


variable "account_replication_type" {
  type        = string
  description = "the replication_type of the storage acc"
}

variable "ip_addresses" {
  type = list(string)
  default = []
}

variable "subnet_ids" {
  type = list(string)
  default = []
}

variable "tags" {
    type = map(string)
    default = {}
}