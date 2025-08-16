# Create a resource group
resource "azurerm_resource_group" "this" {
  name     = local.rg.name
  location = local.rg.location
  tags     = local.tags
}

resource "azurerm_storage_account" "batch_storage" {
  name                     = local.storage_acc.name
  resource_group_name      = azurerm_resource_group.this.name
  location                 = azurerm_resource_group.this.location
  account_tier             = local.storage_acc.tier
  account_replication_type = local.storage_acc.replication
  tags                     = local.tags
}

resource "azurerm_role_assignment" "openai_storage_blob_contributor" {
  scope                = azurerm_storage_account.batch_storage.id
  role_definition_name = "Storage Blob Data Contributor"
  principal_id         = azurerm_cognitive_account.openai.identity[0].principal_id
}

resource "azurerm_cognitive_account" "openai" {
  name                  = local.oai.name
  custom_subdomain_name = local.oai.custom_subdomain_name
  location              = azurerm_resource_group.this.location
  resource_group_name   = azurerm_resource_group.this.name
  kind                  = "OpenAI"
  sku_name              = "S0"
  tags                  = local.tags
  identity {
    type = "SystemAssigned"
  }
}

resource "azurerm_cognitive_deployment" "gpt4o_mini" {
  name                 = "gpt-4o-mini-batch"
  cognitive_account_id = azurerm_cognitive_account.openai.id
  model {
    format  = "OpenAI"
    name    = "gpt-4o-mini"
    version = "2024-07-18"
  }
  sku {
    name     = "GlobalBatch"
    capacity = 1 # 1K tokens per minute
  }
}

resource "azurerm_storage_container" "batch_input" {
  for_each              = local.storage_acc.containers
  name                  = each.value
  storage_account_name  = azurerm_storage_account.batch_storage.name
  container_access_type = "private"
}

# Role assignment for the storage account for the User or Identity that will upload files
resource "azurerm_role_assignment" "user_openai_storage_blob_contributor" {
  scope                = azurerm_storage_account.batch_storage.id
  role_definition_name = "Storage Blob Data Contributor"
  principal_id         = var.executor_object_id
}

# Role assignment for the cognitive OpenAI resource for the User or Identity 
# that will create the batch job
resource "azurerm_role_assignment" "user_openai_congnitive_data_contributor" {
  scope                = azurerm_cognitive_account.openai.id
  role_definition_name = "Cognitive Services Data Contributor (Preview)"
  principal_id         = var.executor_object_id
}