locals {
  is_premium    = var.sku_name == "Premium"
  is_userassigned = length(regexall("UserAssigned", var.identity_type)) > 0
  rc_tags = {
    Name        = var.name
    profile     = var.profile
    author      = "rapid-cloud"
  }
}