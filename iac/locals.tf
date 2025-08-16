locals {
  base_name = "${var.base_name}-${var.env}"
  rg = {
    name     = "${local.base_name}-rg"
    location = var.region
  }
  storage_acc = {
    name        = "${replace(local.base_name, "-", "")}sa"
    tier        = "Standard"
    replication = "LRS"
    containers = {
      input  = "batch-input"
      output = "batch-output"
    }
  }
  oai = {
    name                  = "${local.base_name}-oai"
    custom_subdomain_name = replace("${local.base_name}-oai", "-", "")
  }
  tags = {
    environment = var.env
    project     = local.base_name
  }
}