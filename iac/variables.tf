variable "region" {
  description = "value of the Azure region"
  default     = "swedencentral"
  type        = string
}
variable "subscription_id" {
  description = "value of the Azure subscription ID"
  type        = string
}
variable "base_name" {
  description = "value of the base name for resources"
  type        = string
}
variable "executor_object_id" {
  description = "Object ID of the user or identity that will upload files to the storage account and use the OpenAI service"
  type        = string

}
variable "env" {
  description = "Environment name (e.g., d, t, a, p)"
  default     = "d"
  type        = string
  
}