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
  description = "The name of the redis cache"
}

variable "capacity" {
  type        = string
  description = "The capacity value describes the capacity of storage"
}


variable "family" {
  type        = string
  description = "the unique name describes which family of storage it is"
}

variable "sku_name" {
  type        = string
  description = "the unique name describes which family of storage it is"
}

variable "subnet_id" {
  type = string
}


variable "zones" {
  type = list(string)
}

variable "identity_type" {
  type = string
}

variable "managed_ids" {
  type = list(string)
  default = []
}

variable "tags" {
    type = map(string)
    default = {}
}