resource "azurerm_storage_account" "azure_storage_acc" {
  name                     = var.name
  resource_group_name      = var.resource_group_name
  location                 = var.location
  account_tier             = var.access_tier
  account_replication_type = var.account_replication_type

  dynamic "network_rules" {
    for_each = length(var.ip_addresses) > 0 || length(var.subnet_ids) > 0 ? ["network_rules"] : []

    content {
      default_action              = "Deny"
      ip_rules                    = var.ip_addresses
      virtual_network_subnet_ids  = var.subnet_ids
    }   
  }

  tags = merge(local.rc_tags, var.tags)

}

output "id" {
  value = azurerm_storage_account.azure_storage_acc.id
}