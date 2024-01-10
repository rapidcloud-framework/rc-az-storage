resource "azurerm_redis_cache" "redis_cache" {
  name                = var.name
  location            = var.location
  resource_group_name = var.resource_group_name
  capacity            = var.capacity
  family              = var.family
  sku_name            = var.sku_name
  subnet_id           = var.sku_name == "Premium" ? var.subnet_id : null

  dynamic "identity" { # only premium sku
    for_each = var.identity_type != null || var.identity_type != "" ? ["identity"] : []

    content {
      type = var.identity_type
      identity_ids = local.is_userassigned ? var.managed_ids : null
    }
  }

  zones = var.sku_name == "Premium" ? var.zones : null

  tags = merge(local.rc_tags, var.tags)
}